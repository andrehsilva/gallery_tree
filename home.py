import streamlit as st
import pandas as pd

def app():
    st.header('Annual 2024')
    st.subheader('Mapa da escola e possível Upsell:')
    df = pd.read_excel('dados.xlsx')

    # Cria uma lista de escolas para o selectbox
    escolas = df['School Name'].unique()
    
    # Input para digitar parte do nome da escola
    escola_parte = st.text_input("Pesquise por parte do nome da escola")
    # Filtra a lista de escolas baseado no input
    escolas_filtradas = [escola for escola in escolas if escola_parte.lower() in escola.lower()]
    
    # Adiciona uma opção vazia no início da lista de escolas filtradas
    escolas_filtradas.insert(0, "")

    # Selectbox para escolher a escola das opções filtradas
    escola_selecionada = st.selectbox("Escolha uma escola", escolas_filtradas)
    if escola_selecionada:
        # Filtra o DataFrame pela escola selecionada
        df_filtrado = df[df['School Name'] == escola_selecionada]
        
        # Exibir quantidade de alunos (supondo que a coluna seja 'Número de Alunos')
        ei = df_filtrado['Alunos Educação Infantil'].sum() if 'Alunos Educação Infantil' in df_filtrado.columns else 'Informação não disponível'
        ef1 = df_filtrado['Alunos Educação Anos Iniciais'].sum() if 'Alunos Educação Anos Iniciais' in df_filtrado.columns else 'Informação não disponível'
        ef2 = df_filtrado['Alunos Educação Anos Finais'].sum() if 'Alunos Educação Anos Finais' in df_filtrado.columns else 'Informação não disponível'
        em = df_filtrado['Alunos Ensino Médio'].sum() if 'Alunos Ensino Médio' in df_filtrado.columns else 'Informação não disponível'
        pv = df_filtrado['Alunos Pré Vestibular'].sum() if 'Alunos Pré Vestibular' in df_filtrado.columns else 'Informação não disponível'

        # Criação de colunas para exibir os valores
        col1, col2, col3, col4, col5 = st.columns(5)
        
        col1.metric(label="EI", value=ei)
        col2.metric(label="EFI", value=ef1)
        col3.metric(label="EFII", value=ef2)
        col4.metric(label="EM", value=em)
        col5.metric(label="PV", value=pv)

        st.write(f"{escola_selecionada}")

        # Exibe todos os produtos da escola selecionada
        st.write(f"Marcas contratadas:")
        
        sistemas = df_filtrado.iloc[:, 3:-17]  # Seleciona todas as colunas de produtos a partir da quinta coluna
        st.dataframe(sistemas, hide_index=True)

        # Exibe todos os produtos da escola selecionada
        st.write(f"Produtos da escola:")

        produtos = df_filtrado.iloc[:, 6:-9]  # Seleciona todas as colunas de produtos a partir da quinta coluna
        st.dataframe(produtos, hide_index=True)

        # Exibe todas as novas soluções educacionais
        st.write(f"Novas soluções educacionais:")

        col1, col2, col3, col4 = st.columns(4)
        
        col1.write('Aprova rápido')
        col2.write('Alura Start')
        col3.write('Adapte')
        col4.write('Sponte')
    else:
        st.write("Nenhuma escola encontrada com esse nome.")

if __name__ == "__main__":
    app()
