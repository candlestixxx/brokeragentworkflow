FROM python:3.12-slim

# Build frontend assets
FROM node:22-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Build Python app
FROM python:3.12-slim
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the python application code
COPY . .

# Copy compiled frontend assets from the node builder stage
COPY --from=frontend-builder /app/dist /app/dist

# Set default env variables (can be overridden by docker-compose)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port for Flask
EXPOSE 5000

# Default command (will be overridden in docker-compose for the scheduler service)
CMD ["flask", "run"]
