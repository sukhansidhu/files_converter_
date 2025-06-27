# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all files into the container (assumes your Dockerfile is at the root)
COPY . .

# Set working directory inside /bot because your code is there
WORKDIR /app/bot

# Install dependencies
RUN pip install --upgrade pip \
 && pip install -r ../requirements.txt

# Expose port (if needed by hosting platform)
EXPOSE 8080

# Start the bot
CMD ["python", "main.py"]
