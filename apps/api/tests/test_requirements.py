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
        json={"name": "project"},
        headers={"Authorization": f"Bearer {token}"},
    )
    return token, project.json()["id"]


async def test_create_requirement_generates_code(client):
    token, project_id = await _register_and_create_project(client, "req1@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.post(
        f"/api/projects/{project_id}/requirements",
        json={"type": "FUNCTIONAL", "title": "title"},
        headers=headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["code"] == "FR-001"
    assert body["status"] == "DRAFT"
    assert body["priority"] == "MEDIUM"


async def test_codes_increment_per_type_independently(client):
    token, project_id = await _register_and_create_project(client, "req2@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    async def create(req_type: str) -> str:
        response = await client.post(
            f"/api/projects/{project_id}/requirements",
            json={"type": req_type, "title": "title"},
            headers=headers,
        )
        return response.json()["code"]

    assert await create("FUNCTIONAL") == "FR-001"
    assert await create("FUNCTIONAL") == "FR-002"
    assert await create("NONFUNCTIONAL") == "NFR-001"
    assert await create("BUSINESS") == "BR-001"


async def test_codes_are_scoped_per_project(client):
    token, project_a = await _register_and_create_project(client, "req3@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    project_b = (
        await client.post("/api/projects", json={"name": "Second project"}, headers=headers)
    ).json()["id"]

    code_a = (
        await client.post(
            f"/api/projects/{project_a}/requirements",
            json={"type": "FUNCTIONAL", "title": "requirement in project a"},
            headers=headers,
        )
    ).json()["code"]
    code_b = (
        await client.post(
            f"/api/projects/{project_b}/requirements",
            json={"type": "FUNCTIONAL", "title": "requirement in project b"},
            headers=headers,
        )
    ).json()["code"]

    assert code_a == "FR-001"
    assert code_b == "FR-001"


async def test_filter_by_type_status_priority(client):
    token, project_id = await _register_and_create_project(client, "req4@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    await client.post(
        f"/api/projects/{project_id}/requirements",
        json={"type": "FUNCTIONAL", "title": "FR one", "priority": "HIGH"},
        headers=headers,
    )
    await client.post(
        f"/api/projects/{project_id}/requirements",
        json={"type": "NONFUNCTIONAL", "title": "NFR one", "priority": "LOW"},
        headers=headers,
    )

    response = await client.get(
        f"/api/projects/{project_id}/requirements?type=FUNCTIONAL", headers=headers
    )
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["type"] == "FUNCTIONAL"

    response = await client.get(
        f"/api/projects/{project_id}/requirements?priority=LOW", headers=headers
    )
    assert response.json()["total"] == 1


async def test_pagination(client):
    token, project_id = await _register_and_create_project(client, "req5@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    for i in range(5):
        await client.post(
            f"/api/projects/{project_id}/requirements",
            json={"type": "FUNCTIONAL", "title": f"FR {i}"},
            headers=headers,
        )

    response = await client.get(
        f"/api/projects/{project_id}/requirements?page=1&page_size=2", headers=headers
    )
    body = response.json()
    assert body["total"] == 5
    assert len(body["items"]) == 2


async def test_update_requirement_status(client):
    token, project_id = await _register_and_create_project(client, "req6@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    create = await client.post(
        f"/api/projects/{project_id}/requirements",
        json={"type": "FUNCTIONAL", "title": "requirement"},
        headers=headers,
    )
    requirement_id = create.json()["id"]

    update = await client.patch(
        f"/api/projects/{project_id}/requirements/{requirement_id}",
        json={"status": "APPROVED", "verifiable": False},
        headers=headers,
    )
    assert update.status_code == 200
    assert update.json()["status"] == "APPROVED"
    assert update.json()["verifiable"] is False


async def test_delete_requirement(client):
    token, project_id = await _register_and_create_project(client, "req7@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    create = await client.post(
        f"/api/projects/{project_id}/requirements",
        json={"type": "FUNCTIONAL", "title": "To delete"},
        headers=headers,
    )
    requirement_id = create.json()["id"]

    delete = await client.delete(
        f"/api/projects/{project_id}/requirements/{requirement_id}", headers=headers
    )
    assert delete.status_code == 204

    listing = await client.get(f"/api/projects/{project_id}/requirements", headers=headers)
    assert listing.json()["total"] == 0


async def test_get_unknown_requirement_returns_404(client):
    token, project_id = await _register_and_create_project(client, "req8@example.com")
    unknown_requirement_id = uuid.uuid4()
    response = await client.get(
        f"/api/projects/{project_id}/requirements/{unknown_requirement_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


async def test_non_member_forbidden(client):
    _, project_id = await _register_and_create_project(client, "req9@example.com")
    other_register = await client.post(
        "/api/auth/register",
        json={"email": "req10@example.com", "password": "password1", "full_name": "name"},
    )
    other_token = other_register.json()["access_token"]

    response = await client.get(
        f"/api/projects/{project_id}/requirements",
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert response.status_code == 403
