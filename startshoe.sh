#!/bin/bash

# Shoe Store API Startup Script
cd /home/crake178/projects/shoe-store-api

echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting Shoe Store API with uvicorn..."
uvicorn main:app --reload
