import uuid

from httpx import AsyncClient


async def _setup_project(client: AsyncClient, email: str) -> tuple[str, str]:
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


async def _create_goal(client: AsyncClient, headers: dict, project_id: str, title: str) -> str:
    response = await client.post(
        f"/api/projects/{project_id}/business-goals", json={"title": title}, headers=headers
    )
    return response.json()["id"]


async def _create_requirement(
    client: AsyncClient, headers: dict, project_id: str, title: str
) -> str:
    response = await client.post(
        f"/api/projects/{project_id}/requirements",
        json={"type": "FUNCTIONAL", "title": title},
        headers=headers,
    )
    return response.json()["id"]


async def _create_use_case(client: AsyncClient, headers: dict, project_id: str, title: str) -> str:
    response = await client.post(
        f"/api/projects/{project_id}/use-cases", json={"title": title}, headers=headers
    )
    return response.json()["id"]


async def test_create_trace_link_between_requirement_and_goal(client):
    token, project_id = await _setup_project(client, "trace1@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    goal_id = await _create_goal(client, headers, project_id, "goal")
    req_id = await _create_requirement(client, headers, project_id, "requirement")

    response = await client.post(
        f"/api/projects/{project_id}/trace-links",
        json={
            "from_type": "REQUIREMENT",
            "from_id": req_id,
            "to_type": "BUSINESS_GOAL",
            "to_id": goal_id,
            "relation": "DERIVES_FROM",
        },
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["relation"] == "DERIVES_FROM"


async def test_link_to_nonexistent_entity_returns_404(client):
    token, project_id = await _setup_project(client, "trace2@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    req_id = await _create_requirement(client, headers, project_id, "requirement")
    nonexistent_entity_id = uuid.uuid4()

    response = await client.post(
        f"/api/projects/{project_id}/trace-links",
        json={
            "from_type": "REQUIREMENT",
            "from_id": req_id,
            "to_type": "BUSINESS_GOAL",
            "to_id": f"{nonexistent_entity_id}",
            "relation": "DERIVES_FROM",
        },
        headers=headers,
    )
    assert response.status_code == 404


async def test_self_link_rejected(client):
    token, project_id = await _setup_project(client, "trace3@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    req_id = await _create_requirement(client, headers, project_id, "requirement")

    response = await client.post(
        f"/api/projects/{project_id}/trace-links",
        json={
            "from_type": "REQUIREMENT",
            "from_id": req_id,
            "to_type": "REQUIREMENT",
            "to_id": req_id,
            "relation": "DERIVES_FROM",
        },
        headers=headers,
    )
    assert response.status_code == 422


async def test_duplicate_link_rejected(client):
    token, project_id = await _setup_project(client, "trace4@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    goal_id = await _create_goal(client, headers, project_id, "goal")
    req_id = await _create_requirement(client, headers, project_id, "requirement")

    payload = {
        "from_type": "REQUIREMENT",
        "from_id": req_id,
        "to_type": "BUSINESS_GOAL",
        "to_id": goal_id,
        "relation": "DERIVES_FROM",
    }
    first = await client.post(
        f"/api/projects/{project_id}/trace-links", json=payload, headers=headers
    )
    assert first.status_code == 201

    second = await client.post(
        f"/api/projects/{project_id}/trace-links", json=payload, headers=headers
    )
    assert second.status_code == 409


async def test_cycle_detection_rejects_circular_dependency(client):
    token, project_id = await _setup_project(client, "trace5@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    req_a = await _create_requirement(client, headers, project_id, "requirement A")
    req_b = await _create_requirement(client, headers, project_id, "requirement B")
    use_case = await _create_use_case(client, headers, project_id, "use case")

    link1 = await client.post(
        f"/api/projects/{project_id}/trace-links",
        json={
            "from_type": "USE_CASE",
            "from_id": use_case,
            "to_type": "REQUIREMENT",
            "to_id": req_a,
            "relation": "SATISFIES",
        },
        headers=headers,
    )
    assert link1.status_code == 201

    link2 = await client.post(
        f"/api/projects/{project_id}/trace-links",
        json={
            "from_type": "REQUIREMENT",
            "from_id": req_a,
            "to_type": "REQUIREMENT",
            "to_id": req_b,
            "relation": "DERIVES_FROM",
        },
        headers=headers,
    )
    assert link2.status_code == 201

    link3 = await client.post(
        f"/api/projects/{project_id}/trace-links",
        json={
            "from_type": "REQUIREMENT",
            "from_id": req_b,
            "to_type": "USE_CASE",
            "to_id": use_case,
            "relation": "DERIVES_FROM",
        },
        headers=headers,
    )
    assert link3.status_code == 422


async def test_conflicts_with_does_not_trigger_cycle_check(client):
    token, project_id = await _setup_project(client, "trace6@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    req_a = await _create_requirement(client, headers, project_id, "requirement A")
    req_b = await _create_requirement(client, headers, project_id, "requirement B")

    first = await client.post(
        f"/api/projects/{project_id}/trace-links",
        json={
            "from_type": "REQUIREMENT",
            "from_id": req_a,
            "to_type": "REQUIREMENT",
            "to_id": req_b,
            "relation": "CONFLICTS_WITH",
        },
        headers=headers,
    )
    assert first.status_code == 201

    second = await client.post(
        f"/api/projects/{project_id}/trace-links",
        json={
            "from_type": "REQUIREMENT",
            "from_id": req_b,
            "to_type": "REQUIREMENT",
            "to_id": req_a,
            "relation": "CONFLICTS_WITH",
        },
        headers=headers,
    )
    assert second.status_code == 201


async def test_graph_endpoint_returns_resolved_nodes(client):
    token, project_id = await _setup_project(client, "trace7@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    goal_id = await _create_goal(client, headers, project_id, "goal")
    req_id = await _create_requirement(client, headers, project_id, "requirement")

    await client.post(
        f"/api/projects/{project_id}/trace-links",
        json={
            "from_type": "REQUIREMENT",
            "from_id": req_id,
            "to_type": "BUSINESS_GOAL",
            "to_id": goal_id,
            "relation": "DERIVES_FROM",
        },
        headers=headers,
    )

    response = await client.get(f"/api/projects/{project_id}/trace-links/graph", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert len(body["nodes"]) == 2
    assert len(body["edges"]) == 1
    codes = {node["code"] for node in body["nodes"]}
    assert "FR-001" in codes


async def test_delete_trace_link(client):
    token, project_id = await _setup_project(client, "trace8@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    goal_id = await _create_goal(client, headers, project_id, "goal")
    req_id = await _create_requirement(client, headers, project_id, "requirement")

    create = await client.post(
        f"/api/projects/{project_id}/trace-links",
        json={
            "from_type": "REQUIREMENT",
            "from_id": req_id,
            "to_type": "BUSINESS_GOAL",
            "to_id": goal_id,
            "relation": "DERIVES_FROM",
        },
        headers=headers,
    )
    link_id = create.json()["id"]

    delete = await client.delete(
        f"/api/projects/{project_id}/trace-links/{link_id}", headers=headers
    )
    assert delete.status_code == 204

    listing = await client.get(f"/api/projects/{project_id}/trace-links", headers=headers)
    assert listing.json() == []
