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
    """
    Schema for the summary request body.

    Attributes:
        mode (int): The mode of input (0: Text, 1: URL, 2: File).
        text (str): The text to be summarized (used when mode is 0 or 2).
        url (str): The URL to fetch and summarize (used when mode is 1).
        sum_len (str): The length of the summary ('short', 'medium', 'long').
    """
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
        if req.mode in [0, 2]:
            toSummarize = req.text
        elif req.mode == 1:
            toSummarize = req.ur
        else:
            raise HTTPException(status_code=400, detail="Invalid mode specified")

        # Generate the summary
        summary_text = summary(req.mode, toSummarize, req.sum_len)

        if summary_text:
            return {"summary": summary_text}
        else:
            raise HTTPException(status_code=422, detail="An error occurred while generating the summary")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))