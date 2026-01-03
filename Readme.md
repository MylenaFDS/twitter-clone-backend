# 🐦 Twitter Clone – Backend

Backend de um **clone do Twitter**, desenvolvido com **Django + Django Rest Framework**, utilizando autenticação JWT, upload de imagens via **Cloudinary** e preparado para deploy no **Render**.

Este projeto serve como API para o frontend do Twitter Clone.

---

## 🚀 Tecnologias utilizadas

- Python 3
- Django
- Django Rest Framework
- Simple JWT (autenticação)
- PostgreSQL (produção)
- SQLite (desenvolvimento)
- Cloudinary (upload de imagens)
- Render (deploy)

---

## ⚙️ Funcionalidades

- Autenticação (login, cadastro, refresh token)
- Feed de tweets
- Curtir e descurtir tweets
- Comentários (criar, editar e deletar)
- Seguir e deixar de seguir usuários
- Perfil do usuário (avatar e banner)
- Sugestões de usuários
- Redefinição de senha
- Upload de imagens com Cloudinary

---

## 📦 Instalação local

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/MylenaFDS/twitter-clone-backend.git
cd twitter-clone-backend
```

---

### 2️⃣ Crie e ative um ambiente virtual

```bash
python -m venv venv
```

**Windows**
```bash
venv\Scripts\activate
```

**Linux / Mac**
```bash
source venv/bin/activate
```

---

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure o arquivo `.env`

Crie um arquivo **.env** na raiz do projeto com as seguintes variáveis:

```env
SECRET_KEY=sua_secret_key
DEBUG=True

DATABASE_URL=sqlite:///db.sqlite3

CLOUDINARY_CLOUD_NAME=seu_cloud_name
CLOUDINARY_API_KEY=sua_api_key
CLOUDINARY_API_SECRET=seu_api_secret
```

⚠️ O projeto usa **Cloudinary**, pois o disk do Render é pago.

---

### 5️⃣ Execute as migrações

```bash
python manage.py migrate
```

---

### 6️⃣ Crie um superusuário (opcional)

```bash
python manage.py createsuperuser
```

---

### 7️⃣ Rode o servidor

```bash
python manage.py runserver
```

A API estará disponível em:  
👉 **http://127.0.0.1:9000**

---

## 🔐 Autenticação

A autenticação é feita via **JWT**.

- Login: `POST /api/token/`
- Refresh: `POST /api/token/refresh/`

Header necessário:

```
Authorization: Bearer SEU_TOKEN
```

---

## 🌐 Deploy

O backend está preparado para deploy no **Render**.

Principais cuidados:
- Usar `DATABASE_URL` do PostgreSQL
- Configurar variáveis de ambiente no painel do Render
- Desativar `DEBUG` em produção
- Configurar `ALLOWED_HOSTS`

---

## 📁 Observações importantes

- Upload de avatar e banner é feito via **Cloudinary**
- Não depende de armazenamento local
- API pensada para consumo por frontend em React

---

## 📌 Status do projeto

✅ Funcional  
🚧 Melhorias futuras possíveis  

---

## 👩‍💻 Autora

Desenvolvido por **Mylena Ferreira de Souza**  
Projeto educacional para prática de desenvolvimento Full Stack.
