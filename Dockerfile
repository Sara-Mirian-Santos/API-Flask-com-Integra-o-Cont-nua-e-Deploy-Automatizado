FROM python:3

WORKDIR /app

# copia tudo para o container
COPY . /app

# RUN pip install -r requirements.txt   #no job do docker não precisamos mais executar esse comando

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 5000

CMD ["python", "main.py"]
