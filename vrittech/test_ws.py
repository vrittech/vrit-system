import asyncio
import websockets

JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU5NDc0MDE2LCJpYXQiOjE3NTY4ODIwMTYsImp0aSI6IjFlYzU0MjhjNzJlMzQ3MjQ5Y2Q3YzU2N2UxYzZlMzBlIiwidXNlcl9pZCI6MX0._i6b6btamHx4_tEcskhLm3YucsvcnJhoL7jY80a8sjo"

async def test_ws():
    uri = "ws://127.0.0.1:8000/ws/notification/"
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}"
    }
    
    async with websockets.connect(uri, extra_headers=headers) as websocket:
        print("Connected!")
        while True:
            msg = await websocket.recv()
            print("Received:", msg)

asyncio.run(test_ws())