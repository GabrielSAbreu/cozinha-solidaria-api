# 🍲 Cozinha Solidária API

API RESTful para o gerenciamento de uma **Cozinha Solidária**, responsável pela gestão de cursos de capacitação, usuários, benefícios e controle de acesso por papéis.

Este projeto faz parte do **MVP da Sprint II** da Pós-Graduação em Desenvolvimento Full Stack.

## 💡 Sobre o Projeto

A **Cozinha Solidária** atua em duas frentes principais:

1. **Capacitação profissional:** oferta de cursos e oficinas para alunos da comunidade.
2. **Assistência social:** distribuição organizada de refeições e benefícios.

A API fornece endpoints para cadastro, autenticação e gerenciamento dessas operações, com controle de acesso hierárquico (**RBAC**) para ações administrativas.

O frontend será mantido em outro repositório. O `docker-compose` da solução completa ficará nesse repositório do frontend, enquanto esta API pode ser executada individualmente.

## 🛠️ Tecnologias

- **Linguagem:** Python 3.12+
- **Framework web:** FastAPI
- **Servidor ASGI:** Uvicorn
- **ORM:** SQLAlchemy
- **Banco de dados:** SQLite
- **Validação:** Pydantic e `email-validator`
- **Containerização:** Docker

## 📁 Estrutura do Projeto

```text
cozinha-solidaria-api/
├── database/                 # Banco SQLite
├── model/                    # Modelos SQLAlchemy e configuração do banco
│   ├── __init__.py           # Conexão, sessão e criação do usuário Root
│   ├── base.py               # Declarative Base
│   ├── usuario.py            # Modelo de usuário
│   ├── curso.py              # Modelo de curso
│   ├── beneficio.py          # Modelo de benefício
│   ├── cursa.py              # Relacionamento de inscrição
│   └── recebe.py             # Relacionamento de benefícios
├── schema/                   # Schemas Pydantic
│   ├── __init__.py
│   ├── usuario.py            # Schemas de usuário
│   ├── curso.py              # Schemas de curso
│   └── beneficio.py          # Schemas de benefício
├── routes/                   # Rotas e regras de acesso
│   ├── __init__.py
│   ├── usuario_route.py      # Autenticação e usuários
│   ├── curso_route.py        # Cursos
│   ├── beneficio_route.py    # Benefícios
│   └── permissions.py        # Dependências de permissão
├── app.py                    # Instância principal do FastAPI
├── dockerfile                # Imagem Docker da API
├── .dockerignore             # Arquivos ignorados pelo Docker
├── requirements.txt          # Dependências Python
└── README.md                 # Documentação
```

## 🔐 Controle de Acesso

| Perfil | Permissões |
|---|---|
| `root` | Acesso total. Único perfil autorizado a excluir registros e usuário padrão inicial do sistema. |
| `admin` | Pode criar e editar cursos e benefícios, além de criar administradores. Não pode excluir registros. |
| `aluno` | Pode consultar cursos e realizar inscrições, conforme as rotas disponíveis. |
| `beneficiario` | Pode consultar benefícios e refeições disponíveis. |

As rotas administrativas utilizam o cabeçalho HTTP:

```http
X-User-Id: 1
```

## 👤 Usuário Root Inicial

Na inicialização, a API verifica se existe um usuário com o perfil `root`. Caso não exista, cria automaticamente:

```text
E-mail: root@cozinhasolidaria.org
Senha: root123
```

Essas credenciais são destinadas apenas ao ambiente inicial de desenvolvimento e devem ser alteradas em um ambiente real.

## 🚀 Execução Local

### Pré-requisitos

- Python 3.12 ou superior
- `pip`

### Linux e macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

O banco SQLite será criado ou atualizado em `database/cozinha_solidaria.db`.

## 🐳 Execução Individual com Docker

O `dockerfile` permite executar somente a API, sem depender do frontend.

### Construir a imagem

```bash
docker build -f dockerfile -t cozinha-solidaria-api .
```

### Iniciar o container

Linux e macOS:

```bash
docker run -d \
  --name api_container \
  -p 8000:8000 \
  -v "$(pwd)/database:/app/database" \
  cozinha-solidaria-api
```

Windows PowerShell:

```powershell
docker run -d `
  --name api_container `
  -p 8000:8000 `
  -v "${PWD}/database:/app/database" `
  cozinha-solidaria-api
```

O volume mantém o banco SQLite no diretório `database/` do projeto.

## 📖 Documentação da API

Com a aplicação em execução, acesse:

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

## 📌 Endpoints Principais

### Usuários

| Método | Endpoint | Descrição |
|---|---|---|
| `POST` | `/usuarios` | Cadastro público de alunos ou beneficiários. |
| `POST` | `/usuarios/admin` | Criação de administrador com `X-User-Id`. |
| `POST` | `/usuarios/login` | Login por e-mail e senha. |
| `GET` | `/usuarios` | Lista todos os usuários. |
| `GET` | `/usuarios/{id_usuario}` | Busca um usuário por ID. |

### Cursos

| Método | Endpoint | Permissão |
|---|---|---|
| `GET` | `/cursos` | Público. |
| `GET` | `/cursos/{id_curso}` | Público. |
| `POST` | `/cursos` | `root` ou `admin`. |
| `PUT` | `/cursos/{id_curso}` | `root` ou `admin`. |
| `DELETE` | `/cursos/{id_curso}` | Somente `root`. |

### Benefícios

| Método | Endpoint | Permissão |
|---|---|---|
| `GET` | `/beneficios` | Público. |
| `GET` | `/beneficios/{id_beneficio}` | Público. |
| `POST` | `/beneficios` | `root` ou `admin`. |
| `PUT` | `/beneficios/{id_beneficio}` | `root` ou `admin`. |
| `DELETE` | `/beneficios/{id_beneficio}` | Somente `root`. |

## 🔗 Integração com o Frontend

Quando a API for executada separadamente, utilize a URL base:

```text
http://localhost:8000
```

No ambiente integrado, o repositório do frontend será responsável por:

- manter o `docker-compose` da solução;
- configurar os serviços da aplicação;
- definir as variáveis de ambiente;
- apontar o frontend para a URL da API.

Ao executar frontend e backend em origens diferentes, configure CORS conforme o ambiente de desenvolvimento ou produção.

## ⚙️ Comandos Úteis do Docker

```bash
# Ver logs
docker logs api_container

# Parar o container
docker stop api_container

# Iniciar novamente o container
docker start api_container

# Remover o container
docker rm -f api_container
```
