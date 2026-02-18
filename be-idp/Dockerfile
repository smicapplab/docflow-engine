# -------- Build Stage --------
FROM node:20-slim AS builder

WORKDIR /app

# Install dependencies (deterministic)
COPY package*.json ./
RUN npm ci

# Copy source and build
COPY . .
RUN npm run build

# Prune dev dependencies to produce production node_modules
RUN npm prune --omit=dev


# -------- Production Stage --------
FROM node:20-slim

WORKDIR /app

# Security / runtime best practices
ENV NODE_ENV=production
ENV TZ=UTC

# Install a minimal init system to handle PID 1 correctly
RUN apt-get update && apt-get install -y --no-install-recommends dumb-init \
  && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r nodejs && useradd -r -g nodejs nodejs

# Copy only what we need from the builder (including pruned node_modules)
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist

# Set proper ownership
RUN chown -R nodejs:nodejs /app

# Expose API port
EXPOSE 3000

# Switch to non-root user
USER nodejs

# Start NestJS with init
CMD ["dumb-init", "node", "dist/main.js"]
