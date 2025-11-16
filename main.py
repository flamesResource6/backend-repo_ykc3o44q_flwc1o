import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import db, create_document, get_documents
from schemas import Artwork, Event, Member, Message

app = FastAPI(title="Fine Arts Club API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Fine Arts Club Backend is running"}


@app.get("/api/hello")
def hello():
    return {"message": "Welcome to the Fine Arts Club API"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    return response


# --------- API Models for Responses ---------
class CreateResponse(BaseModel):
    id: str


# --------- Artworks ---------
@app.post("/api/artworks", response_model=CreateResponse)
async def create_artwork(artwork: Artwork):
    try:
        inserted_id = create_document("artwork", artwork)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/artworks", response_model=List[dict])
async def list_artworks(tag: Optional[str] = None, featured: Optional[bool] = None, limit: int = 50):
    try:
        filter_dict = {}
        if tag:
            filter_dict["tags"] = {"$in": [tag]}
        if featured is not None:
            filter_dict["featured"] = featured
        docs = get_documents("artwork", filter_dict, limit)
        # Convert ObjectId to string for _id
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------- Events ---------
@app.post("/api/events", response_model=CreateResponse)
async def create_event(event: Event):
    try:
        inserted_id = create_document("event", event)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/events", response_model=List[dict])
async def list_events(upcoming_only: bool = True, limit: int = 50):
    try:
        filter_dict = {}
        if upcoming_only:
            filter_dict["date"] = {"$gte": datetime.utcnow()}
        docs = get_documents("event", filter_dict, limit)
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------- Members (applications) ---------
@app.post("/api/members", response_model=CreateResponse)
async def create_member(member: Member):
    try:
        inserted_id = create_document("member", member)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------- Contact messages ---------
@app.post("/api/messages", response_model=CreateResponse)
async def create_message(message: Message):
    try:
        inserted_id = create_document("message", message)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
