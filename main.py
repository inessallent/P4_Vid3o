from fastapi import FastAPI, Query, HTTPException, UploadFile, File
from typing import List, Optional
import numpy as np
from typing import Union
import pywt
import subprocess
import os
import cv2
from tempfile import NamedTemporaryFile
import shutil
import tempfile
import uuid


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}
            
        
