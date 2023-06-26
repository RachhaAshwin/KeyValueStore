import streamlit as st
import grpc

import kv_pb2
import kv_pb2_grpc

# Define the gRPC server address
grpc_server_address = '127.0.0.1:4000'  # Replace with your gRPC server address

# Create a gRPC channel and stub
channel = grpc.insecure_channel(grpc_server_address)
stub = kv_pb2_grpc.ClientStub(channel)

# Streamlit UI layout
st.sidebar.title("gRPC Client")
action = st.sidebar.selectbox("Select an action", ["Get", "Set", "List", "Upload Key-Value File"], key="action_select")
st.sidebar.write("")

def get_key():
    key = st.text_input("Enter Key:", key="get_key_input")
    if st.button("Get", key="get_button"):
        try:
            response = stub.Get(kv_pb2.GetKey(key=key))
            if response.defined:
                st.success(f"Value: {response.value}")
            else:
                st.warning("Key not found.")
        except grpc.RpcError as e:
            st.error(f"gRPC Error: {e.code().name} - {e.details()}")

def set_key():
    key = st.text_input("Enter Key:", key="set_key_input")
    value = st.text_input("Enter Value:", key="set_value_input")
    if st.button("Set", key="set_button"):
        try:
            stub.Set(kv_pb2.SetKey(key=key, value=value, broadcast=True))
            st.success("Key-Value pair set successfully.")
        except grpc.RpcError as e:
            st.error(f"gRPC Error: {e.code().name} - {e.details()}")

def list_keys():
    if st.button("List", key="list_button"):
        try:
            response = stub.List(kv_pb2.Void())
            st.success("Key-value pairs defined on the server:")
            for key, value in response.store.items():
                st.write(f"- '{key}' = '{value}'")
        except grpc.RpcError as e:
            st.error(f"gRPC Error: {e.code().name} - {e.details()}")

def upload_file():
    file = st.file_uploader("Upload Key-Value File (.txt)", type="txt", key="file_upload")
    if file is not None:
        content = file.read().decode("utf-8")
        parse_and_display_key_value_pairs(content)

def parse_and_display_key_value_pairs(content):
    st.subheader("Parsed Key-Value Pairs:")
    lines = content.splitlines()
    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            key = parts[0]
            value = " ".join(parts[1:])
            stub.Set(kv_pb2.SetKey(key=key, value=value, broadcast=True))
            st.write(f"- '{key}': '{value}'")

# Streamlit UI layout
st.sidebar.title("gRPC Client")
if action == "Get":
    get_key()
elif action == "Set":
    set_key()
elif action == "List":
    list_keys()
elif action == "Upload Key-Value File":
    upload_file()
