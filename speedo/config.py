
REVERSE_PROXY = {
    "port": 8000,
    "proxied_host": ("localhost", 5000),
    "subscription_path": ["/message/event_based_update"]
}

PUBLISH = {
    # expiredIn: specify the how long will the message 
    # be removed from the pub/sub queue
    "expiredIn": 60,
    "port": 8081
}
