require 'sinatra/reloader'

def bind_ws_connect(ws)
  ws.onopen do
    puts "開いた"
  end
end

def bind_ws_event(ws)
  ws.onmessage do |msg|
    puts "メッセージが来た"
    p msg
    settings.sockets.each do |s|
      s.send(msg)
    end
  end
end

def bind_ws_close(ws)
  ws.onclose do
    puts "とじた"
    settings.sockets.delete(ws)
  end
end
