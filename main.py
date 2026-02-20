import os
import requests
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

BOT_TOKEN = "8538918756:AAFWzZBWeTqgW0OszgOo-GNCihcYn0bv2FA"
CHAT_ID = "8412394779"

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    contents = await file.read()

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"

    files = {
        "video": ("video.mp4", contents)
    }

    data = {
        "chat_id": CHAT_ID,
        "supports_streaming": True
    }

    response = requests.post(url, data=data, files=files)
    print(response.text)

    return {"status": "ok"}