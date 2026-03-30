from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import Response, FileResponse
from fastapi.staticfiles import StaticFiles
import io
from PIL import Image, ImageFilter

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.post("/sharpen")
async def sharpen(
    file: UploadFile = File(...),
    radius: float = Form(1.5),
    percent: int = Form(150),
    threshold: int = Form(3),
):
    data = await file.read()
    img = Image.open(io.BytesIO(data)).convert("RGB")

    sharpened = img.filter(
        ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=threshold)
    )

    buf = io.BytesIO()
    fmt = "JPEG"
    content_type = "image/jpeg"
    if file.filename.lower().endswith(".png"):
        fmt = "PNG"
        content_type = "image/png"

    sharpened.save(buf, format=fmt, quality=95)
    buf.seek(0)

    return Response(content=buf.read(), media_type=content_type)
