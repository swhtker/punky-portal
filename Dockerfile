FROM nginx:1.25-alpine

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy htpasswd for basic auth
COPY .htpasswd /etc/nginx/.htpasswd

# Copy all HTML files
COPY *.html /usr/share/nginx/html/

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q --spider http://localhost/healthz || exit 1

EXPOSE 80
