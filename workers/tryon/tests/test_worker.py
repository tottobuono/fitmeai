"""Test della logica di elaborazione del worker."""

from __future__ import annotations

import asyncio

from app.db.repository import TryOnJobRepository
from app.domain.enums import JobStatus, TryOnMode
from app.domain.models import TryOnJob, TryOnRequest, TryOnResult
from app.tryon.errors import InvalidTryOnInputError, ProviderTimeoutError
from app.tryon.provider import ProviderCapabilities, VirtualTryOnProvider
from app.tryon.providers.mock import MockProvider

from worker import process_job


def _make_job(session_factory) -> str:
    req = TryOnRequest(
        mode=TryOnMode.MEASUREMENTS_ONLY,
        garment_image_url="https://signed/garment.png",
        avatar_image_url="https://signed/avatar.png",
    )
    job = TryOnJob(user_id="user-1", request=req)
    with session_factory() as session:
        TryOnJobRepository(session).create(job)
    return job.id


def _get(session_factory, job_id):
    with session_factory() as session:
        return TryOnJobRepository(session).get(job_id)


def test_process_job_success(session_factory):
    job_id = _make_job(session_factory)
    status = asyncio.run(process_job(job_id, session_factory, MockProvider(latency_s=0)))
    assert status is JobStatus.DONE
    job = _get(session_factory, job_id)
    assert job.status is JobStatus.DONE
    assert job.result is not None
    assert job.result.output_image_urls


def test_process_job_missing_returns_none(session_factory):
    status = asyncio.run(process_job("nope", session_factory, MockProvider(latency_s=0)))
    assert status is None


class _PermanentFailProvider(VirtualTryOnProvider):
    name = "perm-fail"

    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(name=self.name, supported_categories=[], max_samples=1)

    async def generate(self, request):
        raise InvalidTryOnInputError("bad input", provider=self.name)


def test_process_job_permanent_failure(session_factory):
    job_id = _make_job(session_factory)
    status = asyncio.run(process_job(job_id, session_factory, _PermanentFailProvider()))
    assert status is JobStatus.FAILED
    job = _get(session_factory, job_id)
    assert job.status is JobStatus.FAILED
    assert job.error


class _FlakyProvider(VirtualTryOnProvider):
    """Fallisce con errore ritentabile le prime N volte, poi riesce."""

    name = "flaky"

    def __init__(self, fail_times: int) -> None:
        self._fail_times = fail_times
        self.calls = 0

    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(name=self.name, supported_categories=[], max_samples=1)

    async def generate(self, request):
        self.calls += 1
        if self.calls <= self._fail_times:
            raise ProviderTimeoutError("timeout", provider=self.name)
        return TryOnResult(status=JobStatus.DONE, provider=self.name,
                           output_image_urls=["https://signed/out.png"])


def test_process_job_retries_then_succeeds(session_factory):
    job_id = _make_job(session_factory)
    provider = _FlakyProvider(fail_times=2)
    status = asyncio.run(
        process_job(job_id, session_factory, provider, max_attempts=3, base_backoff_s=0)
    )
    assert status is JobStatus.DONE
    assert provider.calls == 3
    assert _get(session_factory, job_id).status is JobStatus.DONE
