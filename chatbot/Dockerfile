# Use Node image as base
FROM node:latest

# Set working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install npm dependencies
RUN npm install

# Copy the entire project to the working directory
COPY . .

# Expose port 3000 (default React port)
EXPOSE 3000

# Start the React application
CMD ["npm", "start"]
