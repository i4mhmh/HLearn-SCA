# -*- coding: utf-8 -*-
"""
"* Author     : M0nk3y"
"* Version    : 1.0"
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import os
import time

UPLOAD_DIR = Path("upload")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
datasetRouter = APIRouter(
    prefix="/api/dataset",
    tags=["Dataset"]
)

# 时间戳转换
def timestamp_to_time(timestamp):
    return time.strftime('%Y-%m-%d %H-:%M:%S', time.localtime(timestamp))

@datasetRouter.get("/show")
async def dataset_pull():
    file_list = os.listdir(UPLOAD_DIR)
    file_name = [item for item in file_list if str(item).split(".")[-1].lower() in ['zip', 'h5']]
    file_create_date = []
    file_size = []
    # 挨个读取创建时间
    for name in file_name:
        relate_path = str(UPLOAD_DIR) + "/" + name
        file_create_date.append(timestamp_to_time(os.path.getctime(relate_path)))
        file_size.append(round(os.path.getsize(relate_path) / float(1024 * 1024), 2))
    # 转换成json
    result = []
    for index, item in enumerate(file_name):
        json_data = {"id": index + 1, "file_name": item, "file_create_date": file_create_date[index], "file_size": file_size[index]}
        result.append(json_data)
    return {"data": result}

@datasetRouter.post("/upload")
async def dataset_upload(file: UploadFile = File(...)):
    file_name = Path(file.filename).name
    if not file_name:
        raise HTTPException(status_code=400, detail="Invalid file name")
    file_location = UPLOAD_DIR / file_name
    print(file_location)
    try:
        with file_location.open("wb") as f:
            while True:
                chuck = await file.read(1024 * 1024)
                if not chuck:
                    break
                f.write(chuck)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {e}")
    finally:
        file.file.close()
    return {"filename": file.filename}
