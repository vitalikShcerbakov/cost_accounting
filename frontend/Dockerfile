FROM node:20

WORKDIR /frontend
COPY . .
RUN npm config set strict-ssl false
RUN npm ci
RUN npm install
RUN npm run build
