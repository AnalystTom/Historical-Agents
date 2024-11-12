from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, field_validator
from typing import List, Union
from transformers import AutoTokenizer, AutoModel
import torch
import uvicorn
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
import pymongo
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    handlers=[logging.FileHandler("app.log"),
                              logging.StreamHandler()])
logger = logging.getLogger(__name__)

# FastAPI application
app = FastAPI()

# Device setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load English embedding model
MODEL_PATH = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModel.from_pretrained(MODEL_PATH).to(device)
model.eval()

# MongoDB connection setup
MONGO_URI = "your_mongodb_atlas_connection_uri"
client = pymongo.MongoClient(MONGO_URI)
db = client["historical_dialogues"]
collection = db["dialogue_logs"]

# Pydantic model for input data
class TextData(BaseModel):
    text: Union[str, List[str]]
    role: str
    turn: int

    @field_validator('text')
    def convert_string_to_list(cls, v):
        if isinstance(v, str):
            return [v]
        return v

async def async_compute_embeddings(texts: List[str]):
    '''Asynchronously compute sentence embeddings'''
    try:
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            encoded_input = await loop.run_in_executor(pool, lambda: tokenizer(texts,
                                                                               padding=True,
                                                                               truncation=True,
                                                                               return_tensors="pt",
                                                                               max_length=512).to(device))
            with torch.no_grad():
                outputs = await loop.run_in_executor(pool, lambda: model(**encoded_input))
                sentence_embeddings = outputs[0][:, 0]
                sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)
            return sentence_embeddings.cpu().numpy().tolist()
    except Exception as e:
        logger.error(f"Error in embedding computation: {e}", exc_info=True)

@app.post("/embeddings/")
async def get_embeddings(request: Request, text_data: TextData):
    try:
        logger.info(f"Received request: {await request.json()}")
        embeddings = await async_compute_embeddings(text_data.text)

        # Prepare the document to be stored in MongoDB
        log_entry = {
            "role": text_data.role,
            "turn": text_data.turn,
            "context": text_data.text,
            "embeddings": embeddings,
            "timestamp": datetime.utcnow()
        }

        # Insert the document into MongoDB
        collection.insert_one(log_entry)
        logger.info("Log entry successfully stored in MongoDB")

        return {"message": "Embedding computed and log entry stored", "embeddings": embeddings}
    except Exception as e:
        logger.error(f"Error in request processing: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
