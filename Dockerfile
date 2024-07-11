#FROM node:18-alpine
FROM nginx:alpine
#WORKDIR /app

#COPY package*.json ./
COPY index.html /usr/share/nginx/html
#RUN npm install

#COPY . .

#RUN npm run build

#EXPOSE 3000
EXPOSE 80
#CMD [ "npm", "run" "start:dev" ]