# Use the official Python base image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the working directory
COPY grpc_server /app/grpc_server

# Install the required dependencies
RUN pip install --no-cache-dir -r /app/grpc_server/requirements.txt

# Expose the desired ports
EXPOSE 80 4000

# Set the command to run your Streamlit app and gRPC server
CMD ["bash", "-c", "streamlit run /app/grpc_server/python/client.py & python /app/grpc_server/python/server.py"]