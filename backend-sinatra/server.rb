require 'bundler/setup'
Bundler.require
require 'sinatra/reloader' if development?
require 'sinatra-websocket'
require './channel'
require 'sinatra/cross_origin'

set :server, 'thin'
set :sockets, []

# CORS
set :allow_origin, :any
set :allow_methods, [:get, :post, :options]

configure do
  enable :cross_origin
end

before do
  response.headers['Access-Control-Allow-Origin'] = '*'
end

get '/' do
  "Hello world"
end

get '/websocket' do
  if request.websocket?
    request.websocket do |ws|
      bind_ws_connect(ws)
      bind_ws_event(ws)
      bind_ws_close(ws)
    end
  end
end
