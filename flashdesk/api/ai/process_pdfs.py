import frappe
import os
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
import chromadb
from langchain.vectorstores.chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain.callbacks.manager import CallbackManagerForLLMRun



def create_vector_db():
    pdf_dir = frappe.get_site_path("private/files/pdffiles/")

    loader = PyPDFDirectoryLoader(pdf_dir)
    documents = loader.load()
    base_url = "http://192.168.192.194:11434"
    print(f"Processed {len(documents)} pdf files")
    chromadb_path = frappe.get_site_path("private/files/chromadb/")
    

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=200)

    texts=text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(documents=texts, embedding=OllamaEmbeddings(base_url=base_url, model="llama2"),persist_directory=os.path.abspath(chromadb_path))      
    vectorstore.persist()

def fetch_info(query):
    print("sadasd")
    base_url = "http://192.168.192.194:11434"
    ollama = Ollama(base_url=base_url,model="llama2")
    oembed = OllamaEmbeddings(base_url=base_url, model="llama2")
    chromadb_path = frappe.get_site_path("private/files/chromadb/")
    vectordb = Chroma(persist_directory=os.path.abspath(chromadb_path), embedding_function=oembed)
    qachain=RetrievalQA.from_chain_type(ollama, retriever=vectordb.as_retriever())
    docs = vectordb.similarity_search(query, k = 2)
    print(len(docs))
    return qachain.invoke(query)['result']

    



@frappe.whitelist(allow_guest=True)
def start_processing():
    frappe.enqueue(
        create_vector_db,
        queue="default",  # one of short, default, long
        timeout=None,  # pass timeout manually
        now=False,  # if this is True, method is run directly (not in a worker)
        job_name= f"Generating Emebeding",  # specify a job name
        enqueue_after_commit=False,  # enqueue the job after the database commit is done at the end of the request
        at_front=False,  # put the job at the front of the queue
    )


    return {"status": "success", "message": "The embedding process has started in the background. Please check Events for more informstion."}

@frappe.whitelist(allow_guest=True)
def fetch_answer(query):
    print(frappe.request.get_json())
    return fetch_info(query)


