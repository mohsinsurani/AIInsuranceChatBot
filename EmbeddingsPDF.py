from PyPDF2 import PdfReader
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain.embeddings.huggingface import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS, Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import pickle
import os.path
import torch


class EmbeddingsPDF:
    file = "healthInsurance.pdf"

    @staticmethod
    def get_pdf_text(pdf_docs):
        text = ""
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                if page is not None:
                    page_text = page.extract_text()
                    if page_text is not None:
                        text += page_text
        return text

    @staticmethod
    def get_text_chunks(raw_text):
        text_splitter = CharacterTextSplitter(
            separator="\n", chunk_size=512, chunk_overlap=200, length_function=len
        )
        chunks = text_splitter.split_text(raw_text)
        return chunks

    def get_rec_chunks(self, raw_text):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)
        texts_chunks = text_splitter.split_text(raw_text)
        return texts_chunks

    def get_vector_store(self, text_chunks):
        file_path = "embed.pickle"
        if os.path.isfile(file_path):
            vectorstore = pickle.load(file_path)
            return vectorstore
        else:
            embeddings = HuggingFaceInstructEmbeddings(
                model_name="hkunlp/instructor-xl"
            )
            vectorstore = FAISS.from_texts(text_chunks, embeddings)
            with open(file_path, "wb") as file:
                pickle.dump(vectorstore, file)
            return vectorstore

    def get_embeddings(self):
        file_path = "embed.pickle"
        if os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                vectorstore = pickle.load(file)
                return vectorstore
        else:
            # 1 Get the text of the pdf
            pdf_docs = open(file, "rb")
            raw_text = self.get_pdf_text([pdf_docs])
            # 2 Get the text chunks
            text_chunks = self.get_text_chunks(raw_text)

            # 3 Get the vector store
            text_vector_store = self.get_vector_store(text_chunks=text_chunks)
            return text_vector_store

    def get_chroma_embeddings(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"

        embeddings = HuggingFaceEmbeddings(
            model_name="thenlper/gte-large",
            model_kwargs={"device": device},
            encode_kwargs={"normalize_embeddings": True},
        )
        if os.path.isdir("db"):
            vectordb = Chroma(persist_directory="db", embedding_function=embeddings)
            return vectordb
        else:
            pdf_docs = open(self.file, "rb")
            raw_text = self.get_pdf_text([pdf_docs])
            # 2 Get the text chunks
            text_chunks = self.get_rec_chunks(raw_text)
            db = Chroma.from_texts(text_chunks, embeddings, persist_directory="db")
            return db
