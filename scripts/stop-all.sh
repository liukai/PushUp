echo "Shutting down the chatroom"
(cd chatroom && paster serve development.ini &)

echo "Shutting down redis"
redis-cli shutdown

