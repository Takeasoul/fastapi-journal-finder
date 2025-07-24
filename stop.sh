#!/bin/bash

# ����� ���� ���������, ��������� � �������� Uvicorn ����� run.sh
PIDS=$(pgrep -f "uvicorn app.main:app")

if [ -z "$PIDS" ]; then
    echo "������ �� �������."
else
    # ���������� ���������
    echo "������������ ������..."
    kill -9 $PIDS
    echo "������ ����������."
fi