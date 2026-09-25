
import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "vuelos.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS vuelos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        fecha TEXT NOT NULL,

        vuelo TEXT NOT NULL,
        destino TEXT NOT NULL,

        etd TEXT NOT NULL,

        tiempo_cierre INTEGER NOT NULL,

        cierre_checkin TEXT NOT NULL,

        mostradores TEXT,

        agente1 TEXT,
        agente2 TEXT,
        agente3 TEXT,
        agente4 TEXT,

        atendido INTEGER DEFAULT 0,

        hora_atencion TEXT,

        observaciones TEXT,

        creado_en TEXT DEFAULT CURRENT_TIMESTAMP,

        UNIQUE(fecha, vuelo)
    )
    """)

    conn.commit()
    conn.close()


def insertar_vuelo(
    fecha,
    vuelo,
    destino,
    etd,
    tiempo_cierre,
    cierre_checkin,
    mostradores,
    agente1,
    agente2,
    agente3,
    agente4,
    observaciones
):

    conn = get_connection()

    conn.execute(
        """
        INSERT OR IGNORE INTO vuelos (
            fecha,
            vuelo,
            destino,
            etd,
            tiempo_cierre,
            cierre_checkin,
            mostradores,
            agente1,
            agente2,
            agente3,
            agente4,
            observaciones
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            fecha,
            vuelo,
            destino,
            etd,
            tiempo_cierre,
            cierre_checkin,
            mostradores,
            agente1,
            agente2,
            agente3,
            agente4,
            observaciones
        )
    )

    conn.commit()
    conn.close()


def obtener_vuelos():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM vuelos
        ORDER BY fecha DESC, cierre_checkin ASC
        """,
        conn
    )

    conn.close()

    return df


def obtener_pendientes():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM vuelos
        WHERE atendido = 0
        ORDER BY fecha ASC, cierre_checkin ASC
        """,
        conn
    )

    conn.close()

    return df


def marcar_atendido(id_vuelo):

    conn = get_connection()

    hora = datetime.now().strftime("%H:%M")

    conn.execute(
        """
        UPDATE vuelos
        SET atendido = 1,
            hora_atencion = ?
        WHERE id = ?
        """,
        (
            hora,
            id_vuelo
        )
    )

    conn.commit()
    conn.close()


def eliminar_vuelo(id_vuelo):

    conn = get_connection()

    conn.execute(
        """
        DELETE FROM vuelos
        WHERE id = ?
        """,
        (id_vuelo,)
    )

    conn.commit()
    conn.close()


def obtener_estadisticas():

    conn = get_connection()

    total = pd.read_sql_query(
        "SELECT COUNT(*) total FROM vuelos",
        conn
    ).iloc[0]["total"]

    atendidos = pd.read_sql_query(
        """
        SELECT COUNT(*) total
        FROM vuelos
        WHERE atendido = 1
        """,
        conn
    ).iloc[0]["total"]

    pendientes = pd.read_sql_query(
        """
        SELECT COUNT(*) total
        FROM vuelos
        WHERE atendido = 0
        """,
        conn
    ).iloc[0]["total"]

    conn.close()

    return {
        "total": int(total),
        "atendidos": int(atendidos),
        "pendientes": int(pendientes)
    }
