# SIGEA - Sistema de Gerenciamento de Espaços Acadêmicos

##  Visão Geral da Estrutura do Projeto

Este projeto é uma **API REST em FastAPI** integrada com **PostgreSQL**, desenvolvida para gerenciar salas, reservas, usuários, disciplinas e eventos em uma instituição acadêmica.

### Estrutura de Pastas

```
Project-Sigea/
├── SIGEA/
│   ├── __init__.py
│   ├── main.py                 # Arquivo principal da aplicação
│   ├── schemas.py              # Modelos Pydantic (validação de dados)
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py           # Modelos SQLAlchemy (tabelas do banco)
│   ├── database/
│   │   └── settings.py         # Configuração do banco PostgreSQL
│   └── routes/
│       └── routes.py           # Todas as rotas da API
├── requirements.txt            # Dependências Python
├── .env.example               # Exemplo de variáveis de ambiente
└── README.md                  # Este arquivo
```

---

## Instalação e Configuração

### 1. **Instalar Dependências**

```bash
pip install -r requirements.txt
```

### 2. **Configurar o PostgreSQL**

Crie um banco de dados PostgreSQL:

```sql
CREATE DATABASE sigea;
```

### 3. **Configurar Variáveis de Ambiente**

Copie `.env.example` para `.env` e configure:

```bash
cp .env.example .env
```

Edite `.env` com suas credenciais:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/sigea
```

### 4. **Executar a Aplicação**

```bash
python -m SIGEA.main
```

A API estará disponível em: **http://localhost:8000**

---

##  Rotas Principais

### **Base de Todas as Rotas**
```
/api
```

### **1. USUÁRIOS** 👥

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/usuarios` | Lista todos os usuários |
| POST | `/usuarios` | Cria novo usuário |

**GET - Listar Usuários:**
```bash
curl -X GET http://localhost:8000/api/usuarios
```

**Response:**
```json
[
  {
    "id_usuario": 1,
    "nome": "João Silva",
    "email": "joao@email.com",
    "tipo": "professor"
  }
]
```

**POST - Criar Usuário:**
```bash
curl -X POST http://localhost:8000/api/usuarios \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@email.com",
    "senha": "senha123",
    "tipo": "professor"
  }'
```

**Request Body:**
```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "senha": "senha123",
  "tipo": "professor"
}
```

**Response:**
```json
{
  "id_usuario": 1,
  "nome": "João Silva",
  "email": "joao@email.com",
  "tipo": "professor"
}
```

Tipos válidos: `aluno`, `professor`, `coordenador`
  "descricao": "Aula de Programação",
  "id_sala": 1,
  "id_usuario": 1,
  "id_disciplina": 1
}
```

**Validações Automáticas:**
- ✅ Data de fim deve ser **depois** da data de início
- ✅ Detecta **conflito de horários** automaticamente
- ✅ Verifica existência de usuário e sala

---

### **7. EVENTOS** 🎉 ⭐ ROTA PRINCIPAL

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/eventos` | Lista todos os eventos |
| POST | `/eventos` | Cria novo evento |
| GET | `/eventos/{evento_id}` | Obtém evento por ID |
| POST | `/eventos/{evento_id}/participar` | Usuário participa do evento |

**POST - Criar Evento:**
```json
{
  "titulo": "Semana da Programação",
  "descricao": "Uma semana dedicada à programação",
  "data_inicio": "2026-06-01T08:00:00",
  "data_fim": "2026-06-01T18:00:00",
  "tipo": "institucional",
  "destaque": true,
  "id_sala": 1,
  "id_usuario": 1
}
```

---

## 📊 Modelos de Dados

### **Usuario**
```python
- id_usuario (INT, PK)
- nome (VARCHAR 100)
- email (VARCHAR 150, UNIQUE)
- senha (TEXT)
- tipo (ENUM: aluno, professor, coordenador)
- created_at (TIMESTAMP)
```

### **Andar**
```python
- id_andar (INT, PK)
- numero (INT)
```

### **Sala**
```python
- id_sala (INT, PK)
- nome (VARCHAR 50)
- capacidade (INT)
- tipo (VARCHAR 50)
- status (ENUM: ativa, manutencao)
- horario_inicio (TIME)
- horario_fim (TIME)
- id_andar (INT, FK)
```

---

## 🔌 Como Integrar com o Front-End

### **1. URLs Base**
```javascript
const API_BASE = "http://localhost:8000/api";
```

### **2. Exemplo de Requisição (JavaScript)**

```javascript
// Listar Usuários
async function getUsuarios() {
  const response = await fetch(`${API_BASE}/usuarios`);
  return await response.json();
}

// Criar Usuário
async function criarUsuario(data) {
  const response = await fetch(`${API_BASE}/usuarios`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  return await response.json();
}
```

---

## 🧪 Testando a API

### **Com cURL:**

```bash
# Listar Usuários
curl http://localhost:8000/api/usuarios

# Criar Usuário
curl -X POST http://localhost:8000/api/usuarios \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@email.com",
    "senha": "senha123",
    "tipo": "professor"
  }'
```

### **Com Postman:**
1. Acesse: `http://localhost:8000/docs` (Swagger UI interativo)

---

## 📝 Notas Importantes

- A API usa **PostgreSQL** (não SQLite)
- Todas as rotas estão disponíveis sem autenticação para facilitar o desenvolvimento local
- A API retorna códigos HTTP apropriados (200, 201, 400, etc)

---

## 🤝 Suporte

Para dúvidas ou problemas, consulte a documentação interativa em:
```
http://localhost:8000/docs
```

