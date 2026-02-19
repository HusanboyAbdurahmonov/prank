from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import subprocess
import os

BOT_TOKEN = os.getenv("8538918756:AAFWzZBWeTqgW0OszgOo-GNCihcYn0bv2FA")
CHAT_ID = os.getenv("8412394779")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    contents = await file.read()

    # webm saqlash
    with open("input.webm", "wb") as f:
        f.write(contents)

    # MP4 ga konvert (iPhone compatible)
    subprocess.run([
        "ffmpeg", "-i", "input.webm",
        "-vcodec", "libx264",
        "-profile:v", "baseline",
        "-level", "3.0",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-acodec", "aac",
        "output.mp4"
    ])

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"

    with open("output.mp4", "rb") as video:
        files = {
            "video": ("video.mp4", video, "video/mp4")
        }

        data = {
            "chat_id": CHAT_ID,
            "supports_streaming": True
        }

        response = requests.post(url, data=data, files=files)

    print(response.text)

    return {"status": "ok"}
