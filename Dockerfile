FROM nginx:1.25-alpine

# Install htpasswd utility
RUN apk add --no-cache apache2-utils

# Create Basic Auth credentials (punky/PunkyAdmin2026!)
RUN htpasswd -cb /etc/nginx/.htpasswd punky 'PunkyAdmin2026!'

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy portal files
COPY index.html /usr/share/nginx/html/index.html

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -q --spider http://localhost/healthz || exit 1

EXPOSE 80
