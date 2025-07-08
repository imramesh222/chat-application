#!/bin/bash
set -a
[ -f ./.env ] && source ./.env
set +a

echo "Starting on port: $SERVICE_PORT"
uvicorn app.main:app --host 0.0.0.0 --port ${SERVICE_PORT:-8003} --reload
