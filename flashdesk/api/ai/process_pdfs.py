import frappe
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
# import chromadb
from langchain.vectorstores.chroma import Chroma
# from langchain.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama

def process_directory(): 
    # Ideally fetch from system settings doc
    base_url = "https://7f0c-103-123-226-98.ngrok-free.app/"
    ollama = Ollama(base_url=base_url,model="llama2")
    pdf_dir = frappe.get_site_path("private/files/pdffiles/")
    loader = DirectoryLoader(pdf_dir, glob="**/*.pdf", use_multithreading=True)

@frappe.whitelist(allow_guest=True)
def start_processing():
    process_directory()
    return "hello"


