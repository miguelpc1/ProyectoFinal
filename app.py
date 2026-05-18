import pandas as pd
import streamlit as st
import numpy as np
import io
import matplotlib.pyplot as plt
import seaborn as sns

#clase creada para el analisis
class DataAnalyzer:

    def __init__(self, df):
        self.df = df

    def clasifVariables(self):
        numericos = self.df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categoricos = self.df.select_dtypes(include=['object']).columns.tolist()
        return numericos, categoricos

    def descriptive_statistics(self):
        return self.df.describe()

    def missing_values(self):
        return self.df.isnull().sum()


st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("Menú Principal")
opcion= st.sidebar.selectbox(
    "Selecciona una opción para navegar por la app",
    ["Home","Visualizar dataset","Análisis exploratorio"]
)   


def home():

    st.markdown("""
    <style>
        [data-testid="column"] img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        }
    </style>
    """, unsafe_allow_html=True)

    img1,img2=st.columns(2)

   # with img1:
   #     st.image("dmcLogo.png",width=100)

    #with img2:
     #   st.image("logoPython.jpg",width=100)

    st.title("Proyecto Final - Insurance Company Analytics")
    st.write("""El objetivo del anáisis es detectar la probabilidad que existe de que cliente pueda" \
            pueda renovar su póliza """)
    st.write("Nombre completo: Miguel Eugenio Poma Cerron")
    st.write("""Nombre del curso: Especialización Python for Anaytics "
                \nAño: 2026
                \nExplicación del dataset: El dataset utilizado para la exploración de datos información valiosa en la toma de decisiones para los ejecutivos de una empresa aseguradora """)
    st.write("Tecnologías utilizadas: Streamlit, Numpy, Python, Pandas")



def visualizar():

    st.title("Cargar dataset a mostrar")

    uploaded_file = st.file_uploader("Cargar archivo CSV", type=["csv"])

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.success("Archivo cargado correctamente")

        st.subheader("Vista previa")
        st.dataframe(df.head())

        st.subheader("Dimensiones del dataset")
        st.write(f"Filas: {df.shape[0]}")
        st.write(f"Columnas: {df.shape[1]}")

    else:
        st.warning("Por favor cargue un archivo CSV")


def analisis():

    st.title("Análisis Exploratorio de Datos (EDA)")

    uploaded_file = st.file_uploader("Cargar archivo CSV para análisis", type=["csv"])

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        analisis = DataAnalyzer(df)

        numerical_cols, categorical_cols = analisis.clasifVariables()

        tabs = st.tabs([
            "Item 1",
            "Item 2",
            "Item 3",
            "Item 4",
            "Item 5",
            "Item 6",
            "Item 7",
            "Item 8",
            "Item 9",
            "Item 10"
        ])

        with tabs[0]:

            st.header("Item 1 - Información General del Dataset")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Tipos de Datos")
                st.dataframe(df.dtypes.astype(str))

            with col2:
                st.subheader("Valores Nulos")
                st.dataframe(df.isnull().sum())

            st.subheader("Información General")

            buffer = io.StringIO()
            df.info(buf=buffer)
            s = buffer.getvalue()
            st.text(s)

        with tabs[1]:
            st.header("Item 2 - Clasificación de Variables")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Variables Numéricas")
                st.write(numerical_cols)
                st.write(f"Cantidad: {len(numerical_cols)}")
            with col2:
                st.subheader("Variables Categóricas")
                st.write(categorical_cols)
                st.write(f"Cantidad: {len(categorical_cols)}")
            
        with tabs[2]:

            st.header("Item 3 - Estadísticas Descriptivas")
            st.subheader("Resumen Estadístico")
            nombres_columnas = {
                "id": "Id de cliente",
                "perc_premium_paid_by_cash_credit": "% de prima pagada",
                "age_in_days": "Edad en días",
                "Income": "Ingreso mensual",
                "Count_3-6_months_late": "Pagos demorados entre 3 y 6 meses",
                "Count_6-12_months_late": "Pagos demorados entre 6 y 12 meses",
                "Count_more_than_12_months_late": "Pagos demorados + 12 meses",
                "application_underwriting_score": "Nivel de riesgo o confiabilidad",
                "no_of_premiums_paid": "Número total de primas pagadas",
                "premium": "Valor monetario de la prima",
                "renewal": "Renovación de póliza"
            }

            describe_df = df.describe()
            describe_df = describe_df.rename(columns=nombres_columnas)

            st.dataframe(describe_df)


            st.subheader("Análisis Descriptivo")

            st.write("""
            - La variable Renovación de póliza presenta una media de 0.93, lo cual indica que que el 93"%" de los clientes actuales renuevan su póliza.
                     
            - En la variable Valor monetario de prima el cual cuenta con una media de 10924 y una mediana de 7500, el cual indica una diferencia considerable
              en los montos que pagan cada cliente.
                     
            - La edad promedio en días es de 18846, el cual en años es 51 años. Esto demuestra que gran parte de los clientes de edad adulta.
            
            - La variable Ingreso mensual presenta una dispersión considerable, el cual demuestra una variación considerable en
              el ingreso mensual de los clientes.
                     
            - La variable de Nivel de riesgo o confiabilidad presenta una menor dispersión, el cual
              indica que se presenta una puntuación similar entre los clientes.
            """)

        with tabs[3]:

            st.header("Item 4 - Análisis de Valores Faltantes")
            faltante = df.isnull().sum()
            faltante_df = pd.DataFrame({
                "Variable": faltante.index,
                "Valores Faltantes": faltante.values,
                "Porcentaje (%)": np.round((faltante.values / len(df)) * 100, 2)
            })

            st.subheader("Tabla de Valores Faltantes")

            st.dataframe(faltante_df, hide_index=True)
            fig, ax = plt.subplots(figsize=(10,4))

            plt.bar(faltante_df["Variable"], faltante_df["Valores Faltantes"])

            plt.xticks(rotation=90)

            st.pyplot(fig)

            columnasProb = faltante_df[
                faltante_df["Valores Faltantes"] > 0
            ]

            st.subheader("Columnas que requieren limpieza")

            if len(columnasProb) > 0:

                st.dataframe(columnasProb, hide_index=True)
                st.write("""
                Las columnas mostradas presentan valores faltantes,
                por lo cual se requiere realizar un proceso de limpieza.
                """)
            else:
                st.success("El dataset no presenta valores faltantes.")

        with tabs[4]:

            st.header("Item 5 - Distribución de Variables Numéricas")
            nombres_columnas = {
                "id": "Id de cliente",
                "perc_premium_paid_by_cash_credit": "% de prima pagada",
                "age_in_days": "Edad en días",
                "Income": "Ingreso mensual",
                "Count_3-6_months_late": "Pagos demorados entre 3 y 6 meses",
                "Count_6-12_months_late": "Pagos demorados entre 6 y 12 meses",
                "Count_more_than_12_months_late": "Pagos demorados + 12 meses",
                "application_underwriting_score": "Nivel de riesgo o confiabilidad",
                "no_of_premiums_paid": "Número total de primas pagadas",
                "premium": "Valor monetario de la prima",
                "renewal": "Renovación de póliza"
            }

            columnas_visibles = [
                nombres_columnas[col]
                for col in numerical_cols
            ]

            varVisible = st.selectbox(
                "Seleccione variable numérica",
                columnas_visibles
            )

            # Obtener nombre real de la columna
            varReal = [
                key for key, value in nombres_columnas.items()
                if value == varVisible
            ][0]

            # Histograma
            fig, ax = plt.subplots(figsize=(8,4))

            sns.histplot(df[varReal], kde=True, ax=ax)

            ax.set_xlabel("")

            st.pyplot(fig)

            # Estadísticas dinámicas
            st.write(f"""
            La variable seleccionada ({varVisible}) presenta una media de 
            {round(df[varReal].mean(),2)} y una mediana de 
            {round(df[varReal].median(),2)}.
            """)

        
        with tabs[5]:

            st.header("Item 6 - Variables Categóricas")
            nombres_columnas = {
                "id": "Id de cliente",
                "perc_premium_paid_by_cash_credit": "% de prima pagada",
                "age_in_days": "Edad en días",
                "Income": "Ingreso mensual",
                "Count_3-6_months_late": "Pagos demorados entre 3 y 6 meses",
                "Count_6-12_months_late": "Pagos demorados entre 6 y 12 meses",
                "Count_more_than_12_months_late": "Pagos demorados + 12 meses",
                "application_underwriting_score": "Nivel de riesgo o confiabilidad",
                "no_of_premiums_paid": "Número total de primas pagadas",
                "sourcing_channel": "Canal de captación",
                "residence_area_type": "Tipo de área de residencia",
                "premium": "Valor monetario de la prima",
                "renewal": "Renovación de póliza"
            }

            colVisibles = [
                nombres_columnas[col]
                for col in categorical_cols
            ]

            varVisible = st.selectbox(
                "Seleccione variable categórica",
                colVisibles
            )

            # Obtener nombre real
            variable_real = [
                key for key, value in nombres_columnas.items()
                if value == varVisible
            ][0]

            # Conteo de categorías
            counts = df[variable_real].value_counts()

            # DataFrame personalizado
            counts_df = pd.DataFrame({
                "Categoría": counts.index,
                "Cantidad de Clientes": counts.values,
                "Porcentaje (%)": np.round((counts.values / len(df)) * 100, 2)
            })

            st.subheader("Frecuencia de Categorías")

            st.dataframe(counts_df, hide_index=True)

            # Gráfico
            fig, ax = plt.subplots(figsize=(6,4))

            plt.bar(
                counts_df["Categoría"],
                counts_df["Cantidad de Clientes"]
            )

            ax.set_xlabel("")
            ax.set_ylabel("")

            plt.xticks(rotation=45)

            st.pyplot(fig)

            # Interpretación automática
            categoria_top = counts.idxmax()

            cantidad_top = counts.max()

            st.write(f"""
            La categoría con mayor frecuencia es '{categoria_top}',
            con un total de {cantidad_top} registros.
            """)


        with tabs[6]:

            st.header("Item 7 - Análisis Bivariado Numérico vs Categórico")

            # Diccionario de nombres personalizados
            nombres_columnas = {
                "id": "Id de cliente",
                "perc_premium_paid_by_cash_credit": "% de prima pagada",
                "age_in_days": "Edad en días",
                "Income": "Ingreso mensual",
                "Count_3-6_months_late": "Pagos demorados entre 3 y 6 meses",
                "Count_6-12_months_late": "Pagos demorados entre 6 y 12 meses",
                "Count_more_than_12_months_late": "Pagos demorados + 12 meses",
                "application_underwriting_score": "Nivel de riesgo o confiabilidad",
                "no_of_premiums_paid": "Número total de primas pagadas",
                "sourcing_channel": "Canal de captación",
                "residence_area_type": "Tipo de área de residencia",
                "premium": "Valor monetario de la prima",
                "renewal": "Renovación de póliza"
            }

            # Variables numéricas visibles
            numericas_visibles = [
                nombres_columnas[col]
                for col in numerical_cols
            ]

            # Variables categóricas visibles
            categoricas_visibles = [
                nombres_columnas[col]
                for col in categorical_cols
            ]

            # Selectbox personalizados
            numeric_visible = st.selectbox(
                "Variable Numérica",
                numericas_visibles
            )

            categorical_visible = st.selectbox(
                "Variable Categórica",
                categoricas_visibles
            )

            # Obtener nombres reales
            numeric_real = [
                key for key, value in nombres_columnas.items()
                if value == numeric_visible
            ][0]

            categorical_real = [
                key for key, value in nombres_columnas.items()
                if value == categorical_visible
            ][0]

            # Boxplot
            fig, ax = plt.subplots(figsize=(8,5))

            sns.boxplot(
                x=df[categorical_real],
                y=df[numeric_real],
                ax=ax
            )

            # Limpiar nombres técnicos
            ax.set_xlabel("")
            ax.set_ylabel("")

            st.pyplot(fig)


        with tabs[7]:

            st.header("Item 8 - Análisis Categórico vs Categórico")

            # Diccionario de nombres personalizados
            nombres_columnas = {
                "id": "Id de cliente",
                "perc_premium_paid_by_cash_credit": "% de prima pagada",
                "age_in_days": "Edad en días",
                "Income": "Ingreso mensual",
                "Count_3-6_months_late": "Pagos demorados entre 3 y 6 meses",
                "Count_6-12_months_late": "Pagos demorados entre 6 y 12 meses",
                "Count_more_than_12_months_late": "Pagos demorados + 12 meses",
                "application_underwriting_score": "Nivel de riesgo o confiabilidad",
                "no_of_premiums_paid": "Número total de primas pagadas",
                "sourcing_channel": "Canal de captación",
                "residence_area_type": "Tipo de área de residencia",
                "premium": "Valor monetario de la prima",
                "renewal": "Renovación de póliza"
            }

            # Variables categóricas visibles
            categoricas_visibles = [
                nombres_columnas[col]
                for col in categorical_cols
            ]

            # Selectbox personalizados
            cat1_visible = st.selectbox(
                "Seleccione primera variable",
                categoricas_visibles,
                key='cat1'
            )

            cat2_visible = st.selectbox(
                "Seleccione segunda variable",
                categoricas_visibles,
                key='cat2'
            )

            # Obtener nombres reales
            cat1_real = [
                key for key, value in nombres_columnas.items()
                if value == cat1_visible
            ][0]

            cat2_real = [
                key for key, value in nombres_columnas.items()
                if value == cat2_visible
            ][0]

            # Tabla cruzada
            cross = pd.crosstab(df[cat1_real], df[cat2_real])

            # Personalizar nombres
            cross.index.name = "Categorías"
            cross.columns.name = "Variables"

            st.subheader("Tabla Cruzada")

            st.dataframe(cross)

            # Heatmap
            fig, ax = plt.subplots(figsize=(8,5))

            sns.heatmap(
                cross,
                annot=True,
                fmt='d',
                cmap='Blues',
                ax=ax
            )

            # Eliminar nombres técnicos
            ax.set_xlabel("")
            ax.set_ylabel("")

            st.pyplot(fig)

        
        with tabs[8]:

            st.header("Item 9 - Análisis Dinámico")

            nombres_columnas = {
                "id": "Id de cliente",
                "perc_premium_paid_by_cash_credit": "% de prima pagada",
                "age_in_days": "Edad en días",
                "Income": "Ingreso mensual",
                "Count_3-6_months_late": "Pagos demorados entre 3 y 6 meses",
                "Count_6-12_months_late": "Pagos demorados entre 6 y 12 meses",
                "Count_more_than_12_months_late": "Pagos demorados + 12 meses",
                "application_underwriting_score": "Nivel de riesgo o confiabilidad",
                "no_of_premiums_paid": "Número total de primas pagadas",
                "sourcing_channel": "Canal de captación",
                "residence_area_type": "Tipo de área de residencia",
                "premium": "Valor monetario de la prima",
                "renewal": "Renovación de póliza"
            }

            # Multiselect con nombres amigables
            columnas_visibles = st.multiselect(
                "Seleccione columnas para visualizar",
                list(nombres_columnas.values()),
                key="multi_item9"
            )

            # Convertir nombres visibles a nombres reales
            columnas_reales = [
                key for key, value in nombres_columnas.items()
                if value in columnas_visibles
            ]

            # Slider
            rows = st.slider(
                "Cantidad de filas a mostrar",
                5,
                50,
                10,
                key="slider_item9"
            )

            # Mostrar información
            if st.checkbox("Mostrar información", key="check_item9"):

                if len(columnas_reales) > 0:

                    tabla = df[columnas_reales].head(rows)

                    # Renombrar columnas
                    tabla = tabla.rename(columns=nombres_columnas)

                    st.dataframe(tabla, hide_index=True)

                else:

                    st.warning("Seleccione al menos una columna.")

            # Análisis dinámico entre variables
            if columnas_reales and len(columnas_reales) >= 2:

                st.subheader("Análisis entre Variables")

                col1 = columnas_reales[0]
                col2 = columnas_reales[1]

                nombre1 = nombres_columnas[col1]
                nombre2 = nombres_columnas[col2]

                # NUMÉRICA VS NUMÉRICA
                if col1 in numerical_cols and col2 in numerical_cols:

                    correlacion = round(df[col1].corr(df[col2]), 2)

                    st.write(f"""
                    La relación entre '{nombre1}' y '{nombre2}'
                    presenta una correlación de {correlacion}.
                    """)

                    if correlacion > 0:

                        st.write(f"""
                        Esto indica una relación positiva entre ambas variables,
                        es decir, cuando '{nombre1}' aumenta,
                        '{nombre2}' también tiende a aumentar.
                        """)

                    elif correlacion < 0:

                        st.write(f"""
                        Esto indica una relación negativa entre ambas variables,
                        es decir, cuando '{nombre1}' aumenta,
                        '{nombre2}' tiende a disminuir.
                        """)

                    else:

                        st.write("""
                        No se observa una relación significativa entre ambas variables.
                        """)

                # CATEGÓRICA VS NUMÉRICA
                elif col1 in categorical_cols and col2 in numerical_cols:

                    promedio = df.groupby(col1)[col2].mean()

                    categoria_top = promedio.idxmax()

                    valor_top = round(promedio.max(),2)

                    st.write(f"""
                    La categoría '{categoria_top}' presenta el promedio más alto
                    en la variable '{nombre2}',
                    con un valor de {valor_top}.
                    """)

                # NUMÉRICA VS CATEGÓRICA
                elif col1 in numerical_cols and col2 in categorical_cols:

                    promedio = df.groupby(col2)[col1].mean()

                    categoria_top = promedio.idxmax()

                    valor_top = round(promedio.max(),2)

                    st.write(f"""
                    La categoría '{categoria_top}' presenta el promedio más alto
                    en la variable '{nombre1}',
                    con un valor de {valor_top}.
                    """)

                # CATEGÓRICA VS CATEGÓRICA
                else:

                    tabla_cruzada = pd.crosstab(df[col1], df[col2])

                    st.write(f"""
                    Se observa la distribución conjunta entre
                    '{nombre1}' y '{nombre2}',
                    permitiendo identificar patrones y concentraciones
                    entre categorías.
                    """)

        with tabs[9]:

            st.header("Item 10 - Hallazgos Clave")

            st.subheader("Insights principales")

            st.write("- Por el análisis realizado se obtuvo que la mayoría de clientes es de zona urbana.")
            st.write("- Existen diferencias de ingresos según tipo de cliente.")
            st.write("- El canal de adquisición influye en la renovación.")
            st.write("- Los clientes con menos retrasos tienden a renovar más.")

            renewal_counts = df['renewal'].value_counts()

            fig, ax = plt.subplots(figsize=(5,4))
            renewal_counts.plot(kind='bar', ax=ax)
            st.pyplot(fig)

    else:
        st.warning("Debe cargar un archivo CSV para ejecutar el análisis")

















## NAVEGACION

if opcion=="Home":
    home()

elif opcion=="Visualizar dataset":

    visualizar()

elif opcion=="Análisis exploratorio":
    analisis()

elif opcion=="Ejercicio 3":
    ejercicio3()
    
elif opcion=="Ejercicio 4":
    ejercicio4()
