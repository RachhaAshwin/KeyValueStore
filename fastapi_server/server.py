import uvicorn

def start_http_server():
    """Start the FastAPI server."""

    # Specify the module and object where your FastAPI application resides
    app_module = 'main'
    app_object = 'app'

    # Set the host and port for the FastAPI server
    host = '127.0.0.1'
    port = 8000

    # Start the FastAPI server using uvicorn
    uvicorn.run(app_module + ':' + app_object, host=host, port=port)

if __name__ == "__main__":
    start_http_server()
