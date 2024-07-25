from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import s3
import os
import rds
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    rds.create_connection()
    return templates.TemplateResponse("chat_broad.html", {"request": request})

@app.post("/api/upload")
async def upload(request: Request, message : Optional[str] = Form(None), image: Optional[UploadFile] = File(None)):
    if message == "" and image.filename == "":
        return JSONResponse(content={"error": True})
    if message == "" and image.filename != "":
            try:
                print(image)
                file_name = image.filename
                file_location = os.path.join("./tmp/", image.filename)
                with open(file_location, "wb") as file:
                    file.write(await image.read())
                s3.upload_file(file_location, "examplebucket10101010",file_name)
                rds.add_data(image = file_name)
                rds.show_data()
                os.remove(file_location)
                return JSONResponse(content={"ok": True, "file_location": file_location, "file_name": "https://df6a6ozdjz3mp.cloudfront.net/{}".format(file_name)})
            except Exception as e:
                print("Error: ", e)
    if message != "" and image.filename == "":
        try:
            print(message)
            rds.add_data(comment = message)
            rds.show_data()
            return JSONResponse(content={"ok": True, "message": message})
        except Exception as e:
            print("Error: ", e)
    if message != "" and image.filename != "":
        try:
            print(image)
            file_name = image.filename
            file_location = os.path.join("./tmp/", image.filename)
            with open(file_location, "wb") as file:
                file.write(await image.read())
            s3.upload_file(file_location, "examplebucket10101010",file_name)
            rds.add_data(comment = message, image = file_name)
            rds.show_data()
            os.remove(file_location)
            return JSONResponse(content={"ok": True, "file_location": file_location, "file_name": "https://df6a6ozdjz3mp.cloudfront.net/{}".format(file_name)})
        except Exception as e:
            print("Error: ", e)

class History(BaseModel):
    id: int
    comment: Optional[str]
    image: Optional[str]
    date: datetime

@app.get("/api/history", response_model = List[History])
async def history(request: Request):
    datas = rds.get_data()
    historys = []
    for data in datas:
        comment = History(
            id = data[0],
            comment = data[1],
            image = data[2],
            date = data[3]
        )
        historys.append(comment)

    return jsonable_encoder(historys)