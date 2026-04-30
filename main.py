from fastapi import FastAPI
import json

app = FastAPI()

# load your JSON file
with open("lectures.json", "r") as f:
    data = json.load(f)

@app.get("/")
def home():
    return {"status": "working"}

# ✅ GET FULL PLAYLIST
@app.get("/playlist")
def get_playlist():
    return data

# ✅ GET SINGLE LECTURE
@app.get("/playlist/{lecture_id}")
def get_lecture(lecture_id: int):
    for lecture in data["lectures"]:
        if lecture["id"] == lecture_id:
            return lecture

    return {"error": "not found"}