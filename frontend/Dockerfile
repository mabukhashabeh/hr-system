# Stage 1: Build
FROM node:18-alpine AS build-stage
WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

# Install dependencies with clean npm cache
RUN npm cache clean --force && npm install

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine AS production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]