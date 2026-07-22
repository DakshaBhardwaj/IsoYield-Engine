FROM python:3.10-slim

# Install system dependencies (GLPK solver for Pyomo)
RUN apt-get update && apt-get install -y \
    glpk-utils \
    libglpk-dev \
    glpk-doc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI backend with Uvicorn
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
