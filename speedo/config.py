
# incept path with the following pattern 
LONG_POLLING_PATHS = [
    "/message/event_based_update",
]

SERVER = {
    "listen_client_port": 5000,
    "listen_backend_port": 5001,
}

PROXIED_SERVER = {
    "host": "localhost",
    "port": 5000
}
