# SIGEA — Sistema Integrado de Gestão de Espaços Acadêmicos

## Visão geral

O SIGEA é uma plataforma web desenvolvida para centralizar o gerenciamento de espaços acadêmicos, como salas, laboratórios, reservas, eventos e disciplinas. O sistema foi pensado para melhorar a organização institucional, reduzir conflitos de horário e facilitar a consulta de disponibilidade de ambientes por usuários autorizados.

A proposta do projeto é oferecer uma solução simples, clara e eficiente para o contexto acadêmico, permitindo que administradores, professores, coordenadores e alunos acessem informações de forma padronizada e segura.

## Proposta do projeto

Em instituições de ensino, a gestão de espaços físicos costuma envolver processos manuais, descentralizados ou pouco integrados. Isso pode gerar sobreposição de horários, dificuldade na consulta de salas disponíveis, falta de visibilidade sobre a ocupação dos ambientes e retrabalho administrativo.

O SIGEA surge como uma resposta a esse cenário, propondo uma aplicação capaz de:

* centralizar o cadastro e a consulta de espaços acadêmicos;
* permitir reservas de salas por usuários autorizados;
* controlar conflitos de horário automaticamente;
* registrar e listar eventos institucionais;
* disponibilizar a agenda do usuário e a agenda geral do sistema;
* oferecer uma experiência de uso mais intuitiva e organizada.

## Objetivos

### Objetivo geral

Desenvolver uma plataforma para gestão de espaços acadêmicos que centralize informações, facilite reservas e melhore a organização do uso dos ambientes institucionais.

### Objetivos específicos

* Permitir o cadastro e gerenciamento de usuários;
* Controlar o cadastro de andares e salas;
* Possibilitar a criação, validação e cancelamento de reservas;
* Evitar conflitos de horário automaticamente;
* Permitir o cadastro e a consulta de eventos;
* Disponibilizar consulta de disponibilidade, status e agenda;
* Permitir a associação entre usuários e disciplinas;
* Melhorar a transparência e a comunicação sobre ocupação dos espaços.

## Escopo funcional

O sistema contempla os seguintes módulos principais:

* Autenticação de usuários
* Cadastro e gerenciamento de usuários
* Cadastro e gerenciamento de andares
* Cadastro e gerenciamento de salas
* Definição de horários de alocação
* Cadastro e gerenciamento de disciplinas
* Associação entre usuários e disciplinas
* Criação, validação e cancelamento de reservas
* Consulta de disponibilidade de salas
* Visualização de status das salas
* Cadastro, listagem e participação em eventos
* Consulta de agenda individual e agenda geral
* Busca e filtros de salas
* Exibição de localização das salas

## Requisitos funcionais considerados

O projeto foi estruturado com base nos requisitos funcionais definidos na documentação:

* RF01 — Cadastro de Usuários
* RF02 — Autenticação de Usuários
* RF03 — Gerenciamento de Perfis
* RF04 — Cadastro de Andares
* RF05 — Cadastro de Salas
* RF06 — Definição de Horário de Alocação
* RF07 — Cadastro de Disciplinas
* RF08 — Associação Usuário-Disciplina
* RF09 — Criação de Reservas
* RF10 — Validação de Conflito de Horário
* RF11 — Consulta de Disponibilidade de Salas
* RF12 — Visualização de Status das Salas
* RF13 — Visualização de Agenda do Usuário
* RF14 — Cancelamento de Reservas
* RF15 — Cadastro de Eventos
* RF16 — Listagem de Eventos
* RF17 — Participação em Eventos
* RF18 — Filtros e Busca de Salas
* RF19 — Exibição de Localização da Sala
* RF20 — Visualização de Agenda Geral

## Requisitos não funcionais

* Autenticação segura com JWT;
* Controle de permissão para alteração e cancelamento de reservas;
* Tempo de resposta inferior a 2 segundos para consultas de disponibilidade;
* Acesso via navegador web.

## Tecnologias utilizadas

* Backend: Python e FastAPI
* Frontend: Next.js + React
* Banco de dados: PostgreSQL
* Arquitetura: MVC
* Outras ferramentas: Trello, Figma e Visual Studio Code

## Estrutura do projeto

A estrutura segue a lógica da arquitetura MVC, separando responsabilidades entre camadas de aplicação.

Exemplo de organização:

```bash
src/
├── controllers/
├── models/
├── routes/
├── schemas/
├── services/
├── database/
└── main.py
```

## API

A API foi pensada de forma REST, com rotas organizadas por domínio. Exemplos de grupos de rotas:

* `/auth`
* `/usuarios`
* `/andares`
* `/salas`
* `/disciplinas`
* `/reservas`
* `/eventos`
* `/agenda`

## Exemplo de respostas mockadas da API

Abaixo estão exemplos de respostas simuladas para representar o formato esperado dos dados.

### Login

```json
{
  "email": "usuario@email.com",
  "sessao": "autenticada"
}
```

### Cadastro de usuário

```json
{
  "usuario": {
    "id": 1,
    "nome": "Nome",
    "email": "email@email.com",
    "tipo": "professor"
  }
}
```

### Cadastro de sala

```json
{
  "sala": {
    "id": 1,
    "nome": "Sala 1",
    "capacidade": 30,
    "tipo": "sala",
    "id_andar": 1
  }
}
```

### Criação de reserva

```json
{
  "reserva": {
    "id": 1,
    "id_sala": 1,
    "id_disciplina": 1,
    "data_inicio": "2026-04-10 08:00",
    "data_fim": "2026-04-10 10:00",
    "descricao": "Aula"
  }
}
```

### Cadastro de evento

```json
{
  "evento": {
    "id": 1,
    "titulo": "Evento",
    "descricao": "Descricao",
    "id_sala": 1,
    "data_inicio": "2026-05-01 08:00",
    "data_fim": "2026-05-01 10:00",
    "tipo": "institucional"
  }
}
```

### Agenda do usuário

```json
{
  "id_usuario": 1,
  "reservas": [
    {
      "id": 1,
      "id_sala": 1,
      "data_inicio": "2026-04-10 08:00",
      "data_fim": "2026-04-10 10:00"
    }
  ],
  "eventos": [
    {
      "id": 1,
      "titulo": "Evento",
      "data_inicio": "2026-05-01 08:00",
      "data_fim": "2026-05-01 10:00"
    }
  ]
}
```

## Status do projeto

Projeto em desenvolvimento.

## Contribuidores

* Fillype Amorim
* Guilherme Bispo
* Kenzo Senna
* Leonardo Franco de Almeida
* Luísa de Matos
* Matheus Camarotto
* Matheus Silva
* Nicolas Wolf
* Vinícius Lourençon
* Jonathan Patrocinio Dos Santos

## Referências

* FastAPI Documentation
* Next.js Documentation
* React Documentation
* RFC 7519 — JSON Web Token (JWT)
* Manifesto Ágil
* UML Specification
