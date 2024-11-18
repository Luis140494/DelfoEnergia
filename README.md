### 📋 Pré-requisitos
De que coisas você precisa para executar o software?
```
- **FastAPI** para expor dados de um banco de dados PostgreSQL (Fonte).
- **PostgreSQL** para armazenar dados de entrada e saída.
- **SQLAlchemy** para interação com o banco de dados alvo.
- **Pandas** para transformação de dados.
- **Dagster** para orquestração do pipeline ETL.
- **Docker** e **Docker Compose** para orquestrar os containers.
```

### 🚀 Começando
Criar ambiente virtual
```
python -m venv ambientevirtual
ativar ambiente vitual
.\ambientevirtual\Scripts\activate
Para desativar ambiente vitual caso necessário
deactivate
```
### 🔧 Instalação
instalar as bibliotecas junto ao python e fastApi 
```
pip install fastapi pyscopg2-binary sqlalchemy sqlmodel asyncpg uvicorn pytz passlib python-multipart pydantic-settings httpx pandas dagster dagit, dagster_postgres
```
## ⚙️ Executar
Primeira parte
```
Criar dois banco de dados no PostgreSQL, um chamado Fonte e outro Alvo
Importante: Criar tabelas do banco alvo primeiro, pois o fonte além de criar a tabela vai inserir os registros em 1 em 1 minuto como foi solicitado 
Criar tabela do banco de dados Alvo com o comando "python app/criar_tabela_alvo.py" 
Criar tabela do banco de dados Fonte com o comando "python app/criar_tabela_fonte.py" 
```
Segunda Parte
```
Abrir um novo terminal caso você queira continuar alimentando o banco Fonte da primeira parte 
Rodar a Api do banco fonte dentro da pasta app com comando "python app/main.py"
```
Terceiro Parte 
```
Rodas o script ETL caso não queria utilizar o dagster com comando "python app/etl_script.py", esse local é aonde vai ser realizado a chamada da Api do Banco fonte para alimentar o banco alvo.








