import streamlit as st


def main():
    st.set_page_config(page_title="Mutlitple pdfs", page_icon=":books:")
    st.header("Chat with Multiple PDFs :books:")
    st.text_input("Ask Question about your Insurance")

    with st.sidebar:
        st.subheader("Your documents")
        st.file_uploader("Upload your pdf here and click on Process")
        st.button("Process")

    if __name__ == "__main__":
        main()
