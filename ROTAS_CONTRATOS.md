# Documentação de Contratos das Rotas - SIGEA

**Versão:** 1.0
**Data:** 2026-05-15  
**Base URL:** `http://localhost:8000`
**Server URL** `https://api2.sigea.fun/` 

---

1. [Autenticação](#autenticação)
2. [Reservas](#reservas)
3. [Usuários](#usuários)

---

## Autenticação

### POST /login

Realiza autenticação do usuário no sistema.

**Request Body:**
```json
{
  "email": "string",
  "senha": "string"
}
```

**Validações:**
- `email`: Deve corresponder ao email registrado
- `senha`: Deve corresponder à senha registrada

**Exemplo de Requisição:**
```bash
curl -X POST "{ServerURL}" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@email.com",
    "senha": "senha123"
  }'
```

**Response (200 - Sucesso):**
```json
{
  "sucesso": true,
  "mensagem": "Autenticação realizada com sucesso",
  "email": "usuario@email.com",
  "sessao": "autenticada"
}
```

**Response (401 - Credenciais Inválidas):**
```json
{
  "sucesso": false,
  "mensagem": "Credenciais inválidas"
}
```

---

## Reservas

### POST /reservas

Cria uma nova reserva de sala. Suporta dois tipos: **diária** e **semestral**.

**Request Body - Tipo Diária:**
```json
{
  "id_sala": 201,
  "id_disciplina": 1,
  "descricao": "string (até 500 caracteres)",
  "tipo_reserva": "diaria",
  "detalhes": {
    "data": "YYYY-MM-DD",
    "horario_inicio": "HH:MM:SS",
    "horario_fim": "HH:MM:SS"
  }
}
```

**Request Body - Tipo Semestral:**
```json
{
  "id_sala": 201,
  "id_disciplina": 1,
  "descricao": "string (até 500 caracteres)",
  "tipo_reserva": "semestral",
  "detalhes": {
    "data_inicio": "YYYY-MM-DD",
    "data_fim": "YYYY-MM-DD",
    "dias_semana": ["segunda", "quarta", "sexta"],
    "horarios": {
      "segunda": {
        "inicio": "HH:MM:SS",
        "fim": "HH:MM:SS"
      },
      "quarta": {
        "inicio": "HH:MM:SS",
        "fim": "HH:MM:SS"
      },
      "sexta": {
        "inicio": "HH:MM:SS",
        "fim": "HH:MM:SS"
      }
    }
  }
}
```

**Validações:**
- `id_sala`: Deve existir na lista de salas disponíveis (201, 202, 204)
- `horario_fim`: Deve ser maior que `horario_inicio`
- `data_fim`: Deve ser maior que `data_inicio`
- Não deve haver conflito de horários na mesma sala
- Dias válidos: "segunda", "terca", "quarta", "quinta", "sexta", "sabado", "domingo"

**Exemplo - Reserva Diária:**
```bash
curl -X POST "ServerURL/reservas" \
  -H "Content-Type: application/json" \
  -d '{
    "id_sala": 201,
    "id_disciplina": 1,
    "descricao": "Aula de Matemática",
    "tipo_reserva": "diaria",
    "detalhes": {
      "data": "2026-05-20",
      "horario_inicio": "08:00:00",
      "horario_fim": "10:00:00"
    }
  }'
```

**Exemplo - Reserva Semestral:**
```bash
curl -X POST "ServerURL/reservas" \
  -H "Content-Type: application/json" \
  -d '{
    "id_sala": 201,
    "id_disciplina": 1,
    "descricao": "Matemática - Semestre 2026.1",
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
  }'
```

**Response (200 - Sucesso):**
```json
{
  "sucesso": true,
  "mensagem": "Reserva diaria realizada com sucesso!",
  "id_reserva": 1,
  "reserva": {
    "id_sala": 201,
    "id_disciplina": 1,
    "descricao": "Aula de Matemática",
    "tipo_reserva": "diaria",
    "data": "2026-05-20",
    "horario_inicio": "08:00:00",
    "horario_fim": "10:00:00"
  }
}
```

**Response (404 - Sala não encontrada):**
```json
{
  "sucesso": false,
  "mensagem": "Sala não encontrada"
}
```

**Response (409 - Conflito de horário):**
```json
{
  "sucesso": false,
  "mensagem": "Horário indisponível nesta sala"
}
```

---

### GET /reservas

Lista todas as reservas cadastradas.

**Parâmetros:** Nenhum

**Response (200 - Sucesso):**
```json
{
  "sucesso": true,
  "total": 2,
  "reservas": {
    "1": {
      "id_sala": 201,
      "id_disciplina": 1,
      "descricao": "Aula de Matemática",
      "tipo_reserva": "diaria",
      "data": "2026-05-20",
      "horario_inicio": "08:00:00",
      "horario_fim": "10:00:00"
    },
    "2": {
      "id_sala": 202,
      "id_disciplina": 2,
      "descricao": "Aula de Física",
      "tipo_reserva": "diaria",
      "data": "2026-05-21",
      "horario_inicio": "10:00:00",
      "horario_fim": "12:00:00"
    }
  }
}
```

**Exemplo de Requisição:**
```bash
curl -X GET "ServerUrl/reservas"
```

---

### GET /reservas/{id_reserva}

Obtém os detalhes de uma reserva específica.

**Parâmetros:**
- `id_reserva` (path, obrigatório): ID da reserva

**Response (200 - Sucesso):**
```json
{
  "sucesso": true,
  "reserva": {
    "id_sala": 201,
    "id_disciplina": 1,
    "descricao": "Aula de Matemática",
    "tipo_reserva": "diaria",
    "data": "2026-05-20",
    "horario_inicio": "08:00:00",
    "horario_fim": "10:00:00"
  }
}
```

**Response (404 - Reserva não encontrada):**
```json
{
  "sucesso": false,
  "mensagem": "Reserva não encontrada"
}
```

**Exemplo de Requisição:**
```bash
curl -X GET "http://ServerURL/reservas/1"
```

---

### DELETE /reservas/{id_reserva}

Cancela uma reserva existente.

**Parâmetros:**
- `id_reserva` (path, obrigatório): ID da reserva

**Response (200 - Sucesso):**
```json
{
  "sucesso": true,
  "mensagem": "Reserva cancelada com sucesso",
  "reserva_removida": {
    "id_sala": 201,
    "id_disciplina": 1,
    "descricao": "Aula de Matemática",
    "tipo_reserva": "diaria",
    "data": "2026-05-20",
    "horario_inicio": "08:00:00",
    "horario_fim": "10:00:00"
  }
}
```

**Response (404 - Reserva não encontrada):**
```json
{
  "sucesso": false,
  "mensagem": "Reserva não encontrada"
}
```

**Exemplo de Requisição:**
```bash
curl -X DELETE "ServerURL/reservas/1"
```

---

## Usuários

### POST /usuarios

Cria um novo usuário no sistema.

**Request Body:**
```json
{
  "nome": "string (mínimo 3 caracteres)",
  "email": "string (formato válido e único)",
  "senha": "string (mínimo 6 caracteres)",
  "tipo": "aluno|professor|coordenador"
}
```

**Validações:**
- `nome`: Mínimo 3 caracteres, espaços removidos
- `email`: Deve ser válido (conter @ e .), será convertido para minúsculas, deve ser único
- `senha`: Mínimo 6 caracteres
- `tipo`: Apenas valores "aluno", "professor" ou "coordenador"

**Exemplo de Requisição:**
```bash
curl -X POST "ServerURL/usuarios" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao.silva@universidade.com",
    "senha": "senha123",
    "tipo": "professor"
  }'
```

**Response (200 - Sucesso):**
```json
{
  "sucesso": true,
  "mensagem": "Usuário criado com sucesso",
  "id_usuario": 1,
  "usuario": {
    "id_usuario": 1,
    "nome": "João Silva",
    "email": "joao.silva@universidade.com",
    "tipo": "professor",
    "created_at": "2026-05-15T10:30:45.123456"
  }
}
```

**Response (409 - Email já cadastrado):**
```json
{
  "sucesso": false,
  "mensagem": "Email já cadastrado"
}
```

**Response (422 - Validação falhou):**
```json
{
  "detail": [
    {
      "loc": ["body", "nome"],
      "msg": "Nome deve ter pelo menos 3 caracteres",
      "type": "value_error"
    }
  ]
}
```

---

### GET /usuarios

Lista todos os usuários cadastrados.

**Parâmetros:** Nenhum

**Response (200 - Sucesso):**
```json
{
  "sucesso": true,
  "total": 2,
  "usuarios": [
    {
      "id_usuario": 1,
      "nome": "João Silva",
      "email": "joao.silva@universidade.com",
      "tipo": "professor",
      "created_at": "2026-05-15T10:30:45.123456"
    },
    {
      "id_usuario": 2,
      "nome": "Maria Santos",
      "email": "maria.santos@universidade.com",
      "tipo": "aluno",
      "created_at": "2026-05-15T10:35:20.654321"
    }
  ]
}
```

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:8000/usuarios"
```

---

### GET /usuarios/{id_usuario}

Obtém os detalhes de um usuário específico.

**Parâmetros:**
- `id_usuario` (path, obrigatório): ID do usuário

**Response (200 - Sucesso):**
```json
{
  "sucesso": true,
  "usuario": {
    "id_usuario": 1,
    "nome": "João Silva",
    "email": "joao.silva@universidade.com",
    "tipo": "professor",
    "created_at": "2026-05-15T10:30:45.123456"
  }
}
```

**Response (404 - Usuário não encontrado):**
```json
{
  "sucesso": false,
  "mensagem": "Usuário não encontrado"
}
```

**Exemplo de Requisição:**
```bash
curl -X GET "ServerURL/usuarios/1"
```

---

### DELETE /usuarios/{id_usuario}

Remove um usuário do sistema.

**Parâmetros:**
- `id_usuario` (path, obrigatório): ID do usuário

**Response (200 - Sucesso):**
```json
{
  "sucesso": true,
  "mensagem": "Usuário deletado com sucesso",
  "usuario_removido": {
    "id_usuario": 1,
    "nome": "João Silva",
    "email": "joao.silva@universidade.com"
  }
}
```

**Response (404 - Usuário não encontrado):**
```json
{
  "sucesso": false,
  "mensagem": "Usuário não encontrado"
}
```

**Exemplo de Requisição:**
```bash
curl -X DELETE "http://localhost:8000/usuarios/1"
```

---

## Códigos de Status HTTP

| Código | Significado |
|--------|-------------|
| **200** | Sucesso na requisição |
| **401** | Autenticação falhou (credenciais inválidas) |
| **404** | Recurso não encontrado |
| **409** | Conflito (email duplicado, horário indisponível) |
| **422** | Validação falhou (dados inválidos) |

---

## Salas Disponíveis

As salas atualmente disponíveis no sistema são:
- **201**
- **202**
- **204**

---

## Observações Gerais

1. Todos os horários devem estar no formato **HH:MM:SS**
2. Todas as datas devem estar no formato **YYYY-MM-DD**
3. Emails são salvos em **minúsculas**
4. Nomes têm **espaços extras removidos**
5. As senhas são armazenadas em **texto plano** (será implementado hash quando integrado ao banco de dados) 
6. A detecção de conflitos funciona apenas para reservas do tipo **"diaria"**
7. Todos os responses incluem um campo `sucesso` indicando se a operação foi bem-sucedida
