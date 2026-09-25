import sqlite3
import pandas as pd
from datetime import datetime

DB = "vuelos.db"

def conectar():
    return sqlite3.connect(DB)

def crear_db():

    conn = conectar()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS vuelos(
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

        UNIQUE(fecha, vuelo)
    )
    """)

    conn.commit()
    conn.close()

def insertar(datos):

    conn = conectar()

    conn.execute("""
    INSERT OR IGNORE INTO vuelos(
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
        atendido,
        hora_atencion,
        observaciones
    )
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, datos)

    conn.commit()
    conn.close()

def obtener_todos():

    conn = conectar()

    df = pd.read_sql(
        "SELECT * FROM vuelos",
        conn
    )

    conn.close()

    return df

def marcar_atendido(id_vuelo):

    conn = conectar()

    hora = datetime.now().strftime("%H:%M")

    conn.execute("""
    UPDATE vuelos
    SET atendido = 1,
        hora_atencion = ?
    WHERE id = ?
    """, (hora, id_vuelo))

    conn.commit()
    conn.close()
