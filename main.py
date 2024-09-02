import streamlit as st
from streamlit_option_menu import option_menu
import io

import tree


st.set_page_config(
        page_title="Meus produtos Conexia",
        page_icon="large_blue_square",
        layout="wide",
    )


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


##########################################################################################################################################################
##########################################################################################################################################################

if check_password():
    buffer = io.BytesIO()

    with st.sidebar:        
        app = option_menu(
            menu_title='Galeria de livros ',
            options=['Árvore'],
            icons=['folder-fill'],
            menu_icon='book-fill',
            default_index=0,
            styles={
                "container": {"padding": "5!important"},
                "icon": { "font-size": "16px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#F7EFE5"},
                "nav-link-selected": {"background-color": "blue"},}
            )
            
    if app == "Árvore":
        tree.app()

    
    
     
             
