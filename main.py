# # from fastapi import FastAPI
# # import json

# # app = FastAPI()

# # # load your JSON file
# # with open("lectures.json", "r") as f:
# #     data = json.load(f)

# # @app.get("/")
# # def home():
# #     return {"status": "working"}

# # # ✅ GET FULL PLAYLIST
# # @app.get("/playlist")
# # def get_playlist():
# #     return data

# # # ✅ GET SINGLE LECTURE
# # @app.get("/playlist/{lecture_id}")
# # def get_lecture(lecture_id: int):
# #     for lecture in data["lectures"]:
# #         if lecture["id"] == lecture_id:
# #             return lecture

# #     return {"error": "not found"}


# from fastapi import FastAPI
# from fastapi.responses import StreamingResponse
# import requests
# import json

# app = FastAPI()

# with open("lectures.json", "r") as f:
#     data = json.load(f)


# @app.get("/playlist")
# def get_playlist():
#     return data


# @app.get("/audio/{lecture_id}")
# def stream_audio(lecture_id: int):
#     lecture = next(
#         (l for l in data["lectures"] if l["id"] == lecture_id),
#         None
#     )

#     if not lecture:
#         return {"error": "not found"}

#     url = lecture["audio_url"]

#     headers = {
#         "User-Agent": "Mozilla/5.0",
#         "Referer": "https://daarulxadiith.com/"
#     }

#     r = requests.get(url, stream=True, headers=headers)

#     return StreamingResponse(r.raw, media_type="audio/mpeg")




from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import requests
import json

app = FastAPI()

with open("lectures.json", "r") as f:
    data = json.load(f)


@app.get("/playlist")
def get_playlist():
    return data


@app.get("/audio/{lecture_id}")
def stream_audio(lecture_id: int):
    lecture = next(
        (l for l in data["lectures"] if l["id"] == lecture_id),
        None
    )

    if not lecture:
        raise HTTPException(status_code=404, detail="Not found")

    url = lecture["audio_url"]

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://daarulxadiith.com/"
    }

    r = requests.get(url, stream=True, headers=headers)

    if r.status_code != 200:
        raise HTTPException(status_code=500, detail="Audio fetch failed")

    def iter_audio():
        for chunk in r.iter_content(chunk_size=1024 * 64):
            if chunk:
                yield chunk

    return StreamingResponse(
        iter_audio(),
        media_type=r.headers.get("Content-Type", "audio/mpeg"),
        headers={
            "Content-Length": r.headers.get("Content-Length"),
            "Accept-Ranges": "bytes",
        },
    )