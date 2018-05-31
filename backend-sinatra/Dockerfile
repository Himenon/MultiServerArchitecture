FROM ruby:2.5.1

RUN mkdir -p /code
WORKDIR /code
COPY ./ /code
RUN bundle install

CMD ["ruby", "server.rb", "-p", "5432", "-o", "0.0.0.0"]
