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


async def test_create_user_story_with_acceptance_criteria(client):
    token, project_id = await _register_and_create_project(client, "us1@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.post(
        f"/api/projects/{project_id}/user-stories",
        json={
            "role": "Patient",
            "goal": "book an appointment online",
            "benefit": "I don't have to call the clinic",
            "acceptance_criteria": [
                "Given available slots, patient can pick one",
                "Patient receives a confirmation",
            ],
        },
        headers=headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["code"] == "US-001"
    assert len(body["acceptance_criteria"]) == 2


async def test_user_story_codes_increment(client):
    token, project_id = await _register_and_create_project(client, "us2@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    async def create(role: str) -> str:
        response = await client.post(
            f"/api/projects/{project_id}/user-stories",
            json={"role": role, "goal": "do something", "benefit": "value"},
            headers=headers,
        )
        return response.json()["code"]

    assert await create("Patient") == "US-001"
    assert await create("Administrator") == "US-002"


async def test_update_and_delete_user_story(client):
    token, project_id = await _register_and_create_project(client, "us3@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    create = await client.post(
        f"/api/projects/{project_id}/user-stories",
        json={"role": "Doctor", "goal": "see my schedule", "benefit": "plan my day"},
        headers=headers,
    )
    story_id = create.json()["id"]

    update = await client.patch(
        f"/api/projects/{project_id}/user-stories/{story_id}",
        json={"acceptance_criteria": ["Schedule shows all appointments for today"]},
        headers=headers,
    )
    assert update.status_code == 200
    assert len(update.json()["acceptance_criteria"]) == 1

    delete = await client.delete(
        f"/api/projects/{project_id}/user-stories/{story_id}", headers=headers
    )
    assert delete.status_code == 204


async def test_non_member_forbidden(client):
    _, project_id = await _register_and_create_project(client, "us4@example.com")
    other_register = await client.post(
        "/api/auth/register",
        json={"email": "us5@example.com", "password": "password1", "full_name": "Other"},
    )
    other_token = other_register.json()["access_token"]

    response = await client.get(
        f"/api/projects/{project_id}/user-stories",
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert response.status_code == 403
