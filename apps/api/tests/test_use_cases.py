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


async def test_create_use_case_with_flows(client):
    token, project_id = await _register_and_create_project(client, "uc1@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.post(
        f"/api/projects/{project_id}/use-cases",
        json={
            "title": "Book an appointment",
            "actors": ["Patient"],
            "preconditions": "Patient is registered in the system",
            "postconditions": "Appointment is created",
            "main_flow": [
                "Patient opens the booking page",
                "Patient selects a doctor and time slot",
            ],
            "alternative_flows": [
                {
                    "name": "No available slots",
                    "condition": "Selected doctor has no free slots",
                    "steps": ["System shows a message", "Patient selects another doctor"],
                }
            ],
        },
        headers=headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["code"] == "UC-001"
    assert len(body["main_flow"]) == 2
    assert body["alternative_flows"][0]["name"] == "No available slots"


async def test_use_case_codes_increment(client):
    token, project_id = await _register_and_create_project(client, "uc2@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    async def create(title: str) -> str:
        response = await client.post(
            f"/api/projects/{project_id}/use-cases",
            json={"title": title},
            headers=headers,
        )
        return response.json()["code"]

    assert await create("Book appointment") == "UC-001"
    assert await create("Cancel appointment") == "UC-002"


async def test_update_use_case_flows(client):
    token, project_id = await _register_and_create_project(client, "uc3@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    create = await client.post(
        f"/api/projects/{project_id}/use-cases",
        json={"title": "Cancel appointment", "main_flow": ["Step 1"]},
        headers=headers,
    )
    use_case_id = create.json()["id"]

    update = await client.patch(
        f"/api/projects/{project_id}/use-cases/{use_case_id}",
        json={"main_flow": ["Step 1", "Step 2", "Step 3"]},
        headers=headers,
    )
    assert update.status_code == 200
    assert len(update.json()["main_flow"]) == 3


async def test_delete_use_case(client):
    token, project_id = await _register_and_create_project(client, "uc4@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    create = await client.post(
        f"/api/projects/{project_id}/use-cases",
        json={"title": "To delete"},
        headers=headers,
    )
    use_case_id = create.json()["id"]

    delete = await client.delete(
        f"/api/projects/{project_id}/use-cases/{use_case_id}", headers=headers
    )
    assert delete.status_code == 204

    listing = await client.get(f"/api/projects/{project_id}/use-cases", headers=headers)
    assert listing.json() == []


async def test_get_unknown_use_case_returns_404(client):
    token, project_id = await _register_and_create_project(client, "uc5@example.com")
    unknown_use_case_id = uuid.uuid4()
    response = await client.get(
        f"/api/projects/{project_id}/use-cases/{unknown_use_case_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
