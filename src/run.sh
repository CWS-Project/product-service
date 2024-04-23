#!/bin/bash
cd ./src && uvicorn main:app --reload --port 8002 --host 0.0.0.0 --env-file ../.env