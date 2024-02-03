#!/bin/bash
set -e

case $1 in
  api)
    echo "Starting api server"
    exec uvicorn --port 8000 --host 0.0.0.0 main:app
  ;;

  dev)
    echo "Starting dev server"
    exec python main.py
  ;;

  *)
    exec "$@"
  ;;
esac

exit 0
