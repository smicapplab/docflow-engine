# -------- Build Stage --------
FROM node:20-slim AS builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source
COPY . .

# Build NestJS app
RUN npm run build


# -------- Production Stage --------
FROM node:20-slim

WORKDIR /app

ENV NODE_ENV=production

# Copy only necessary artifacts from builder
COPY --from=builder /app/package*.json ./
RUN npm install --omit=dev

COPY --from=builder /app/dist ./dist

# Expose API port
EXPOSE 3000

# Start NestJS
CMD ["node", "dist/main.js"]
