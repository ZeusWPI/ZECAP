read -p "Enter your username: " username

curl -s -X POST http://127.0.0.1:8000/api/countdown/saveUsername/ -H "Content-Type: application/json" -d "{\"username\": \"$username\"}"

echo "Username saved successfully!"

echo "Joining session..."

curl -s -X POST http://127.0.0.1:8000/api/countdown/joinSession/ -H "Content-Type: application/json"  -d "{\"username\": \"$username\", \"session_name\": \"zeusisdemax\"}"

echo "Session joined successfully!"

echo "Waiting for session to start..."

while true; do
  sleep 5
  response2=$(curl -s -X POST http://127.0.0.1:8000/api/countdown/getQuestion/ -H "Content-Type: application/json" -d "{\"username\": \"$username\", \"session_name\": \"zeusisdemax\"}")
  echo response2
done