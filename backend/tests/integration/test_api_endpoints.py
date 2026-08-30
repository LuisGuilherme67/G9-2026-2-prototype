from fastapi.testclient import TestClient

def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "Tamburetei UnB" in data["project"]

def test_auth_register_and_login(client: TestClient):
    # Registro
    user_payload = {
        "name": "Aluno UnB",
        "email": "aluno@aluno.unb.br",
        "password": "senha_segura_123",
        "role": "student"
    }
    response = client.post("/api/v1/auth/register", json=user_payload)
    assert response.status_code == 201
    created_user = response.json()
    assert created_user["email"] == "aluno@aluno.unb.br"

    # Login
    login_payload = {
        "email": "aluno@aluno.unb.br",
        "password": "senha_segura_123"
    }
    login_res = client.post("/api/v1/auth/login", json=login_payload)
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

def test_listar_cursos_vazio(client: TestClient):
    response = client.get("/api/v1/cursos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
