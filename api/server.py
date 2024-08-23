from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys

# Add the model path to sys.path to import the model
sys.path.insert(0, 'C:\Storage\Codes\py_projects\summarizer')
from model import summary

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="templates"), name="static")

class SummaryRequest(BaseModel):
    mode: int
    text: str = ''
    url: str = ''
    sum_len: str = 'medium'

@app.get("/")
async def root():
    return FileResponse("./templates/index.html")


@app.post("/summary")
async def get_summary(req: SummaryRequest):
    try:
        if req.mode == 0 and req.text == '':
            raise HTTPException(status_code=400, detail="Text is required for mode 0 (user input)")
        summary_text = summary(req.mode, req.text, req.url, req.sum_len)
        
        return {summary_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))