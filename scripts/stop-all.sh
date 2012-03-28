echo "Shutting down the chatroom"
chatroom.sh stop

echo "Shutting down redis"
redis-cli shutdown

