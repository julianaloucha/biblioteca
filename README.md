# Monitorias Facamp

Aplicação web simples de lista de tarefas (TODO) desenvolvida como projeto da faculdade. A aplicação consiste em um frontend Vue.js e um backend Flask que se comunicam via Web Services (WS). Os dados são armazenados em um banco de dados NoSQL MongoDB.

### A aplicação pode:
- Fazer login e registro de usuários através de login e senha
- Guardar a lista de tarefas separadas por usuário
- Atualizar, incluir e excluir tarefas pela demanda do usuário 

## Requisitos

- Python 3.7+
- MongoDB Atlas
- Node.js e npm

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/julianaloucha/monitoriasfacamp.git
cd monitoriasfacamp
```


2. Crie e ative um ambiente virtual Python:

```bash
python -m venv .venv
source .venv/bin/activate (Linux/Mac)
.venv\Scripts\activate (Windows)
```

3. Instale as dependências do backend:

```bash
pip install -r requirements.txt
```

4. Crie um arquivo `.ini` na raiz do projeto e adicione suas credenciais do MongoDB Atlas:

```
[PROD]
DB_URI = seu_uri_de_conexão_do_mongodb_atlas
```

5. Instale as dependências do frontend:

```bash
cd frontend
npm install
```

## Executando o projeto

1. Inicie o servidor backend:

```bash
cd monitoriasfacamp
python wsgi.py
```

2. Inicie o servidor frontend:

```bash
cd ./monitoriasfacamp/frontend
npm run dev
```

3. Abra seu navegador e acesse [http://localhost:5173](http://localhost:5173) (ou a porta especificada pelo seu servidor frontend) para ver a aplicação em execução.

## Contribuindo

Pull requests são bem-vindos. Para grandes alterações, abra uma issue primeiro para discutir o que você gostaria de mudar.

## Licença

[MIT](https://choosealicense.com/licenses/mit/)