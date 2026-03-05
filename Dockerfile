FROM php:8.2-cli

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app
COPY . .

# Make sure files exist
RUN ls -la

# Install Python packages
RUN pip3 install --no-cache-dir --break-system-packages requests

EXPOSE $PORT

# Start PHP server
CMD php -S 0.0.0.0:$PORT
