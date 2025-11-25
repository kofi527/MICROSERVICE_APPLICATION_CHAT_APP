from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow all for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ---------------------- DB Dependency -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------- Connection Manager ----------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket):
        self.active_connections[room_id].remove(websocket)

    async def broadcast(self, room_id: str, message: str):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_text(message)

manager = ConnectionManager()


# ---------------------- REST API Endpoints ----------------------

# Send a message (store in DB + broadcast to websocket clients)
@app.post("/messages/")
def send_message(room_id: str, sender: str, content: str, db: Session = Depends(get_db)):
    message = models.Message(room_id=room_id, sender=sender, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)

    # Broadcast to websocket users
    import asyncio
    asyncio.create_task(
        manager.broadcast(room_id, f"{sender}: {content}")
    )

    return message


# Get messages for a room
@app.get("/messages/{room_id}")
def get_messages(room_id: str, db: Session = Depends(get_db)):
    return db.query(models.Message).filter(models.Message.room_id == room_id).all()


# ---------------------- WebSocket Endpoint -----------------------
@app.websocket("/ws/{room_id}")
async def websocket_chat(websocket: WebSocket, room_id: str):
    await manager.connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast message to everyone in the room
            await manager.broadcast(room_id, data)
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
