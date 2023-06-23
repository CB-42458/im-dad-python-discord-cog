# Multi-architecture base image
FROM --platform=$BUILDPLATFORM node:latest

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . .

# Install dependencies
RUN npm install

# Expose port 6969
EXPOSE 6969

# Start the application
CMD ["node", "server.js"]