import streamlit as st
import pandas as pd

def app():
    st.image('logo-arvore.svg')
    st.header('Galeria de Livros')
    st.subheader('Aqui você encontra todos os livros disponíveis mapeados com seu sistema de ensino.')
    st.divider()

    df = pd.read_excel('dados.xlsx', sheet_name='TODOS OS VOLUMES')

    col1, col2 = st.columns(2)

    # Filtro composto por TÍTULO (multi-seleção)
    titulo_input = col1.multiselect(
        "Selecione um ou mais TÍTULOS:", 
        options=df['TÍTULO'].unique()
    )

    # Filtro composto por AUTOR (multi-seleção) - desabilitado se o filtro de TÍTULO estiver ativo
    autor_input = col2.multiselect(
        "Selecione um ou mais AUTORES:", 
        options=df['AUTOR'].unique()
    ) if not titulo_input else col2.selectbox(
        "Filtro de AUTOR desabilitado devido à seleção de TÍTULO",
        options=[""], disabled=True
    )

    col3, col4 = st.columns(2)

    # Filtro composto por DISCIPLINA (multi-seleção)
    disciplina_input = col3.multiselect(
        "Selecione uma ou mais DISCIPLINAS:", 
        options=df['DISCIPLINA'].unique()
    ) if not (titulo_input or autor_input) else col3.selectbox(
        "Filtro de DISCIPLINA desabilitado devido à seleção de TÍTULO ou AUTOR",
        options=[""], disabled=True
    )

    # Filtro composto por SÉRIE (multi-seleção)
    serie_input = col4.multiselect(
        "Selecione uma ou mais SÉRIES:", 
        options=df['SÉRIE'].unique()
    ) if not (titulo_input or autor_input) else col4.selectbox(
        "Filtro de SÉRIE desabilitado devido à seleção de TÍTULO ou AUTOR",
        options=[""], disabled=True
    )

    # Aplicar filtros compostos
    if titulo_input:
        df = df[df['TÍTULO'].isin(titulo_input)]
    if autor_input:
        df = df[df['AUTOR'].isin(autor_input)]
    if disciplina_input:
        df = df[df['DISCIPLINA'].isin(disciplina_input)]
    if serie_input:
        df = df[df['SÉRIE'].isin(serie_input)]

    st.divider()

    # Exibir os resultados em formato de card
    if not df.empty:
        # Determinar o número de colunas necessário baseado no número de resultados
        num_results = len(df)
        num_cols = min(4, num_results)  # Limita a 4 colunas no máximo
        cols = st.columns(num_cols)  # Cria o layout dinâmico de colunas
        
        for index, row in df.iterrows():
            with cols[index % num_cols]:  # Distribui os cards nas colunas criadas
                st.image(f"{row['IMAGE']}")
                st.markdown(f"### {row['TÍTULO']}")
                st.markdown(f"**Autor:** {row['AUTOR']}")
                st.markdown(f"**Disciplina:** {row['DISCIPLINA']}")
                st.markdown(f"**Série:** {row['SÉRIE']}")
                st.markdown(f"**Disponível:** {row['DISPONÍVEL']}")
                st.markdown(f"**Sugestão:** {row['COMENTÁRIO']}")
             
                link = row['LINK']
                button_label = f"Acesse: {row['TÍTULO']}"
                button_html = f'<a href="{link}" target="_blank"><button style="background-color: #5353ec; color: white; padding: 10px 20px; border: none; cursor: pointer; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; border-radius: 4px;">{button_label}</button></a>'
                st.markdown(button_html, unsafe_allow_html=True)

                st.markdown("---")
    else:
        st.markdown("Nenhum resultado encontrado para os filtros aplicados.")

if __name__ == "__main__":
    app()
