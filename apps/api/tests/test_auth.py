async def test_register_returns_token_pair(client):
    response = await client.post(
        "/api/auth/register",
        json={"email": "user1@example.com", "password": "password1", "full_name": "user1"},
    )
    assert response.status_code == 201
    body = response.json()
    assert "access_token" in body
    assert "refresh_token" in body


async def test_register_duplicate_email_fails(client):
    payload = {"email": "user2@example.com", "password": "password1", "full_name": "user2"}
    await client.post("/api/auth/register", json=payload)
    response = await client.post("/api/auth/register", json=payload)
    assert response.status_code == 409


async def test_login_success(client):
    await client.post(
        "/api/auth/register",
        json={"email": "user3@example.com", "password": "password1", "full_name": "user3"},
    )
    response = await client.post(
        "/api/auth/login", json={"email": "user3@example.com", "password": "password1"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


async def test_login_wrong_password_fails(client):
    await client.post(
        "/api/auth/register",
        json={"email": "user4@example.com", "password": "password1", "full_name": "user4"},
    )
    response = await client.post(
        "/api/auth/login", json={"email": "user4@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401


async def test_me_requires_auth(client):
    response = await client.get("/api/auth/me")
    assert response.status_code == 401


async def test_me_returns_current_user(client):
    register = await client.post(
        "/api/auth/register",
        json={"email": "user5@example.com", "password": "password1", "full_name": "user5"},
    )
    token = register.json()["access_token"]
    response = await client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "user5@example.com"


async def test_refresh_issues_new_token_pair(client):
    register = await client.post(
        "/api/auth/register",
        json={"email": "user5@example.com", "password": "password1", "full_name": "user5"},
    )
    refresh_token = register.json()["refresh_token"]
    response = await client.post("/api/auth/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    assert "access_token" in response.json()
