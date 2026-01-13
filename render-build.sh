#!/bin/bash

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Generate Prisma Client
echo "Generating Prisma Client..."
prisma generate

# Push database schema (creates tables if not exist)
echo "Pushing database schema..."
prisma db push --accept-data-loss

echo "Build completed!"
