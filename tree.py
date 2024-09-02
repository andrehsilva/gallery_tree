import streamlit as st
import pandas as pd


def app():
    st.header('Galeria de Livros')
    st.subheader('Aqui você encontra todos os livros disponíveis mapeados com seu sistema de ensino.')
    df = pd.read_excel('dados.xlsx', sheet_name='TODOS OS VOLUMES')

    st.divider()

    col1, col2 = st.columns(2)
    
    # Filtro composto por TÍTULO
    titulo_input = col1.selectbox(
        "Selecione ou digite um TÍTULO:", 
        options=[""] + list(df['TÍTULO'].unique())
    )

    # Filtro composto por AUTOR - desabilitado se o filtro de TÍTULO estiver ativo
    if titulo_input:
        autor_input = col2.selectbox(
            "Filtro de AUTOR desabilitado devido à seleção de TÍTULO",
            options=[""], disabled=True
        )
    else:
        autor_input = col2.selectbox(
            "Selecione ou digite um AUTOR:", 
            options=[""] + list(df['AUTOR'].unique())
        )

    col3, col4 = st.columns(2)

    # Filtro composto por DISCIPLINA
    if titulo_input or autor_input:
        disciplina_input = col3.selectbox(
            "Filtro de DISCIPLINA desabilitado devido à seleção de TÍTULO ou AUTOR",
            options=[""], disabled=True
        )
    else:
        disciplina_input = col3.selectbox(
            "Selecione ou digite uma DISCIPLINA:", 
            options=[""] + list(df['DISCIPLINA'].unique())
        )

    # Filtro composto por SÉRIE
    if titulo_input or autor_input:
        serie_input = col4.selectbox(
            "Filtro de SÉRIE desabilitado devido à seleção de TÍTULO ou AUTOR",
            options=[""], disabled=True
        )
    else:
        serie_input = col4.selectbox(
            "Selecione ou digite uma SÉRIE:", 
            options=[""] + list(df['SÉRIE'].unique())
        )

    # Aplicar filtros compostos
    if titulo_input:
        df = df[df['TÍTULO'].str.contains(titulo_input, case=False, na=False)]
    if autor_input:
        df = df[df['AUTOR'].str.contains(autor_input, case=False, na=False)]
    if disciplina_input:
        df = df[df['DISCIPLINA'].str.contains(disciplina_input, case=False, na=False)]
    if serie_input:
        df = df[df['SÉRIE'].str.contains(serie_input, case=False, na=False)]

    st.divider()

    # Exibir os resultados em formato de card
    if not df.empty:
        cols = st.columns(4)
        for index, row in df.iterrows():
            with cols[index % 4]:
                st.markdown(f"### {row['TÍTULO']}")
                st.markdown(f"**Autor:** {row['AUTOR']}")
                st.markdown(f"**Disciplina:** {row['DISCIPLINA']}")
                st.markdown(f"**Série:** {row['SÉRIE']}")
                st.markdown(f"**Link:** {row['LINK']}")
                st.markdown("---")
    else:
        st.markdown("Nenhum resultado encontrado para os filtros aplicados.")

if __name__ == "__main__":
    app()

