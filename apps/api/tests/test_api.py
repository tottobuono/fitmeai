"""Test degli endpoint HTTP."""

from __future__ import annotations

from tests.conftest import valid_payload


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_create_job_persists_and_enqueues(client, queue):
    resp = client.post("/tryon-jobs", json=valid_payload())
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "queued"
    assert body["user_id"] == "user-1"
    assert body["id"]
    # L'id e' stato accodato esattamente una volta.
    assert queue.enqueued == [body["id"]]


def test_get_job_roundtrip(client):
    created = client.post("/tryon-jobs", json=valid_payload()).json()
    resp = client.get(f"/tryon-jobs/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]
    assert resp.json()["request"]["mode"] == "measurements_only"


def test_get_job_not_found(client):
    assert client.get("/tryon-jobs/does-not-exist").status_code == 404


def test_create_job_invalid_mode_rejected(client):
    payload = valid_payload()
    # photo_measurements senza person_image_url -> 422 dal contratto di dominio
    payload["request"]["mode"] = "photo_measurements"
    payload["request"].pop("avatar_image_url", None)
    resp = client.post("/tryon-jobs", json=payload)
    assert resp.status_code == 422


def test_create_job_extra_field_rejected(client):
    payload = valid_payload()
    payload["unexpected"] = "x"
    assert client.post("/tryon-jobs", json=payload).status_code == 422
