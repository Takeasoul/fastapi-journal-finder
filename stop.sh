#!/bin/bash

# Поиск всех процессов, связанных с запуском Uvicorn через run.sh
PIDS=$(pgrep -f "uvicorn app.main:app")

if [ -z "$PIDS" ]; then
    echo "Сервер не запущен."
else
    # Завершение процессов
    echo "Останавливаю сервер..."
    kill -9 $PIDS
    echo "Сервер остановлен."
fi