"""Test sui contratti di dominio condivisi."""

import pytest
from pydantic import ValidationError

from app.domain import (
    BodyMeasurements,
    BodyProfile,
    Garment,
    GarmentCategory,
    JobStatus,
    TryOnJob,
    TryOnMode,
    TryOnRequest,
    TryOnResult,
)


def test_body_measurements_rejects_non_positive_values():
    with pytest.raises(ValidationError):
        BodyMeasurements(height_cm=0, weight_kg=70)


def test_body_measurements_defaults():
    m = BodyMeasurements(height_cm=180, weight_kg=75)
    assert m.unit.value == "metric"
    assert m.fit_preference.value == "regular"
    assert m.chest_cm is None


def test_extra_fields_forbidden():
    with pytest.raises(ValidationError):
        BodyMeasurements(height_cm=180, weight_kg=75, unexpected="x")


def test_tryon_request_photo_mode_requires_person_image():
    with pytest.raises(ValidationError):
        TryOnRequest(
            mode=TryOnMode.PHOTO_MEASUREMENTS,
            garment_image_url="https://signed/garment.png",
        )


def test_tryon_request_measurements_only_requires_avatar():
    with pytest.raises(ValidationError):
        TryOnRequest(
            mode=TryOnMode.MEASUREMENTS_ONLY,
            garment_image_url="https://signed/garment.png",
        )


def test_tryon_request_valid_photo_mode():
    req = TryOnRequest(
        mode=TryOnMode.PHOTO_MEASUREMENTS,
        garment_image_url="https://signed/garment.png",
        person_image_url="https://signed/person.png",
    )
    assert req.samples == 1
    assert req.quality.value == "standard"


def test_tryon_request_samples_bounds():
    with pytest.raises(ValidationError):
        TryOnRequest(
            mode=TryOnMode.MEASUREMENTS_ONLY,
            garment_image_url="https://signed/garment.png",
            avatar_image_url="https://signed/avatar.png",
            samples=5,
        )


def test_job_lifecycle_shape():
    req = TryOnRequest(
        mode=TryOnMode.MEASUREMENTS_ONLY,
        garment_image_url="https://signed/garment.png",
        avatar_image_url="https://signed/avatar.png",
    )
    job = TryOnJob(user_id="user-1", request=req)
    assert job.status is JobStatus.QUEUED
    assert job.result is None
    assert job.id  # auto-generato

    job.result = TryOnResult(
        status=JobStatus.DONE,
        provider="mock",
        output_image_urls=["https://signed/out-0.png"],
    )
    job.status = JobStatus.DONE
    assert job.result.provider == "mock"


def test_garment_minimal():
    g = Garment(category=GarmentCategory.TOP, image_url="https://signed/top.png")
    assert g.brand is None
    assert g.id


def test_body_profile_has_no_inline_photos():
    profile = BodyProfile(
        user_id="user-1",
        measurements=BodyMeasurements(height_cm=170, weight_kg=65),
    )
    # Le foto sono solo riferimenti a storage, mai binari inline.
    assert profile.photo_storage_keys == []
