
from lightrag import LightRAG, QueryParam
from lightrag.llm import hf_model_complete, hf_embedding,zhipu_complete_if_cache
from lightrag.utils import EmbeddingFunc
from transformers import AutoModel, AutoTokenizer
import os
from dotenv import load_dotenv

load_dotenv()
#
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
WORKING_DIR = os.getenv("WORKING_DIR")

# neo4j
BATCH_SIZE_NODES = 500
BATCH_SIZE_EDGES = 100
os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "12345678"




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
embedding_func=EmbeddingFunc(
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
    graph_storage="Neo4JStorage"
)



with open("./book.txt", "r", encoding="utf-8") as f:
    rag.insert(f.read())

# 