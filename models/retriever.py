# # from sentence_transformers import SentenceTransformer
# # from chromadb import PersistentClient
# # import os

# # def process_knowledge_base():
# #     # Load knowledge base text
# #     kb_file_path = os.path.join('data', 'knowledge_base.txt')
# #     with open(kb_file_path, 'r', encoding='utf-8') as f:
# #         kb_text = f.read()

# #     # Chunk by paragraphs (double newlines)
# #     chunks = [chunk.strip() for chunk in kb_text.split('\n\n') if chunk.strip()]

# #     # Initialize embedding model
# #     model = SentenceTransformer('all-MiniLM-L6-v2')
# #     embeddings = model.encode(chunks)

# #     # Set up ChromaDB client and collection
# #     client = PersistentClient(path="./chroma_db")

# #     try:
# #         collection = client.get_collection(name="insurance_kb")
# #     except:
# #         collection = client.create_collection(name="insurance_kb")

# #     # Add documents to collection
# #     ids = [f"doc_{i}" for i in range(len(chunks))]
# #     metadatas = [{"source": "knowledge_base.txt", "chunk_index": i} for i in range(len(chunks))]
# #     collection.add(
# #         documents=chunks,
# #         embeddings=embeddings.tolist(),
# #         ids=ids,
# #         metadatas=metadatas
# #     )
# #     print("Knowledge base processed and stored in ChromaDB.")

# # if __name__ == "__main__":
# #     process_knowledge_base()

# from sentence_transformers import SentenceTransformer
# from chromadb import PersistentClient
# import os

# # def process_knowledge_base():
# #     # Load knowledge base text
# #     kb_file_path = os.path.join('data', 'knowledge_base.txt')
# #     with open(kb_file_path, 'r', encoding='utf-8') as f:
# #         kb_text = f.read()

# #     # Chunk by paragraphs (double newlines)
# #     chunks = [chunk.strip() for chunk in kb_text.split('\n\n') if chunk.strip()]

# #     # Initialize embedding model
# #     model = SentenceTransformer('all-MiniLM-L6-v2')
# #     embeddings = model.encode(chunks)

# #     # Set up ChromaDB client and collection
# #     client = PersistentClient(path="./chroma_db")

# #     try:
# #         collection = client.get_collection(name="insurance_kb")
# #     except:
# #         collection = client.create_collection(name="insurance_kb")

# #     # Add documents to collection
# #     ids = [f"doc_{i}" for i in range(len(chunks))]
# #     metadatas = [{"source": "knowledge_base.txt", "chunk_index": i} for i in range(len(chunks))]
# #     collection.add(
# #         documents=chunks,
# #         embeddings=embeddings.tolist(),
# #         ids=ids,
# #         metadatas=metadatas
# #     )
# #     print("✅ Knowledge base processed and stored in ChromaDB.")

# def process_knowledge_base():
#     import re
#     # Splits text on lines starting with numbers (like '1. ...', '2. ...')
#     sections = re.split(r'\n\s*(\d+\.\s)', text)
#     chunks = []

#     # Recombine numbered titles with content
#     for i in range(1, len(sections), 2):
#         title = sections[i].strip()
#         content = sections[i + 1].strip()
#         full = f"{title} {content}"
#         chunks.append(full)
    
#     return chunks


# # def query_knowledge_base(query):
# #     from sentence_transformers import SentenceTransformer
# #     from chromadb import PersistentClient

# #     # Load embedding model
# #     model = SentenceTransformer('all-MiniLM-L6-v2')

# #     # Connect to ChromaDB client and collection
# #     client = PersistentClient(path="./chroma_db")
# #     collection = client.get_collection(name="insurance_kb")

# #     # Encode the user query
# #     query_embedding = model.encode([query])

# #     # Search for relevant chunks
# #     results = collection.query(
# #         query_embeddings=query_embedding.tolist(),
# #         n_results=3
# #     )

#     # Return top 3 matching chunks (as a flat list)
#     # return results['documents'][0]

# def query_knowledge_base(query, top_k=3):
#     from sentence_transformers import SentenceTransformer
#     from chromadb import PersistentClient

#     model = SentenceTransformer('all-MiniLM-L6-v2')
#     client = PersistentClient(path="./chroma_db")
#     collection = client.get_collection(name="insurance_kb")

#     query_embedding = model.encode([query])
#     results = collection.query(
#         query_embeddings=query_embedding.tolist(),
#         n_results=top_k
#     )

#     return results["documents"][0]  # A list of top-k strings


# if __name__ == "__main__":
#     # Rebuild the database if needed
#     process_knowledge_base()

#     # Test a query
#     print("\n🔍 Sample Query Result:")
#     results = query_knowledge_base("What is my premium due date?")
#     for i, doc in enumerate(results, 1):
#         print(f"{i}. {doc}")


# model = SentenceTransformer('all-MiniLM-L6-v2')
# chroma = PersistentClient(path="./chroma_db")
# kb = chroma.get_collection("insurance_kb")

# def retrieve_facts(query, top_k=3):
#     emb = model.encode([query])
#     res = kb.query(query_embeddings=emb.tolist(), n_results=top_k)
#     return res["documents"][0] if res["documents"] else []




from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
import os

# Load model once
_model = SentenceTransformer("all-MiniLM-L6-v2")
_client = PersistentClient(path="./chroma_db")
_collection = _client.get_collection("insurance_kb")

def retrieve_facts(query: str, top_k=3):
    embedding = _model.encode([query])
    results = _collection.query(query_embeddings=embedding.tolist(), n_results=top_k)
    return results["documents"][0] if results and results["documents"] else []
