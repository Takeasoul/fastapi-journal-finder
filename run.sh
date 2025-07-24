#!/bin/bash

# ��������� ������������ ���������
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "Virtual environment activated."
else
    echo "Virtual environment not found. Please ensure 'venv' exists and is properly set up."
    exit 1
fi

# ����������� ���� ��� ����������� �������
while true; do
    echo "Starting Uvicorn..."
    # ������ Uvicorn � ��������� ������ � �����
    uvicorn app.main:app --host 0.0.0.0 --port 8181
    # ���� Uvicorn ����������, ������� ��������� � ��� 5 ������ ����� ������������
    echo "Uvicorn stopped with exit code $?. Restarting in 5 seconds..."
    sleep 5
done