# syntax=docker/dockerfile:1

# =========================================================
# Stage 1: Build the Angular application
# =========================================================
FROM node:22-alpine AS builder


WORKDIR /app

# Copy dependency files first so Docker can cache npm install.
COPY package.json package-lock.json ./

# Reproducible dependency installation based on package-lock.json.
RUN npm ci

# Copy the remaining Angular source code.
COPY . .

# Create an optimized production build.
RUN npm run build -- --configuration production


# =========================================================
# Stage 2: Serve Angular using Nginx
# =========================================================
FROM nginx:1.28-alpine AS runtime

# Remove the default Nginx configuration.
RUN rm -f /etc/nginx/conf.d/default.conf \
    && mkdir -p \
        /tmp/client_temp \
        /tmp/proxy_temp \
        /tmp/fastcgi_temp \
        /tmp/uwsgi_temp \
        /tmp/scgi_temp \
    && chown -R nginx:nginx \
        /tmp/client_temp \
        /tmp/proxy_temp \
        /tmp/fastcgi_temp \
        /tmp/uwsgi_temp \
        /tmp/scgi_temp \
        /usr/share/nginx/html

# Copy our custom Nginx configuration.
COPY nginx.conf /etc/nginx/nginx.conf

# Copy only the compiled Angular files from the builder.
COPY --from=builder \
    --chown=nginx:nginx \
    /app/dist/dashboard/browser/ \
    /usr/share/nginx/html/

# Do not run the Angular container as root.
USER nginx

EXPOSE 8080

# Docker will use this endpoint to determine container health.
HEALTHCHECK --interval=30s \
    --timeout=5s \
    --start-period=10s \
    --retries=3 \
    CMD wget -q -O - http://127.0.0.1:8080/health || exit 1

CMD ["nginx", "-g", "daemon off;"]