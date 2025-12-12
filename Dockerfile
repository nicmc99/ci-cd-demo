FROM python:3.11-slim

WORKDIR /app

# Let us pass a version string from Jenkins
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy app code
COPY . .

# Run the app
CMD ["python", "app.py"]
