#!/bin/bash

set -e

case "$1" in
  build)
    echo "Building images..."
    docker compose build
    ;;

  up)
    echo "Starting services in foreground..."
    docker compose up
    ;;

  up-detached)
    echo "Starting services in detached mode..."
    docker compose up -d
    ;;

  down)
    echo "Stopping services..."
    docker compose down
    ;;

  clean)
    echo "Removing containers, images, and volumes..."
    docker compose down --volumes --rmi all
    ;;

  logs)
    echo "Showing logs..."
    docker compose logs -f
    ;;

  *)
    echo "Usage: ./manage.sh {build|up|up-detached|down|clean|logs}"
    exit 1
    ;;
esac
