PYLONS_PID_FILE=pylons.pid

# Start the redis
echo "Starting redis..."
redis-server > redis.log &

# Start the pylons 
echo "Starting chatroom..."
(cd chatroom && paster serve development.ini &)

# Start the reverse proxy

