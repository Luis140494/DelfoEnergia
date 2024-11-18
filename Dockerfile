# Use Python 3.10 como imagem base
FROM python:3.10.0

# Define o diretório de trabalho no container
WORKDIR /app

# Copie os arquivos do diretório local para o container
COPY . /app/

# Instalar dependências do projeto
RUN pip install pip install fastapi pyscopg2-binary sqlalchemy sqlmodel asyncpg uvicorn pytz passlib python-multipart pydantic-settings httpx pandas dagster dagit, dagster_postgres -r requirements.txt

# Exponha a porta 8000 para a API FastAPI
EXPOSE 8000

# Comando padrão para rodar o FastAPI (API)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]