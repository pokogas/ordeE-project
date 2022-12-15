FROM node:16.13.2-alpine
ARG AXIOS_BASEURL
ARG AXIOS_BROWSER_BASEURL
RUN apk update
COPY . .
WORKDIR /usr/src/app
COPY package.json ./
COPY package-lock.json ./
RUN npm install
RUN npm run build
ENV HOST=0.0.0.0 PORT=3001
