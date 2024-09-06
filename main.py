import streamlit as st
import pandas as pd
from streamlit_modal import Modal

import io

st.set_page_config(page_title="Árvore de Livros & AZ",page_icon="📚",layout="wide")

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

#st.snow()
# st.image('logo-arvore.svg')
st.logo('logo.png')
col1, col2, col3, col4 = st.columns(4)
# Cria um modal com o título
modal = Modal(key="video_modal", title="Aprenda a encontrar livros mapeados na Árvore & AZ")

# Botão para abrir o modal
if col1.button("**Clique aqui para aprender!**"):
    modal.open()

# Conteúdo do modal
if modal.is_open():
    with modal.container():
        st.video("arvore.mp4")
st.header('Mapeamento de Livros Árvore & AZ')
st.subheader('Explore uma coleção completa de livros mapeados com o seu sistema de ensino AZ.')


st.divider()

df = pd.read_excel('dados.xlsx', sheet_name='TODOS OS VOLUMES')
col1, col2, col3, col4 = st.columns(4)
# Filtro composto por TÍTULO (multi-seleção)
titulo_input = col1.multiselect(
    "Selecione um ou mais títulos:", placeholder="Escolha uma opção",
    options=sorted(df['TÍTULO'].unique())  # Ordena os títulos
)
# Filtro composto por AUTOR (multi-seleção) - desabilitado se o filtro de TÍTULO estiver ativo
volume_input = col2.multiselect(
    "Selecione um ou mais volumes:", placeholder="Escolha uma opção",
    options=sorted(df['VOLUME/PROJETO'].unique())
) if not titulo_input else col2.selectbox(
    "Filtro de VOLUME/PROJETO desabilitado devido à seleção de TÍTULO",
    options=[""], disabled=True
)
# Filtro composto por DISCIPLINA (multi-seleção)
disciplina_input = col3.multiselect(
    "Selecione uma ou mais disciplinas:", placeholder="Escolha uma opção",
    options=sorted(df['DISCIPLINA'].unique())  # Ordena as disciplinas
) if not (titulo_input or volume_input) else col3.selectbox(
    "Filtro de DISCIPLINA desabilitado devido à seleção de TÍTULO ou VOLUME/PROJETO", 
    options=[""], disabled=True
)
# Filtro composto por SÉRIE (multi-seleção)
serie_input = col4.multiselect(
    "Selecione uma ou mais séries:", placeholder="Escolha uma opção",
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

# Aplicar a ordenação ANTES do paginamento
categoria_ordem = pd.Categorical(df['DISPONÍVEL NA ÁRVORE'], 
                                 categories=["Sim", "Não, utilizar sugestão", "Não, utilizar obra indicada no material AZ"],
                                 ordered=True)
df = df.sort_values(by='DISPONÍVEL NA ÁRVORE', key=lambda col: categoria_ordem)

# Paginamento
results_per_page = 16
total_pages = len(df) // results_per_page + (1 if len(df) % results_per_page > 0 else 0)

col1, col2, col3, col4 = st.columns(4)
selected_page = col1.selectbox('Selecione a página:', range(1, total_pages + 1))

start_idx = (selected_page - 1) * results_per_page
end_idx = start_idx + results_per_page

# Aplicar o paginamento ao dataframe filtrado e ordenado
page_data = df.iloc[start_idx:end_idx]


# Continuar com a exibição dos cards
# Exibir os resultados em formato de card


if not page_data.empty:
    num_results = len(page_data)
    num_cols = min(4, num_results)  # Limita a 4 colunas no máximo
    cols_per_row = 4  # Definir o número máximo de colunas por linha
    
    for i in range(0, num_results, cols_per_row):
        cols = st.columns(min(cols_per_row, num_results - i))  # Ajustar o número de colunas dinamicamente
        
        for j, row in enumerate(page_data.iloc[i:i+cols_per_row].iterrows()):
            with cols[j]:  # Distribui os cards nas colunas criadas
                # Definir um valor padrão para a cor
                #cor = "gray"
                
                # Construir o HTML do card
                card_html = f"""
                <div style="border: 1px solid #ddd; padding: 0px; border-radius: 5px; margin-bottom: 2px; margin-top: 2px; height: 620px; text-align: center;">
                """
                if row[1]['DISPONÍVEL NA ÁRVORE'] == 'Sim':
                    card_html += f"<div style='background-color: #45d0c1; border: 1px solid #45d0c1; color: #ffffff; padding: 1px; border-radius: 5px 5px 0px 0px; margin-bottom: 5px;'><strong>📗 Livro Disponível</strong></div>"

                # Adicionar sugestão de livro, se houver
                if pd.notna(row[1]['SUGESTÃO DE LIVRO']) and row[1]['SUGESTÃO DE LIVRO'].strip():
                    card_html += f"<div style='background-color: #b36848; border: 1px solid #b36848; color: #ffffff; padding: 1px; border-radius: 5px 5px 0px 0px; margin-bottom: 5px;'><strong>Sugestão</strong></div>"

                if row[1]['DISPONÍVEL NA ÁRVORE'] == 'Não, utilizar obra indicada no material AZ':
                    card_html += f"<div style='background-color: #fdc311; border: 1px solid #fdc311; color: #000000; padding: 1px; border-radius: 5px 5px 0px 0px; margin-bottom: 5px;'><strong>Indisponível</strong></div>"

                # Adicionar a imagem e as demais informações do card
                card_html += f"""
                <img src="{row[1]['LINK DA IMAGEM']}" style="width: 200px; height: auto; display: block; margin-left: auto; margin-right: auto;"/>
                <h4 style="color:#494c4e; margin: 5px 0;">{row[1]['NOME']}</h4>
                <p style="margin: 5px 0;"><strong>{row[1]['DISCIPLINA']} | {row[1]['SÉRIE']} | Volume: {row[1]['VOLUME/PROJETO']}</strong></p>
                """
                
                # Adicionar proposta de leitura original, se houver
                #if pd.notna(row[1]['TÍTULO']) and row[1]['TÍTULO'].strip():
                    
                    #card_html += f"<p style='margin: 5px 0;'><strong>Autor:</strong> {row[1]['AUTOR']}</p>"

                # Adicionar botão com o link do livro
                if row[1]['DISPONÍVEL NA ÁRVORE'] == 'Sim':
                    card_html += f"<p style='margin: 5px 0;'><strong>Autor:</strong> {row[1]['AUTOR']}</p>"
                    cor = "#45d0c1"   
                    texto_cor = "white"
                elif row[1]['DISPONÍVEL NA ÁRVORE'] == 'Não, utilizar sugestão':
                    card_html += f"<p style='margin: 5px 0;'><strong>Proposta de leitura original:</strong> {row[1]['TÍTULO']}</p>"
                    cor = "#b36848"
                    texto_cor = "white"
                elif row[1]['DISPONÍVEL NA ÁRVORE'] == 'Não, utilizar obra indicada no material AZ':
                    cor = "#fdc311"
                    texto_cor = "black"
                
                link = row[1]['LINK DO LIVRO']
                button_label = f"{row[1]['NOME DO BOTÃO']}"
                card_html += f'<div style="text-align: center;"><a href="{link}" target="_blank"><button style="background-color: {cor}; color: {texto_cor}; padding: 10px 20px; border: none; cursor: pointer; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; border-radius: 4px;">{button_label}</button></a></div>'
                
                # Fechar a div do card
                card_html += "</div>"
                
                # Renderizar o HTML no Streamlit
                st.markdown(card_html, unsafe_allow_html=True)
                st.markdown("")
else:
    st.markdown("Nenhum resultado encontrado para os filtros aplicados.")
