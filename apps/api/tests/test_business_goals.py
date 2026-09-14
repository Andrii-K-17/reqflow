from httpx import AsyncClient


async def _register_and_create_project(client: AsyncClient, email: str) -> tuple[str, str]:
    register = await client.post(
        "/api/auth/register",
        json={"email": email, "password": "password1", "full_name": "Test User"},
    )
    token = register.json()["access_token"]
    project = await client.post(
        "/api/projects",
        json={"name": "Test"},
        headers={"Authorization": f"Bearer {token}"},
    )
    return token, project.json()["id"]


async def test_create_and_list_business_goals(client):
    token, project_id = await _register_and_create_project(client, "goal1@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    create = await client.post(
        f"/api/projects/{project_id}/business-goals",
        json={
            "title": "goal1",
            "priority": "HIGH",
        },
        headers=headers,
    )
    assert create.status_code == 201
    assert create.json()["priority"] == "HIGH"

    listing = await client.get(f"/api/projects/{project_id}/business-goals", headers=headers)
    assert len(listing.json()) == 1


async def test_default_priority_is_medium(client):
    token, project_id = await _register_and_create_project(client, "goal2@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    create = await client.post(
        f"/api/projects/{project_id}/business-goals",
        json={"title": "goal2"},
        headers=headers,
    )
    assert create.json()["priority"] == "MEDIUM"


async def test_update_and_delete_business_goal(client):
    token, project_id = await _register_and_create_project(client, "goal3@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    create = await client.post(
        f"/api/projects/{project_id}/business-goals",
        json={"title": "goal3"},
        headers=headers,
    )
    goal_id = create.json()["id"]

    update = await client.patch(
        f"/api/projects/{project_id}/business-goals/{goal_id}",
        json={"priority": "CRITICAL"},
        headers=headers,
    )
    assert update.json()["priority"] == "CRITICAL"

    delete = await client.delete(
        f"/api/projects/{project_id}/business-goals/{goal_id}", headers=headers
    )
    assert delete.status_code == 204


async def test_non_member_forbidden(client):
    _, project_id = await _register_and_create_project(client, "goal4@example.com")
    other_register = await client.post(
        "/api/auth/register",
        json={"email": "goal5@example.com", "password": "password1", "full_name": "Other"},
    )
    other_token = other_register.json()["access_token"]

    response = await client.get(
        f"/api/projects/{project_id}/business-goals",
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert response.status_code == 403
