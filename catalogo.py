# ==========================================
# CATÁLOGO DE VUELOS
# ==========================================

VUELOS = {

    # Air Europa
    "AEA4008": "PMI",
    "AEA4014": "PMI",
    "AEA4060": "MAD",
    "AEA4064": "MAD",

    # Air France
    "AF1417": "CDG",

    # Air Algérie
    "AH2009": "ALG",

    # Finnair
    "AY1704": "HEL",
    "AY1706": "HEL",

    # Air Baltic
    "BT698": "RIX",

    # Norse
    "D83655": "CPH",

    # Transavia
    "HV5102": "EIN",
    "HV5104": "EIN",
    "HV5106": "EIN",
    "HV5107": "EIN",

    "HV6334": "AMS",
    "HV6336": "AMS",
    "HV6338": "AMS",
    "HV6340": "AMS",

    "HV6442": "RTM",
    "HV6444": "RTM",

    # KLM
    "KL1532": "AMS",

    # Luxair
    "LG764": "LUX",
    "LG770": "PMI",

    # EasyJet
    "NE8002": "AGP",

    # Smartwings
    "QS1055": "PRG",

    # Transavia France
    "TO4621": "ORY",
    "TO4623": "ORY",
    "TO4625": "ORY",
    "TO4627": "ORY",
    "TO4629": "ORY",

    # Air Transat
    "TS277": "YUL",

    # Wizz Air
    "W43186": "OTP",
    "W43412": "CLJ",
    "W43568": "TSR",
    "W43724": "IAS",

    "W46028": "FCO",
    "W46030": "FCO",
    "W46046": "FCO",

    "W46318": "MXP",
    "W46386": "TRN",

    "W46746": "VCE",
    "W46748": "VCE",

    "W61338": "WAW",

    "W62080": "KRK",
    "W62386": "BUD",
    "W64410": "SOF",

    "W95368": "LTN",
    "W95738": "LGW"
}

# ==========================================
# AGENTES
# ==========================================

AGENTES = [

    "JavierP",
    "Carmela",
    "MariaC",
    "Daniel",
    "Pamela",
    "Nezahat",
    "CamilaA",
    "Delfina",
    "Darío",
    "Carmela",
    "Juanjo"
]

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

def obtener_destino(vuelo):

    return VUELOS.get(
        vuelo.upper(),
        ""
    )


def lista_vuelos():

    return sorted(
        VUELOS.keys()
    )


def lista_agentes():

    return sorted(
        list(set(AGENTES))
    )
