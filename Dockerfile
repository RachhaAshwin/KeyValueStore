FROM python:3.10

COPY requirements.txt app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY grpc_server /app/grpc_server

EXPOSE 8501 4000

CMD ["bash", "-c", "streamlit run /app/grpc_server/python/client.py & python /app/grpc_server/python/server.py"]
