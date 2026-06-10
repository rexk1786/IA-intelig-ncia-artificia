# PharmaCore ERP 🏥

Um sistema profissional de gestão de farmácia com API REST, autenticação JWT, auditoria completa e relatórios analíticos.

## 📋 Funcionalidades

### ✅ MVP (Fase 1)
- **Gestão de Utilizadores**: Login, Registo, Perfis (Admin, Farmacêutico, Caixa)
- **Autenticação JWT**: Segurança em endpoints
- **Gestão de Medicamentos**: CRUD completo com validações
- **Gestão de Stock**: Entradas, saídas, alertas
- **Sistema de Vendas**: Com transações ACID
- **Auditoria**: Rastreabilidade completa de ações
- **Testes Automatizados**: Cobertura >80%

### 🚀 Futuras Melhorias (Fase 2)
- Relatórios avançados (Medicamentos mais vendidos, Lucro mensal, etc.)
- Dashboard analytics
- Integração com sistemas de pagamento
- Backup automático

## 🛠️ Stack Tecnológico

**Backend**
- Python 3.11+
- FastAPI
- SQLAlchemy ORM
- Pydantic
- PostgreSQL

**Segurança**
- JWT (python-jose)
- bcrypt (password hashing)
- CORS middleware

**Qualidade**
- pytest (testes)
- black, isort, flake8 (code style)
- pytest-cov (cobertura)

**DevOps**
- Docker & docker-compose
- GitHub Actions (CI/CD)
- Git workflow

## 📁 Estrutura do Projeto

```
pharmacore/
├── app/
│   ├── models/           # SQLAlchemy models
│   ├── repositories/     # Data access layer
│   ├── services/         # Business logic
│   ├── routes/          # API endpoints
│   ├── middleware/      # Middleware customizado
│   ├── schemas/         # Pydantic schemas
│   └── utils/           # Utilities (logger, security, etc)
├── database/            # Database config
├── tests/               # Unit + Integration tests
├── docs/                # Documentação
├── logs/                # Application logs
├── .github/workflows/   # CI/CD pipelines
├── main.py              # Entry point
├── config.py            # Configurações
├── requirements.txt     # Dependências
├── docker-compose.yml   # Docker setup
└── .env.example         # Template de env vars
```

## 🚀 Quick Start

### Com Docker (Recomendado)
```bash
# Clone o repositório
git clone https://github.com/rexk1786/IA-intelig-ncia-artificia.git
cd pharmacore

# Configure o .env
cp .env.example .env

# Inicie os serviços
docker-compose up -d

# Os testes rodam automaticamente
docker-compose run app pytest

# API estará em http://localhost:8000
```

### Setup Local
```bash
# Python 3.11+
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais PostgreSQL

# Rode testes
pytest

# Inicie o servidor
python main.py
```

## 📚 Documentação

- [Setup Detalhado](./docs/SETUP.md)
- [Arquitetura](./docs/ARCHITECTURE.md)
- [API Reference](./docs/API.md)
- [Testing Guide](./docs/TESTING.md)

## 🔐 Endpoints Principais

### Autenticação
- `POST /auth/register` - Registar novo utilizador
- `POST /auth/login` - Login (retorna JWT)
- `POST /auth/refresh` - Renovar token

### Medicamentos
- `GET /medications` - Listar medicamentos
- `POST /medications` - Criar medicamento
- `GET /medications/{id}` - Obter detalhes
- `PUT /medications/{id}` - Atualizar
- `DELETE /medications/{id}` - Apagar

### Vendas
- `POST /sales` - Criar venda (com transação)
- `GET /sales` - Listar vendas
- `GET /sales/{id}` - Detalhes da venda

### Stock
- `GET /stock` - Estado do stock
- `POST /stock/entry` - Entrada de stock
- `POST /stock/exit` - Saída de stock

### Auditoria
- `GET /audit-logs` - Histórico de ações
- `GET /audit-logs/user/{user_id}` - Ações por utilizador

## 🧪 Testes

```bash
# Rodar todos os testes
pytest

# Com cobertura
pytest --cov=app --cov-report=html

# Testes específicos
pytest tests/unit/test_auth_service.py
pytest tests/integration/test_api_sales.py

# Watch mode
ptw
```

## 👤 Autenticação

Todos os endpoints (exceto `/auth/register` e `/auth/login`) requerem header:
```
Authorization: Bearer <seu_jwt_token>
```

## 🔧 Configuração

Veja `.env.example` para todas as variáveis disponíveis:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/pharmacore
JWT_SECRET_KEY=sua-chave-secreta-super-segura
JWT_ALGORITHM=HS256
ENVIRONMENT=development
```

## 📊 O Que Impressiona Recrutadores

1. ✅ **Transações ACID** - Vendas com rollback automático
2. ✅ **Auditoria Completa** - Rastreamento de quem fez cada ação
3. ✅ **Testes Automatizados** - >80% de cobertura
4. ✅ **Logging Estruturado** - Rastreamento de erros
5. ✅ **Type Hints** - Python profissional
6. ✅ **Docker** - Pronto para produção
7. ✅ **CI/CD** - GitHub Actions automático
8. ✅ **Documentação** - API self-documenting (FastAPI)

## 🤝 Contributing

Este projeto segue gitflow:
- `main` - Versão estável
- `develop` - Desenvolvimento ativo
- `feature/*` - Novas funcionalidades

## 📝 Licença

MIT

## 👨‍💻 Autor

**rexk1786** - [GitHub](https://github.com/rexk1786)

---

**Desenvolvido com ❤️ para impressionar recrutadores**
