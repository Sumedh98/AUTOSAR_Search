import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


# Create a Chromdb to store embeddings
chroma_client = chromadb.PersistentClient(path = "database")

# Create a collection with Google Gemeni API for embedding
google_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key="AIzaSyCymU7yIntvND2XceqMMJl1ysu0SM51k00", task_type="RETRIEVAL_DOCUMENT")
collection = chroma_client.get_or_create_collection(name="autosar_book", embedding_function=google_ef)

# Load all the PDFs to be read for embeddding  
loader = PyPDFDirectoryLoader("data/book")
raw_docs = loader.load()
print(raw_docs[0])

#split the docs
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)
chunks = text_splitter.split_documents(raw_docs)

print(len(chunks))

# Upsert the documents to chromdb in batches
BATCH_SIZE = 50
documents = []
ids = []
metadata = []
i=0
for chunk in chunks:
    documents.append(chunk.page_content)
    ids.append("ID" + str(i))
    metadata.append(chunk.metadata)
    i += 1
    print(i)
    if len(documents) == BATCH_SIZE:
        print("Adding batch to collection")
        collection.upsert(documents=documents, metadatas=metadata, ids=ids)
        print(f"Added batch up to {i} to collection")
        documents = []
        ids = []
        metadata = []


# Upsert any remaining documents after the loop
if documents:
    collection.upsert(documents=documents, metadatas=metadata, ids=ids)
    print(f"Added final batch up to {i} to collection")    
