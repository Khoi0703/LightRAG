from fastapi import FastAPI, Request, Depends, Response
from pydantic import BaseModel
import uvicorn
from lightrag import LightRAG, QueryParam
from lightrag.llm import hf_model_complete, hf_embedding, zhipu_complete_if_cache
from lightrag.utils import EmbeddingFunc
from transformers import AutoModel, AutoTokenizer
from dotenv import load_dotenv
import os
from uuid import uuid4

load_dotenv()
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
WORKING_DIR = os.getenv("WORKING_DIR")

# Neo4j Config
os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "12345678"

# In-Memory Cache using Dictionary
session_store = {}

# LLM Model
async def llm_model_func(
    prompt, system_prompt=None, history_messages=[], keyword_extraction=False, **kwargs
) -> str:
    return await zhipu_complete_if_cache(
        prompt=prompt,
        model="glm-4-flash",
        system_prompt=system_prompt,
        history_messages=history_messages,
        api_key=ZHIPU_API_KEY,
        **kwargs
    )

embedding_func = EmbeddingFunc(
    embedding_dim=384,
    max_token_size=5000,
    func=lambda texts: hf_embedding(
        texts,
        tokenizer=AutoTokenizer.from_pretrained(
            "sentence-transformers/all-MiniLM-L6-v2"
        ),
        embed_model=AutoModel.from_pretrained(
            "sentence-transformers/all-MiniLM-L6-v2"
        ),
    ),
)

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=llm_model_func,
    embedding_func=embedding_func,
    graph_storage="Neo4JStorage",
)

app = FastAPI()

# Request Schema
class Query(BaseModel):
    text: str
    mode: str


async def get_session_id(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid4())
        response.set_cookie(key="session_id", value=session_id, httponly=True)
    return session_id

@app.post("/chatbot/")
async def chatbot(input: Query, session_id: str = Depends(get_session_id)):
    # Lấy lịch sử từ In-Memory Cache (Dictionary)
    history_messages = session_store.get(session_id, [])

    # Gọi RAG với lịch sử
    response = await rag.aquery(
        input.text,
        param=QueryParam(mode=input.mode), history_chat=history_messages
    )

    # Cập nhật lịch sử
    history_messages.append({"user": input.text, "bot": response})
    session_store[session_id] = history_messages

    return {"response": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
