# Use official lightweight Node.js image
FROM node:18-slim

# Set working directory
WORKDIR /app

# Copy package files and install dependencies (none in this case, but good practice)
COPY package*.json ./
RUN npm install --production

# Copy the application code
COPY index.js .

# Expose the application port
EXPOSE 8080

# Run the application as a non-root user for security
USER node

# Start the application
CMD [ "node", "index.js" ]
