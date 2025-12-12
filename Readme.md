# Twitter Clone Fullstack (Monorepo Django + React)

> Repositório monolítico com backend em Django REST Framework e frontend em React (Vite). Pensado para deploy no Render.com — backend como Web Service (gunicorn) e frontend como Static Site (Vite build).

---

## Estrutura do projeto

```
/twitter_clone/
├─ backend/
│  ├─ manage.py
│  ├─ backend/
│  │  ├─ __init__.py
│  │  ├─ settings.py
│  │  ├─ urls.py
│  │  └─ wsgi.py
│  └─ api/
│     ├─ __init__.py
│     ├─ admin.py
│     ├─ apps.py
│     ├─ models.py
│     ├─ serializers.py
│     ├─ views.py
│     ├─ urls.py
│     ├─ permissions.py
│     └─ migrations/
├─ frontend/
│  ├─ package.json
│  ├─ vite.config.js
│  ├─ index.html
│  └─ src/
│     ├─ main.jsx
│     ├─ App.jsx
│     ├─ api.js
│     └─ components/
│        ├─ Login.jsx
│        ├─ Register.jsx
│        ├─ Navbar.jsx
│        ├─ Feed.jsx
│        ├─ PostForm.jsx
│        ├─ Post.jsx
│        ├─ Profile.jsx
│        └─ ProfileEdit.jsx
├─ render.yaml
├─ docker-compose.yml
├─ requirements.txt
└─ README.md
```

---

## O que eu adicionei (visão geral)

- **Backend**:
  - Autenticação com Token (DRF TokenAuth)
  - Endpoints para: registro, login, perfil (ver/editar), criar/ler/deletar post, curtir, comentar, seguir/desseguir, feed de quem você segue
  - Models: `Profile`, `Post`, `Like`, `Comment`, `Follow`
  - Serializers completos para cada modelo
  - Permissões: apenas autores podem deletar seus posts, endpoints protegidos por token
  - Config pronto para PostgreSQL via `DATABASE_URL` (usa `dj_database_url`)
  - `collectstatic` e `ALLOWED_HOSTS` configuráveis via env vars

- **Frontend (React + Vite)**:
  - Login e Registro com chamadas à API
  - Feed que mostra posts das pessoas que o usuário segue
  - Criar post (`PostForm`)
  - Curtir/Descurtir, comentar (UI básica)
  - Perfil com edição (avatar URL, nome, senha opcional)
  - Armazenamento do token no `localStorage` e `api.js` para centralizar chamadas

- **Infra / Deploy**:
  - `render.yaml` para deploy infra-as-code no Render (opcional)
  - `docker-compose.yml` para ambiente local com Postgres

- **Testes & Segurança**:
  - Exemplo de testes básicos com `django.test`
  - Sugestões de melhorias (JWT, rate limiting, armazenamento de mídia)

---

## README.md (completo)

# Twitter Clone — Monorepo (Django + React)

Este repositório contém um clone simplificado do Twitter com back-end em Django REST Framework e front-end em React (Vite). O projeto foi pensado para deploy no Render.com (backend: Web Service, frontend: Static Site).

### Principais features
- Autenticação (registro/login) com Token
- Perfil do usuário (avatar, bio, senha)
- Seguir / deixar de seguir
- Feed apenas com posts de quem você segue
- Curtidas e comentários em posts

---

## Requisitos
- Python 3.10+
- Node 16+
- PostgreSQL (recomendado em produção)
- Conta no Render.com (para deploy)

---

## Rodando localmente (modo rápido)

### 1) Backend (com SQLite - modo rápido)

```bash
# na raiz do repo
python -m venv venv
source venv/bin/activate  # mac/linux
# windows: venv/Scripts/activate
pip install -r requirements.txt
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
A API ficará em `http://localhost:8000/api/`.

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```
A UI Vite estará em `http://localhost:5173` por padrão.

---

## Configurar Postgres local com docker-compose (recomendado para testar produção localmente)

Arquivo `docker-compose.yml` (exemplo incluído neste repo). Para subir:

```bash
docker-compose up -d
# depois, configure DATABASE_URL no .env por exemplo:
# DATABASE_URL=postgres://postgres:postgres@db:5432/twitter_clone_db
```

---

## Deploy no Render.com — passo a passo

### Backend (Web Service)

1. No Render: New -> Web Service
2. Conecte o repositório e selecione a branch `main`
3. Runtime: Python 3.x
4. Build Command:

```bash
pip install -r requirements.txt && python backend/manage.py migrate --noinput && python backend/manage.py collectstatic --noinput
```

5. Start Command:

```bash
gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
```

6. Environment:
- `SECRET_KEY` — string segura
- `DATABASE_URL` — URL do Postgres criado no Render ou outro serviço (ex.: `postgres://user:pass@host:5432/dbname`)
- `DEBUG=false`
- `ALLOWED_HOSTS` — o domínio do serviço (ex.: `my-twitter-clone.onrender.com`)

7. Adicionar um serviço Postgres no Render (Add -> Database) e copiar a `DATABASE_URL` para o backend.

### Frontend (Static Site)

1. No Render: New -> Static Site
2. Conecte o repositório e selecione branch `main`
3. Build Command: `cd frontend && npm install && npm run build`
4. Publish Directory: `frontend/dist`
5. Se usar variáveis como `VITE_API_URL` configure-as em `Environment` no Render e use `import.meta.env.VITE_API_URL` no frontend.

---

## Arquivos já incluídos / gerados para facilitar deploy

### render.yaml (opcional, infra-as-code)

```yaml
services:
  - type: web
    name: twitter-clone-backend
    env: python
    plan: free
    repo: <seu-repo-git>
    branch: main
    buildCommand: "pip install -r requirements.txt && python backend/manage.py migrate --noinput && python backend/manage.py collectstatic --noinput"
    startCommand: "gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT"
    envVars:
      - key: SECRET_KEY
        sync: false
      - key: DATABASE_URL
        sync: false
      - key: DEBUG
        value: "false"

staticSites:
  - name: twitter-clone-frontend
    repo: <seu-repo-git>
    branch: main
    buildCommand: "cd frontend && npm install && npm run build"
    publishPath: frontend/dist
```

> Substitua `<seu-repo-git>` pelo URL do seu GitHub (opcional — render aceita configurar via UI também).

---

## docker-compose.yml (para rodar Postgres localmente)

```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_DB: twitter_clone_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

**Como usar:** Suba `docker-compose up -d`, depois configure `DATABASE_URL=postgres://postgres:postgres@localhost:5432/twitter_clone_db` no `.env` e rode `python manage.py migrate`.

---

## Testes básicos (exemplo de `backend/api/tests.py`)

```python
from django.test import TestCase
from django.contrib.auth.models import User

class SimpleAuthTest(TestCase):
    def test_register_and_login(self):
        res = self.client.post('/api/register/', {'username':'tuser','password':'123456'})
        self.assertEqual(res.status_code, 200)
        token = res.json().get('token')
        self.assertTrue(token)
        res2 = self.client.post('/api/login/', {'username':'tuser','password':'123456'})
        self.assertEqual(res2.status_code, 200)
```

Rode `python manage.py test` para executar os testes.

---

## Melhorias de segurança e produção sugeridas

- Trocar `TokenAuth` por JWT (`djangorestframework-simplejwt`) se quiser expiração/refresh.
- Configurar `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` quando usar HTTPS.
- Usar `django-storages` + S3 (ou Spaces) para armazenar uploads de avatar/perfil.
- Configurar `ALLOWED_HOSTS` estrito, `DEBUG=False` e rotinas de rotação de `SECRET_KEY` fora do código.
- Habilitar rate limit (ex.: `django-ratelimit`) para endpoints de autenticação.

---

## Como gerar um ZIP do projeto (localmente)

Na raiz do repo:

```bash
zip -r twitter_clone.zip . -x "**/node_modules/**" "**/venv/**" "**/__pycache__/**"
```

---

## Código frontend adicional (exemplo: `frontend/src/api.js`)

```js
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export async function api(path, method='GET', body=null, token=null){
  const headers = {'Content-Type': 'application/json'};
  if(token) headers['Authorization'] = `Token ${token}`;
  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null
  });
  return res.json();
}
```






