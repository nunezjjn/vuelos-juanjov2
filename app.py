import streamlit as st
import pandas as pd
import plotly.express as px

from datetime import (
    datetime,
    timedelta
)

from database import *
from catalogo import *

crear_db()

st.set_page_config(
    page_title="Vuelos Juanjo",
    layout="wide"
)

# --------------------
# FUNCIONES
# --------------------

def calcular_cierre(etd, minutos):

    hora = datetime.strptime(
        etd.strftime("%H:%M"),
        "%H:%M"
    )

    cierre = hora - timedelta(
        minutes=minutos
    )

    return cierre.strftime("%H:%M")

# --------------------
# CABECERA
# --------------------

st.title("✈️ Gestión Operativa")

tabs = st.tabs(
    [
        "Operación",
        "Alarmas",
        "Histórico",
        "Estadísticas"
    ]
)

# ==================================================
# OPERACION
# ==================================================

with tabsst.subheader("Nuevo vuelo")

    fecha = st.date_input(
        "Fecha"
    )

    vuelo = st.selectbox(
        "Vuelo",
        sorted(VUELOS.keys())
    )

    destino = VUELOS[vuelo]

    st.text_input(
        "Destino",
        value=destino,
        disabled=True
    )

    etd = st.time_input(
        "ETD"
    )

    tiempo_cierre = st.number_input(
        "Tiempo cierre",
        value=40
    )

    cierre = calcular_cierre(
        etd,
        tiempo_cierre
    )

    st.text_input(
        "Cierre Check-in",
        value=cierre,
        disabled=True
    )

    mostradores = st.text_input(
        "Mostradores"
    )

    col1, col2 = st.columns(2)

    with col1:

        agente1 = st.selectbox(
            "Agente 1",
            [""] + AGENTES
        )

        agente2 = st.selectbox(
            "Agente 2",
            [""] + AGENTES,
            key="a2"
        )

    with col2:

        agente3 = st.selectbox(
            "Agente 3",
            [""] + AGENTES,
            key="a3"
        )

        agente4 = st.selectbox(
            "Agente 4",
            [""] + AGENTES,
            key="a4"
        )

    observaciones = st.text_area(
        "Observaciones"
    )

    if st.button("Guardar vuelo"):

        insertar((
            str(fecha),
            vuelo,
            destino,
            etd.strftime("%H:%M"),
            tiempo_cierre,
            cierre,
            mostradores,
            agente1,
            agente2,
            agente3,
            agente4,
            0,
            None,
            observaciones
        ))

        st.success("Vuelo guardado")

# ==================================================
# ALARMAS
# ==================================================

with tabsst.subheader("Vuelos pendientes")

    df = obtener_todos()

    if not df.empty:

        hoy = datetime.today().strftime(
            "%Y-%m-%d"
        )

        pendientes = df[
            (df["atendido"] == 0)
        ].copy()

        pendientes["orden"] = pd.to_datetime(
            pendientes["cierre_checkin"],
            format="%H:%M"
        )

        pendientes = pendientes.sort_values(
            "orden"
        )

        ahora = datetime.now()

        for _, row in pendientes.iterrows():

            cierre = datetime.strptime(
                row["cierre_checkin"],
                "%H:%M"
            )

            minutos = (
                cierre.hour * 60 +
                cierre.minute
            ) - (
                ahora.hour * 60 +
                ahora.minute
            )

            texto = (
                f"{row['vuelo']} | "
                f"{row['destino']} | "
                f"Cierre {row['cierre_checkin']}"
            )

            if minutos <= 15:
                st.error(texto)
            elif minutos <= 30:
                st.warning(texto)
            else:
                st.success(texto)

            if st.button(
                "✅ Atendido",
                key=f"a_{row['id']}"
            ):
                marcar_atendido(
                    row["id"]
                )
                st.rerun()

# ==================================================
# HISTORICO
# ==================================================

with tabsdf = obtener_todos()

    st.dataframe(
        df,
        use_container_width=True
    )

# ==================================================
# ESTADISTICAS
# ==================================================

with tabsdf = obtener_todos()

    if not df.empty:

        df["fecha"] = pd.to_datetime(
            df["fecha"]
        )

        mensual = (
            df.groupby(
                df["fecha"].dt.strftime(
                    "%Y-%m"
                )
            )
            .size()
            .reset_index(
                name="vuelos"
            )
        )

        st.plotly_chart(
            px.bar(
                mensual,
                x="fecha",
                y="vuelos",
                title="Vuelos por mes"
            ),
            use_container_width=True
        )

        destinos = (
            df.groupby("destino")
            .size()
            .reset_index(
                name="vuelos"
            )
            .sort_values(
                "vuelos",
                ascending=False
            )
        )

        st.plotly_chart(
            px.pie(
                destinos,
                values="vuelos",
                names="destino",
                title="Destinos"
            ),
            use_container_width=True
        )
