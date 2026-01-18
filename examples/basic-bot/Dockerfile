FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code
COPY bot.py .
COPY .env.example .env

# Create directory for bridge database mount
RUN mkdir -p /app/bridge/store

# Run the bot
CMD ["python", "bot.py"]
