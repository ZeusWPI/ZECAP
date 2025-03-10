#!/bin/bash

backend=false
frontend=false
build=false

# Arguments parsing
while getopts ":bfc" opt; do
  case ${opt} in
  b)
    backend=true
    ;;
  f)
    frontend=true
    ;;
  c)
    build=true
    ;;
  :)
    echo "Usage: $0 [-b] [-f] [-c]" 1>&2
    exit 1
    ;;
  \?)
    echo "Usage: $0 [-b] [-f] [-c]" 1>&2
    exit 1
    ;;
  esac
done

echo "Checking environment file..."

# If clean build, remove .env and db.sqlite3
if [ "$build" = true ]; then
  rm .env >/dev/null 2>&1
  rm -f backend/db.sqlite3 >/dev/null 2>&1
fi

# Create environment file if it doesn't exist
if ! [ -f .env ]; then
  cp .dev.env .env
  sed -i "s/^DJANGO_SECRET_KEY=.*/DJANGO_SECRET_KEY=totally_random_key_string/" .env
  sed -i "s,^DJANGO_ROOT_DIR=.*,DJANGO_ROOT_DIR=$PWD/backend," .env
  echo "Created environment file"
fi

# Build Docker images
if [ "$build" = true ]; then
  echo "Building Docker images..."
  echo "This can take a while..."
  docker-compose -f development.yml build --no-cache
  if [ $? -ne 0 ]; then
    echo "Error: Failed to build Docker images" 1>&2
    exit 1
  fi
fi

# Start services
echo "Starting services..."
docker-compose -f development.yml up -d
if [ $? -ne 0 ]; then
  echo "Error: Failed to start Docker services" 1>&2
  exit 1
fi

echo "-------------------------------------"
echo "Following logs..."
echo "Press CTRL + C to stop all containers"
echo "-------------------------------------"

# Follow logs based on flags
if [ "$backend" = true ]; then
  docker-compose -f development.yml logs --follow --tail 50 backend
  if [ $? -ne 0 ]; then
    echo "Error: Failed to follow backend logs" 1>&2
    exit 1
  fi
elif [ "$frontend" = true ]; then
  docker-compose -f development.yml logs --follow --tail 50 frontend
  if [ $? -ne 0 ]; then
    echo "Error: Failed to follow backend logs" 1>&2
    exit 1
  fi
else
  docker-compose -f development.yml logs --follow --tail 50 backend frontend
  if [ $? -ne 0 ]; then
    echo "Error: Failed to follow backend logs" 1>&2
    exit 1
  fi
fi

echo "Cleaning up..."

docker-compose -f development.yml down

echo "Done."

