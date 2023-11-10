FROM python:3.11-slim
WORKDIR /app
COPY . .
COPY ../requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "hiking.wsgi:application", "--bind", "0.0.0.0:8000" ]
