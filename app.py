import responder

api = responder.API()
clients = {} # 1

@api.route('/ws', websocket=True)
async def websocket(ws):
    await ws.accept()
    key = ws.headers.get('sec-websocket-key') # 2
    clients[key] = ws # 3
    try:
        while True:
            msg = await ws.receive_text()
            for client in clients.values(): # 4
                await client.send_text(msg)
    except:
        await ws.close()
        del clients[key] # 5

api.add_route('/', static=True)
api.run()
