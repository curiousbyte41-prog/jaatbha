FROM php:8.2-cli

# Install Python and pip with --break-system-packages flag
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install Python dependencies with --break-system-packages
RUN pip3 install --no-cache-dir --break-system-packages -r Requirements.txt

# Make Python scripts executable
RUN chmod +x *.py

# Expose port
EXPOSE $PORT

# Run PHP built-in server
CMD php -S 0.0.0.0:$PORT my.txt
