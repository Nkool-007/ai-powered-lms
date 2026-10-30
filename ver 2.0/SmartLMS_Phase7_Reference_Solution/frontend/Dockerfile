FROM node:22-alpine

WORKDIR /app

# Copy dependency definitions first so this layer can be reused
# when application source changes.
COPY package*.json ./

RUN npm ci

# Copy the remaining React/Vite application.
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
