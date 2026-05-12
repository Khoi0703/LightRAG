from fastapi import FastAPI, Request, Depends, Response
from pydantic import BaseModel
import uvicorn
from lightrag import LightRAG, QueryParam
from lightrag.llm import hf_embedding, zhipu_complete_if_cache
from lightrag.utils import EmbeddingFunc
from transformers import AutoModel, AutoTokenizer
from dotenv import load_dotenv
import os
from uuid import uuid4

load_dotenv()

ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
WORKING_DIR = os.getenv("WORKING_DIR", "./workdir")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

if not ZHIPU_API_KEY:
    raise ValueError("ZHIPU_API_KEY chưa được cấu hình trong file .env")
if not NEO4J_PASSWORD:
    raise ValueError("NEO4J_PASSWORD chưa được cấu hình trong file .env")

os.environ["NEO4J_URI"] = NEO4J_URI
os.environ["NEO4J_USERNAME"] = NEO4J_USERNAME
os.environ["NEO4J_PASSWORD"] = NEO4J_PASSWORD

os.makedirs(WORKING_DIR, exist_ok=True)

# Load embedding model một lần duy nhất khi khởi động
_EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
_tokenizer = AutoTokenizer.from_pretrained(_EMBED_MODEL_NAME)
_embed_model = AutoModel.from_pretrained(_EMBED_MODEL_NAME)


async def llm_model_func(
    prompt, system_prompt=None, history_messages=[], keyword_extraction=False, **kwargs
) -> str:
    return await zhipu_complete_if_cache(
        prompt=prompt,
        model="glm-4-flash",
        system_prompt=system_prompt,
        history_messages=history_messages,
        api_key=ZHIPU_API_KEY,
        **kwargs,
    )


embedding_func = EmbeddingFunc(
    embedding_dim=384,
    max_token_size=5000,
    func=lambda texts: hf_embedding(
        texts,
        tokenizer=_tokenizer,
        embed_model=_embed_model,
    ),
)

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=llm_model_func,
    embedding_func=embedding_func,
    graph_storage="Neo4JStorage",
)

app = FastAPI(title="Voz Forum RAG API")

# In-memory session store (thay bằng Redis cho production)
session_store: dict[str, list] = {}


class Query(BaseModel):
    text: str
    mode: str = "hybrid"


async def get_session_id(request: Request, response: Response) -> str:
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid4())
        response.set_cookie(key="session_id", value=session_id, httponly=True)
    return session_id


@app.post("/chatbot/")
async def chatbot(input: Query, session_id: str = Depends(get_session_id)):
    history_messages = session_store.get(session_id, [])

    response = await rag.aquery(
        input.text,
        param=QueryParam(mode=input.mode),
        history_chat=history_messages,
    )

    history_messages.append({"user": input.text, "bot": response})
    session_store[session_id] = history_messages

    return {"response": response}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
