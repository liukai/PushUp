import sys
sys.path.append("../utils")
import usage_reporter

REVERSE_PROXY = {
    "port": 8080,
    "proxied_host": ("localhost", 5000),
    "subscription_path": ["/message/event_based_update"],
    "backlog": 10000
}

PUBLISH = {
    # expiredIn: specify the how long will the message 
    # be removed from the pub/sub queue
    "expiredIn": 60,
    "port": 8081,
    "message_format": '{"result": "ok", "data": %s, "max_id": %d}',
    "wait_for": 50,
    "backlog": 10000
}

PROFILE = {
    "enabled": True,
    "interval": 1,
    "reporter": usage_reporter.UsageReporter,
    "output": "profile.log"
}


