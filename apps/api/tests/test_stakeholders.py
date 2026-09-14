import uuid

from httpx import AsyncClient


async def _register_and_create_project(client: AsyncClient, email: str) -> tuple[str, str]:
    register = await client.post(
        "/api/auth/register",
        json={"email": email, "password": "password1", "full_name": "Test User"},
    )
    token = register.json()["access_token"]
    project = await client.post(
        "/api/projects",
        json={"name": "Dental Clinic"},
        headers={"Authorization": f"Bearer {token}"},
    )
    return token, project.json()["id"]


async def test_create_and_list_stakeholders(client):
    token, project_id = await _register_and_create_project(client, "user1@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    create = await client.post(
        f"/api/projects/{project_id}/stakeholders",
        json={
            "name": "Patient",
            "category": "PRIMARY",
            "interest_description": "Books appointments",
        },
        headers=headers,
    )
    assert create.status_code == 201
    assert create.json()["name"] == "Patient"

    listing = await client.get(f"/api/projects/{project_id}/stakeholders", headers=headers)
    assert listing.status_code == 200
    assert len(listing.json()) == 1


async def test_update_stakeholder(client):
    token, project_id = await _register_and_create_project(client, "user2@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    create = await client.post(
        f"/api/projects/{project_id}/stakeholders",
        json={"name": "Doctor", "category": "PRIMARY"},
        headers=headers,
    )
    stakeholder_id = create.json()["id"]

    update = await client.patch(
        f"/api/projects/{project_id}/stakeholders/{stakeholder_id}",
        json={"category": "SECONDARY"},
        headers=headers,
    )
    assert update.status_code == 200
    assert update.json()["category"] == "SECONDARY"


async def test_delete_stakeholder(client):
    token, project_id = await _register_and_create_project(client, "user3@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    create = await client.post(
        f"/api/projects/{project_id}/stakeholders",
        json={"name": "Administrator", "category": "PRIMARY"},
        headers=headers,
    )
    stakeholder_id = create.json()["id"]

    delete = await client.delete(
        f"/api/projects/{project_id}/stakeholders/{stakeholder_id}", headers=headers
    )
    assert delete.status_code == 204

    listing = await client.get(f"/api/projects/{project_id}/stakeholders", headers=headers)
    assert listing.json() == []


async def test_non_member_forbidden(client):
    _, project_id = await _register_and_create_project(client, "user4@example.com")
    other_register = await client.post(
        "/api/auth/register",
        json={"email": "user5@example.com", "password": "password1", "full_name": "Other"},
    )
    other_token = other_register.json()["access_token"]

    response = await client.get(
        f"/api/projects/{project_id}/stakeholders",
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert response.status_code == 403


async def test_unknown_project_returns_404(client):
    token, _ = await _register_and_create_project(client, "user6@example.com")
    unknown_project_id = uuid.uuid4()
    response = await client.get(
        f"/api/projects/{unknown_project_id}/stakeholders",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


async def test_unknown_stakeholder_returns_404(client):
    token, project_id = await _register_and_create_project(client, "user7@example.com")
    unknown_stakeholder_id = uuid.uuid4()
    response = await client.patch(
        f"/api/projects/{project_id}/stakeholders/{unknown_stakeholder_id}",
        json={"name": "Ghost"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
