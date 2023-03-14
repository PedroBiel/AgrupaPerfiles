"""
AGRUPA PERFILES

Lee los perfiles de la base de datos EUROPA.db y los agrupa en un único DataFrame de pandas.

El objetivo es poder ordenarlos según los valores de las columnas para poder seleccionar los perfiles más óptimos entre
diferentes tipos de perfil.

Los resultados se muestran con Streamlit.

13/03/2023

__author__ = Pedro Biel
__version__ = 0.0.0
__email__ = pedro.biel@vamanholding.com
"""

import pandas as pd
import sqlite3
import streamlit as st


class MyStreamlit:

    def __init__(self):
        """
        Lee los perfiles laminados en caliente de la base de datos EUROPA.db y los agrupa en un único DataFrame de
        pandas.

        El objetivo es ordenarlos según los valores de las columnas para poder seleccionar los perfiles más óptimos
        entre diferentes tipos de perfil.
        """

        self.db_file = './data/EUROPA.db'

        self.set_page_config()
        self.titulo()
        self.tablas = self.lista_tablas()
        self.perfiles = self.seleccion_perfiles()
        self.dataframe_filtrada()
        self.version()


    def set_page_config(self):
        """Streamlit page config."""

        st.set_page_config(
            page_title='CuentaSilos',
            page_icon=':)',
            layout='wide',
            initial_sidebar_state='expanded',
        )

    def titulo(self):
        """Títulos de las secciones."""

        st.title('Agrupa perfiles')
        st.markdown("""
        Lee los perfiles de la base de datos **EUROPA.db** y los agrupa en un único `DataFrame` de `pandas`.
         
        El objetivo es ordenarlos según los valores de las columnas para poder seleccionar los perfiles más óptimos 
        entre los diferentes tipos de perfil.
        """
        )
        st.sidebar.title('Selección de perfiles')

    def lista_tablas(self):
        """
        Lista con los nombres de las tablas de la base de datos.

        :return: str; lista con los nombres de los perfiles de la base de datos.
        """

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas_fetch = cursor.fetchall()
        tablas = [tabla[0] for tabla in tablas_fetch]
        # st.text(tablas)

        return tablas

    def seleccion_perfiles(self):
        """
        Selección de perfiles.

        :return: str; lista de perfiles seleccionados
        """

        perfiles = st.sidebar.multiselect('Tablas de perfiles:', self.tablas, self.tablas)

        return perfiles

    def dataframe_filtrada(self):
        """
        DataFrame con los perfiles del filtro.

        :return: pandas DataFrame en Streamlit

        """

        df = pd.DataFrame()
        conn = sqlite3.connect(self.db_file)
        for perfil in self.perfiles:
            df_db = pd.read_sql('SELECT * FROM ' + perfil + ';', conn)
            if df.empty:
                df = df_db.copy()
            else:
                df = pd.concat([df, df_db])

        st.write(df)

    def version(self):
        """Versión de las librerías."""

        st.subheader('Versión')
        with st.expander('AgrupaPerfiles 0.0.0'):
            st.markdown(
                """
                | Versión | Comentario |
                | --- | --- |
                | 0.0.0 | Primera edición |

                ---

                | Librería | Versión |
                | --- | --- |
                | pandas | 1.5.3 |
                | python | 3.9.16 |
                | sqlite | 3.40.1 |
                | streamlit | 1.20.0 |
                """)


if __name__ == '__main__':

    myst = MyStreamlit()
