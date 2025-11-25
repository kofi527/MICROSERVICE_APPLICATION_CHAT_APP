FROM python:3.11-slim
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install uvicorn with WebSocket support
RUN pip install "uvicorn[standard]"

# Copy the app code
COPY . .

# Expose the port
EXPOSE 8001

# Start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]