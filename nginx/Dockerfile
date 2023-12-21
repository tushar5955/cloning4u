FROM nginx:latest

# Install Certbot dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        apt-transport-https \
        ca-certificates \
        curl \
        python3-certbot-nginx \
    && rm -rf /var/lib/apt/lists/*

# Copy the default configuration file
COPY default.conf /etc/nginx/conf.d/default.conf
