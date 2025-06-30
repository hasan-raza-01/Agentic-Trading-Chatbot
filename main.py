import uvicorn 
from trading_bot.pipeline.data_ingestion_pipeline import DataIngestionPipeline 
from trading_bot.pipeline.query_pipeline import QueryPipeline 
from fastapi.middleware.cors import CORSMiddleware 
from trading_bot.schema import QuestionRequest
from fastapi import FastAPI, UploadFile, File
from starlette.responses import JSONResponse
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_ingestion_pipeline = DataIngestionPipeline()

# health check 
@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        data_ingestion_pipeline.run(files)
        return {"message": "Files successfully processed and stored."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
query_pipeline = QueryPipeline()

@app.post("/query")
async def query_chatbot(request: QuestionRequest):
    try:
        # Assuming request is a pydantic object like: {"question": "your text"}
        messages={"messages": [request.question]}

        result = query_pipeline.run(messages)
        
        # If result is dict with messages:
        if isinstance(result, dict) and "messages" in result:
            final_output = result["messages"][-1].content  # Last AI response
        else:
            final_output = str(result)
        
        return {"answer": final_output}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

