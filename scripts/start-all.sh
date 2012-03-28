PYLONS_PID_FILE=pylons.pid

# Start the redis
echo "Starting redis..."
redis-server > redis.log &

# Start the pylons 
echo "Starting chatroom..."
chatroom.sh start

# Start the reverse proxy

