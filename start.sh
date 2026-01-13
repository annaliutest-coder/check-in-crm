#!/bin/bash

# Generate Prisma Client
echo "Generating Prisma Client..."
prisma generate

# Push database schema (creates tables if not exist)
echo "Pushing database schema..."
prisma db push --accept-data-loss

# Start the application
echo "Starting FastAPI application..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
