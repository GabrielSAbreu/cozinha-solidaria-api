# 1. Imagem base oficial do Python (leve e otimizada)
FROM python:3.12-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Impede que o Python grave arquivos .pyc no disco e ativa saída de logs sem buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 4. Copia apenas o requirements.txt primeiro (aproveita o cache de camadas do Docker)
COPY requirements.txt .

# 5. Instala as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia todo o restante do código da aplicação para o container
COPY . .

# 7. Garante a criação da pasta database para o SQLite
RUN mkdir -p database

# 8. Expõe a porta 8000
EXPOSE 8000

# 9. Comando para rodar a API FastAPI com o Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]