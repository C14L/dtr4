from channels.routing import route

from dtrprofile.consumers import ws_message, ws_disconnect, ws_connect


channel_routing = [
    route("websocket.connect", ws_connect, path=r'^/api/v1/ws$'),
    route("websocket.disconnect", ws_disconnect),
    route("websocket.receive", ws_message),
]
