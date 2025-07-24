#!/bin/bash

# Активация виртуального окружения
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "Virtual environment activated."
else
    echo "Virtual environment not found. Please ensure 'venv' exists and is properly set up."
    exit 1
fi

# Бесконечный цикл для перезапуска сервера
while true; do
    echo "Starting Uvicorn..."
    # Запуск Uvicorn с указанием модуля и порта
    uvicorn app.main:app --host 0.0.0.0 --port 8181
    # Если Uvicorn завершился, выводим сообщение и ждём 5 секунд перед перезапуском
    echo "Uvicorn stopped with exit code $?. Restarting in 5 seconds..."
    sleep 5
done