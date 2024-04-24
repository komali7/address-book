# main.py
from app import contoller, db_connect
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def start_db():
    conn = db_connect.db_connect()
    db_connect.create_addresses_table(conn)
    conn.close()


app.include_router(contoller.router)