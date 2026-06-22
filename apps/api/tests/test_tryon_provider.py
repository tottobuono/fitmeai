"""Test del layer di try-on: MockProvider e factory."""

import asyncio

import pytest

from app.domain.enums import JobStatus, TryOnMode
from app.domain.models import TryOnRequest
from app.tryon import (
    TryOnProviderError,
    VirtualTryOnProvider,
    get_provider,
)
from app.tryon.providers.mock import MockProvider


def _photo_request(samples: int = 1) -> TryOnRequest:
    return TryOnRequest(
        mode=TryOnMode.PHOTO_MEASUREMENTS,
        garment_image_url="https://signed/garment.png",
        person_image_url="https://signed/person.png",
        samples=samples,
    )


def test_factory_default_is_mock(monkeypatch):
    monkeypatch.delenv("TRYON_PROVIDER", raising=False)
    provider = get_provider()
    assert isinstance(provider, MockProvider)
    assert isinstance(provider, VirtualTryOnProvider)


def test_factory_reads_env(monkeypatch):
    monkeypatch.setenv("TRYON_PROVIDER", "mock")
    assert get_provider().name == "mock"


def test_factory_unknown_provider_raises(monkeypatch):
    monkeypatch.setenv("TRYON_PROVIDER", "does-not-exist")
    with pytest.raises(TryOnProviderError):
        get_provider()


def test_mock_generate_returns_done_with_outputs():
    provider = MockProvider(latency_s=0)
    result = asyncio.run(provider.generate(_photo_request(samples=3)))
    assert result.status is JobStatus.DONE
    assert result.provider == "mock"
    assert len(result.output_image_urls) == 3
    assert result.cost_estimate == 0.0
    assert result.latency_ms is not None


def test_mock_capabilities():
    caps = MockProvider().capabilities()
    assert caps.name == "mock"
    assert caps.max_samples >= 1
    assert caps.supported_categories
