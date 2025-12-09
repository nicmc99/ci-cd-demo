FROM python:3.11-slim
WORKDIR /app

# Copy dependency list first (better cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy app code
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
