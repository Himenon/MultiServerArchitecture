FROM node:10.3

RUN mkdir -p /code
WORKDIR /code
COPY ./ /code
RUN npm install

CMD ["node", "server.js"]
