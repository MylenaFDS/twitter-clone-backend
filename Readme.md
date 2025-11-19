# Twitter Clone

Projeto clone funcional do Twitter com backend em Django REST Framework e frontend em React.

---

## Tecnologias

- **Backend:** Python, Django, Django REST Framework, Djoser (JWT Auth)
- **Frontend:** React
- **Banco de dados:** SQLite local / PostgreSQL no deploy
- **Deploy:** Render.com

---

## Estrutura do projeto

twitter_clone/ ├── backend/ # Backend Django │ ├── manage.py │ ├── requirements.txt │ ├── twitter_clone/ # Configurações do projeto Django │ └── api/ # App Django com models, views, serializers, urls └── frontend/ # Frontend React ├── package.json ├── public/ └── src/


---

## Configuração local

### Backend (Django)

1. Navegue até a pasta backend:

```bash
cd backend

```
2. Crie e ative um ambiente virtual:
Linux/macOS:

python3 -m venv venv
source venv/bin/activate

Windows PowerShell:

python -m venv venv
.\venv\Scripts\activate

3. Instale as dependências:

pip install -r requirements.txt

4. Rode as migrations e crie o superusuário: 

python manage.py migrate
python manage.py createsuperuser

5. Inicie o servidor Django:

python manage.py runserver

O backend estará disponível em http://localhost:8000/

#### Frontend (React)
1. Navegue até a pasta frontend:

cd ../frontend

2. Instale as dependências:

npm install

3. Configure a URL base da API para apontar para o backend local.
Crie um arquivo .env na pasta frontend com o conteúdo:

REACT_APP_API_URL=http://localhost:8000/api

4. Inicie o servidor de desenvolvimento React:

npm start

O frontend estará disponível em http://localhost:3000/


### Deploy no Render.com
#### Backend (Django)
1. Crie um novo Web Service no Render, conectando seu repositório Git.

2. Configure as seguintes opções:

Build Command:

pip install -r backend/requirements.txt
python backend/manage.py migrate
python backend/manage.py collectstatic --noinput

Start Command:

gunicorn twitter_clone.wsgi

Defina as variáveis de ambiente no Render:

SECRET_KEY: sua chave secreta Django para produção
DEBUG: False
Variáveis de configuração do banco PostgreSQL (POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT)

3. Configure o banco PostgreSQL no Render e ajuste o DATABASES do Django para usar as variáveis de ambiente.

### Frontend (React)
1. Crie um novo Static Site no Render, conectando o mesmo repositório Git.

2. Configure as opções:

Build Command:

cd frontend && npm install && npm run build

Publish Directory:

frontend/build

3. Defina a variável de ambiente no Render para o frontend:

REACT_APP_API_URL apontando para a URL do backend no Render, exemplo:

https://seu-backend.onrender.com/api

4. Para isso funcionar, o frontend deve referenciar a API via essa variável .env, usando process.env.REACT_APP_API_URL.

#### Outras observações
CORS: Certifique-se que no settings.py do Django o domínio do frontend está configurado em CORS_ALLOWED_ORIGINS.
Arquivos de mídia: Para produção, avalie usar armazenamento externo (ex: AWS S3) para imagens.
Segurança: Nunca exponha sua SECRET_KEY em repositórios públicos.
Timeouts: Render pode exigir ajuste de timeout para backend.

Comandos úteis
Backend

cd backend
source venv/bin/activate  # ou .\venv\Scripts\activate no Windows
python manage.py runserver

Frontend

cd frontend
npm start

Referências
Django REST Framework
Djoser
React Environment Variables
Render.com Docs
Contato
[Seu nome] — [Seu email ou GitHub]

