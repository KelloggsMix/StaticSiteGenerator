python3 src/main.py
cd public && python3 -m http.server 8888 &

for i in {1..10}; do
    if curl -s http://localhost:8888 > /dev/null; then
        echo "Server's up!"
        break
    fi 
    echo "Waiting for the server to start..."
    sleep
done