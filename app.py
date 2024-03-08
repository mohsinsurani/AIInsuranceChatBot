import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain.embeddings.huggingface import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from htmlTemplates import css, bot_template, user_template


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        print(type(pdf))
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            print(page)
            if page is not None:
                page_text = page.extract_text()
                print(page_text)
                if page_text is not None:
                    text += page_text
    return text


def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=512, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(text_chunks, embeddings)
    return vectorstore


def get_conv_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vectorstore.as_retriever(), memory=memory
    )
    return conversation_chain


def handle_user_input(user_question):
    response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history = response["chat_history"]

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message), unsafe_allow_html=True)
    st.write(response)


def main():
    load_dotenv()
    st.set_page_config(page_title="Multiple PDFs", page_icon=":books:")

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with Multiple PDFs :books:")
    user_question = st.text_input("Ask Question about your Insurance")

    if user_question:
        handle_user_input(user_question)


    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your pdf here and click on Process", accept_multiple_files=True
        )
        if st.button("Process"):
            with st.spinner("Processing"):
                # 1 Get the text of the pdf
                raw_text = get_pdf_text(pdf_docs)
                # 2 Get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # 3 Get the vector store
                text_vector_store = get_vector_store(text_chunks=text_chunks)

                # 4 COnversation chain
                st.session_state.conversation = get_conv_chain(text_vector_store)


if __name__ == "__main__":
    main()
