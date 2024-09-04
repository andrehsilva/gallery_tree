import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import io

def app():
    st.image('logo-arvore.svg')
    st.header('Mapeamento de Livros Árvore & AZ')
    st.subheader('Explore uma coleção completa de livros mapeados com o seu sistema de ensino AZ.')
    st.divider()

    df = pd.read_excel('dados.xlsx', sheet_name='TODOS OS VOLUMES')

    col1, col2 = st.columns(2)

    # Filtro composto por TÍTULO (multi-seleção)
    titulo_input = col1.multiselect(
        "Selecione um ou mais TÍTULOS:", 
        options=sorted(df['TÍTULO'].unique())  # Ordena os títulos
    )

    # Filtro composto por AUTOR (multi-seleção) - desabilitado se o filtro de TÍTULO estiver ativo
    volume_input = col2.multiselect(
        "Selecione um ou mais Volumes:", 
        options=sorted(df['VOLUME/PROJETO'].unique())
    ) if not titulo_input else col2.selectbox(
        "Filtro de VOLUME/PROJETO desabilitado devido à seleção de TÍTULO",
        options=[""], disabled=True
    )

    col3, col4 = st.columns(2)

    # Filtro composto por DISCIPLINA (multi-seleção)
    disciplina_input = col3.multiselect(
        "Selecione uma ou mais DISCIPLINAS:", 
        options=sorted(df['DISCIPLINA'].unique())  # Ordena as disciplinas
    ) if not (titulo_input or volume_input) else col3.selectbox(
        "Filtro de DISCIPLINA desabilitado devido à seleção de TÍTULO ou VOLUME/PROJETO",
        options=[""], disabled=True
    )

    # Filtro composto por SÉRIE (multi-seleção)
    serie_input = col4.multiselect(
        "Selecione uma ou mais SÉRIES:", 
        options=df['SÉRIE'].unique()
    ) if not (titulo_input or volume_input) else col4.selectbox(
        "Filtro de SÉRIE desabilitado devido à seleção de TÍTULO ou VOLUME/PROJETO",
        options=[""], disabled=True
    )

    # Aplicar filtros compostos
    if titulo_input:
        df = df[df['TÍTULO'].isin(titulo_input)]
    if volume_input:
        df = df[df['VOLUME/PROJETO'].isin(volume_input)]
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
                # Construir o HTML do card
                card_html = f"""
                <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                    <img src="{row['LINK DA IMAGEM']}" style="width: 200px; height: auto;"/>
                    <h3>{row['TÍTULO']}</h3>
                    <p><strong>Autor:</strong> {row['AUTOR']}</p>
                    <p><strong>Disciplina:</strong> {row['DISCIPLINA']}</p>
                    <p><strong>Série:</strong> {row['SÉRIE']}</p>
                    <p><strong>Volume:</strong> {row['VOLUME/PROJETO']}</p>
                    <p><strong>Disponível:</strong> {row['DISPONÍVEL NA ÁRVORE']}</p>
                """

                # Adicionar sugestão de livro, se houver
                if pd.notna(row['SUGESTÃO DE LIVRO']) and row['SUGESTÃO DE LIVRO'].strip():
                    card_html += f"<p><strong>Sugestão:</strong> {row['SUGESTÃO DE LIVRO']}</p>"

                # Adicionar botão com o link do livro
                if row['DISPONÍVEL NA ÁRVORE'] == 'Sim':
                    cor = "#2b961f"
                    texto_cor = "white"
                elif row['DISPONÍVEL NA ÁRVORE'] == 'Não, utilizar sugestão':
                    cor = "#0000ff"
                    texto_cor = "white"
                elif row['DISPONÍVEL NA ÁRVORE'] == 'Não, utilizar obra indicada no material AZ':
                    cor = "#e5e619"
                    texto_cor = "black"
                
                link = row['LINK DO LIVRO']
                button_label = f"{row['NOME DO BOTÃO']}"
                card_html += f'<a href="{link}" target="_blank"><button style="background-color: {cor}; color: {texto_cor}; padding: 10px 20px; border: none; cursor: pointer; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; border-radius: 4px;">{button_label}</button></a>'
                
                # Fechar a div
                card_html += "</div>"

                # Renderizar o HTML no Streamlit
                st.markdown(card_html, unsafe_allow_html=True)
                st.markdown("")
    else:
        st.markdown("Nenhum resultado encontrado para os filtros aplicados.")

if __name__ == "__main__":
    app()
