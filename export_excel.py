from io import BytesIO

import pandas as pd


def exportar_dataframe_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="Vuelos",
            index=False
        )

        worksheet = writer.sheets["Vuelos"]

        for columna in worksheet.columns:

            longitud = 0

            letra_columna = columna[0].column_letter

            for celda in columna:

                try:
                    longitud = max(
                        longitud,
                        len(str(celda.value))
                    )
                except Exception:
                    pass

            worksheet.column_dimensions[
                letra_columna
            ].width = longitud + 2

    output.seek(0)

    return output


def exportar_mes(df, anio, mes):

    if df.empty:
        return None

    df["fecha"] = pd.to_datetime(
        df["fecha"],
        errors="coerce"
    )

    filtrado = df[
        (df["fecha"].dt.year == anio)
        &
        (df["fecha"].dt.month == mes)
    ]

    if filtrado.empty:
        return None

    return exportar_dataframe_excel(
        filtrado
    )


def exportar_anio(df, anio):

    if df.empty:
        return None

    df["fecha"] = pd.to_datetime(
        df["fecha"],
        errors="coerce"
    )

    filtrado = df[
        df["fecha"].dt.year == anio
    ]

    if filtrado.empty:
        return None

    return exportar_dataframe_excel(
        filtrado
    )
