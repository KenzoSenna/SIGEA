import json
import urllib.request
import urllib.error

BASE_URL = "http://localhost:8000"
AUTH_HEADERS = {}


def request(method, path, data=None, headers=None):
    url = f"{BASE_URL}{path}"
    request_headers = {"Content-Type": "application/json"}
    request_headers.update(AUTH_HEADERS)
    if headers:
        request_headers.update(headers)
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            text = resp.read().decode("utf-8")
            return resp.status, json.loads(text)
    except urllib.error.HTTPError as exc:
        content = exc.read().decode("utf-8")
        try:
            payload = json.loads(content)
        except Exception:
            payload = content
        return exc.code, payload
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Falha ao conectar em {url}: {exc.reason}")


def assert_status(status, expected, description):
    if status != expected:
        raise AssertionError(f"{description}: esperado {expected}, recebido {status}")


def expect_sucesso(result, expected=True):
    if not isinstance(result, dict) or 'sucesso' not in result:
        print("DEBUG: resposta sem 'sucesso':", result)
        raise AssertionError("Resposta não contém a chave 'sucesso'")
    if result['sucesso'] is not expected:
        raise AssertionError(f"esperado sucesso={expected}, recebido sucesso={result['sucesso']}")


def test_create_user():
    print("[1] Criar usuário")
    status, result = request("POST", "/usuarios", {
        "nome": "João Silva",
        "email": "joao.silva@example.com",
        "senha": "senha123",
        "tipo": "professor"
    })
    assert_status(status, 200, "POST /usuarios")
    expect_sucesso(result, True)
    assert result["usuario"]["email"] == "joao.silva@example.com"
    return result["id_usuario"]


def test_duplicate_email():
    print("[2] Validar email duplicado")
    status, result = request("POST", "/usuarios", {
        "nome": "João Silva",
        "email": "joao.silva@example.com",
        "senha": "senha123",
        "tipo": "professor"
    })
    assert_status(status, 409, "POST /usuarios email duplicado")
    expect_sucesso(result, False)


def test_login():
    print("[3] Login")
    status, result = request("POST", "/login", {
        "email": "usuario@email.com",
        "senha": "senha123"
    })
    assert_status(status, 200, "POST /login")
    expect_sucesso(result, True)
    assert result["sessao"] == "autenticada"
    assert "access_token" in result
    assert result["token_type"] == "bearer"
    AUTH_HEADERS["Authorization"] = f"Bearer {result['access_token']}"
    return result["access_token"]


def test_create_reserva_diaria():
    print("[4] Criar reserva diária")
    status, result = request("POST", "/reservas", {
        "id_sala": 201,
        "id_disciplina": 1,
        "descricao": "Aula de Matemática",
        "tipo_reserva": "diaria",
        "detalhes": {
            "data": "2026-05-20",
            "horario_inicio": "08:00:00",
            "horario_fim": "10:00:00"
        }
    })
    assert_status(status, 200, "POST /reservas diaria")
    expect_sucesso(result, True)
    assert result["reserva"]["tipo_reserva"] == "diaria"
    return result["id_reserva"]


def test_create_reserva_semestral():
    print("[5] Criar reserva semestral")
    status, result = request("POST", "/reservas", {
        "id_sala": 202,
        "id_disciplina": 2,
        "descricao": "Semestre de Física",
        "tipo_reserva": "semestral",
        "detalhes": {
            "data_inicio": "2026-05-15",
            "data_fim": "2026-12-15",
            "dias_semana": ["segunda", "quarta", "sexta"],
            "horarios": {
                "segunda": {"inicio": "08:00:00", "fim": "10:00:00"},
                "quarta": {"inicio": "14:00:00", "fim": "16:00:00"},
                "sexta": {"inicio": "10:00:00", "fim": "12:00:00"}
            }
        }
    })
    assert_status(status, 200, "POST /reservas semestral")
    expect_sucesso(result, True)
    assert result["reserva"]["tipo_reserva"] == "semestral"
    return result["id_reserva"]


def test_list_reservas():
    print("[6] Listar reservas")
    status, result = request("GET", "/reservas")
    assert_status(status, 200, "GET /reservas")
    expect_sucesso(result, True)
    assert "reservas" in result


def test_get_reserva(id_reserva):
    print("[7] Obter reserva por ID")
    status, result = request("GET", f"/reservas/{id_reserva}")
    assert_status(status, 200, "GET /reservas/{id_reserva}")
    assert result["reserva"]["tipo_reserva"] in ["diaria", "semestral"]


def test_cancel_reserva(id_reserva):
    print("[8] Cancelar reserva")
    status, result = request("DELETE", f"/reservas/{id_reserva}")
    assert_status(status, 200, "DELETE /reservas/{id_reserva}")
    expect_sucesso(result, True)


def test_get_user(id_usuario):
    print("[9] Obter usuário por ID")
    status, result = request("GET", f"/usuarios/{id_usuario}")
    assert_status(status, 200, "GET /usuarios/{id_usuario}")
    assert result["usuario"]["email"] == "joao.silva@example.com"


def test_delete_user(id_usuario):
    print("[10] Excluir usuário")
    status, result = request("DELETE", f"/usuarios/{id_usuario}")
    assert_status(status, 200, "DELETE /usuarios/{id_usuario}")
    expect_sucesso(result, True)


def run_test(name, func, *args):
    try:
        return func(*args)
    except Exception as exc:
        print(f"FALHA em {name}: {exc}")
        return None


def main():
    print("Executando testes da API... certifique-se de que o servidor está rodando em http://localhost:8000")

    user_id = run_test("Criar usuário", test_create_user)
    run_test("Validar email duplicado", test_duplicate_email)
    run_test("Login", test_login)

    reserva_diaria_id = run_test("Criar reserva diária", test_create_reserva_diaria)
    reserva_semestral_id = run_test("Criar reserva semestral", test_create_reserva_semestral)
    run_test("Listar reservas", test_list_reservas)

    if reserva_diaria_id is not None:
        run_test("Obter reserva por ID", test_get_reserva, reserva_diaria_id)
        run_test("Cancelar reserva", test_cancel_reserva, reserva_diaria_id)
    else:
        print("Pular testes dependentes de reserva diária porque a criação falhou.")

    if user_id is not None:
        run_test("Obter usuário por ID", test_get_user, user_id)
        run_test("Excluir usuário", test_delete_user, user_id)
    else:
        print("Pular testes dependentes de usuário porque a criação falhou.")

    print("\nExecução de testes finalizada.")


if __name__ == "__main__":
    main()
