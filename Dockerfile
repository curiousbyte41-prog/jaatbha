FROM php:8.2-cli

RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app
COPY . .

RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt
RUN chmod +x *.py

EXPOSE $PORT
CMD php -S 0.0.0.0:$PORT my.txt
