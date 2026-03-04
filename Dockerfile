FROM php:8.2-cli

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Make Python scripts executable
RUN chmod +x *.py

# Expose port (Railway will use $PORT)
EXPOSE $PORT

# Run PHP built-in server
CMD php -S 0.0.0.0:$PORT my.txt
