import uuid

from httpx import AsyncClient


async def _register(client: AsyncClient, email: str) -> str:
    response = await client.post(
        "/api/auth/register",
        json={"email": email, "password": "password1", "full_name": "Test User"},
    )
    return response.json()["access_token"]


async def test_create_project(client) -> None:
    token = await _register(client, "owner1@example.com")
    response = await client.post(
        "/api/projects",
        json={"name": "Dental Clinic", "description": "Booking system"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Dental Clinic"
    assert body["my_role"] == "OWNER"


async def test_list_projects_only_shows_own(client) -> None:
    token_a = await _register(client, "owner2@example.com")
    token_b = await _register(client, "owner3@example.com")
    await client.post(
        "/api/projects",
        json={"name": "project"},
        headers={"Authorization": f"Bearer {token_a}"},
    )
    response = await client.get("/api/projects", headers={"Authorization": f"Bearer {token_b}"})
    assert response.status_code == 200
    assert response.json() == []


async def test_get_project_forbidden_for_non_member(client) -> None:
    token_a = await _register(client, "owner4@example.com")
    token_b = await _register(client, "owner5@example.com")
    create = await client.post(
        "/api/projects",
        json={"name": "Private project"},
        headers={"Authorization": f"Bearer {token_a}"},
    )
    project_id = create.json()["id"]
    response = await client.get(
        f"/api/projects/{project_id}", headers={"Authorization": f"Bearer {token_b}"}
    )
    assert response.status_code == 403


async def test_get_project_not_found(client) -> None:
    token = await _register(client, "owner6@example.com")
    non_existent_id = uuid.uuid4()
    response = await client.get(
        f"/api/projects/{non_existent_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


async def test_update_project(client) -> None:
    token = await _register(client, "owner7@example.com")
    create = await client.post(
        "/api/projects", json={"name": "Old name"}, headers={"Authorization": f"Bearer {token}"}
    )
    project_id = create.json()["id"]
    response = await client.patch(
        f"/api/projects/{project_id}",
        json={"name": "New name"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "New name"


async def test_archive_project_removes_from_list(client):
    token = await _register(client, "owner8@example.com")
    create = await client.post(
        "/api/projects", json={"name": "To archive"}, headers={"Authorization": f"Bearer {token}"}
    )
    project_id = create.json()["id"]
    response = await client.delete(
        f"/api/projects/{project_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204

    listing = await client.get("/api/projects", headers={"Authorization": f"Bearer {token}"})
    assert listing.json() == []
