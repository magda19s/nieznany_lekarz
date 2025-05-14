FROM node:18.17-alpine

WORKDIR /usr/app
ENV NODE_ENV=production
ENV PATH=/usr/app/node_modules/.bin:$PATH

COPY ./package*.json ./
RUN npm i --also=dev
COPY . ./

EXPOSE 5173
CMD ["npm", "run", "dev"]
