FROM node:alpine
WORKDIR /usr/src/app
COPY package*.json ./
COPY node_modules/* /usr/local/lib/node_modules/
ADD . .
EXPOSE 8080
CMD [ "npm", "start"]