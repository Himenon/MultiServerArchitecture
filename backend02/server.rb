require 'bundler/setup'
Bundler.require
require 'sinatra/reloader' if development?
require 'sinatra-websocket'
require './channel'

set :server, 'thin'
set :sockets, []

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
