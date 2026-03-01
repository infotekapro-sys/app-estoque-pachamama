import streamlit as st
import pandas as pd
import os

ARQUIVO_CSV = "estoque.csv"

st.set_page_config(page_title="Controle de Estoque", layout="wide")
st.title("📦 Controle de Estoque Pachamama")

if not os.path.exists(ARQUIVO_CSV):
    df_inicial = pd.DataFrame(columns=["nome", "quantidade", "imagem"])
    df_inicial.to_csv(ARQUIVO_CSV, index=False)

menu = st.sidebar.selectbox(
    "Menu",
    ["Cadastrar Produto", "Ver Estoque"]
)

if menu == "Cadastrar Produto":

    st.subheader("Cadastrar Novo Produto")

    nome = st.text_input("Nome do Produto")
    quantidade = st.number_input("Quantidade", min_value=0, step=1)
    imagem = st.file_uploader("Imagem do Produto", type=["png", "jpg", "jpeg"])

    if st.button("Salvar Produto"):

        if nome and imagem is not None:

            pasta_imagens = "imagens"
            if not os.path.exists(pasta_imagens):
                os.makedirs(pasta_imagens)

            caminho_imagem = os.path.join(pasta_imagens, imagem.name)

            with open(caminho_imagem, "wb") as f:
                f.write(imagem.getbuffer())

            df = pd.read_csv(ARQUIVO_CSV)
            novo = pd.DataFrame([[nome, quantidade, caminho_imagem]],
                                columns=["nome", "quantidade", "imagem"])
            df = pd.concat([df, novo], ignore_index=True)
            df.to_csv(ARQUIVO_CSV, index=False)

            st.success("Produto cadastrado com sucesso!")

        else:
            st.warning("Preencha todos os campos.")

if menu == "Ver Estoque":

    st.subheader("Estoque Atual")

    df = pd.read_csv(ARQUIVO_CSV)

    if df.empty:
        st.info("Nenhum produto cadastrado.")
    else:
        for index, row in df.iterrows():
            col1, col2 = st.columns([1, 3])

            with col1:
                if os.path.exists(row["imagem"]):
                    st.image(row["imagem"], width=120)

            with col2:
                st.write(f"**Produto:** {row['nome']}")
                st.write(f"**Quantidade:** {row['quantidade']}")
                st.markdown("---")
