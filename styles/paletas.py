# ================================================================
# Criar classe e definir as cores das equipes da NBB como objetos
# ================================================================
from dataclasses import dataclass


@dataclass
class Paleta:
    primaria: str
    secundaria: str
    terciaria: str

PALETAS = {
    "Basket Osasco": Paleta(
        primaria="#24AD54", secundaria="#ED3237", terciaria="#A98F71"
    ),
    "Basquete Cearense": Paleta(
        primaria="#E95319", secundaria="#E9671A", terciaria="#DBDBDB"
    ),
    "Bauru": Paleta(
        primaria="#5B8C80", secundaria="#63B32E", terciaria="#00493E"
    ),
    "Botafogo": Paleta(
        primaria="#8A8A8A", secundaria="#FFFFFF", terciaria="#525252"
    ),
    "Brasília": Paleta(
        primaria="#23324E", secundaria="#3C4861", terciaria="#BAA989"
    ),
    "Caxias do Sul Basquete": Paleta(
        primaria="#F39E00", secundaria="#E24A14", terciaria="#B8B8B7"
    ),
    "Corinthians": Paleta(
        primaria="#FFFFFF", secundaria="#6F6F6F", terciaria="#BE0222"
    ),
    "Cruzeiro": Paleta(
        primaria="#4087BF", secundaria="#003D81", terciaria="#B78C18"
    ),
    "Flamengo": Paleta(
        primaria="#BF0411", secundaria="#FFFFFF", terciaria="#6F6F6F"
    ),
    "Franca": Paleta(
        primaria="#011F75", secundaria="#516CD1", terciaria="#9D0003"
    ),
    "Minas": Paleta(
        primaria="#0A1154", secundaria="#183962", terciaria="#FEFEFF"
    ),
    "Mogi": Paleta(
        primaria="#FEE392", secundaria="#F6B206", terciaria="#000C49"
    ),
    "Pato Basquete": Paleta(
        primaria="#005B9D", secundaria="#FBB040", terciaria="#FFFFFF"
    ),
    "Paulistano": Paleta(
        primaria="#F58D94", secundaria="#F8ADB1", terciaria="#FACED1"
    ),
    "Pinheiros": Paleta(
        primaria="#7B92A8", secundaria="#044584", terciaria="#B9C0C7"
    ),
    "São José": Paleta(
        primaria="#D67532", secundaria="#FACF00", terciaria="#053768"
    ),
    "União Corinthians": Paleta(
        primaria="#05A248", secundaria="#003C69", terciaria="#CF004D"
    ),
    "UNIFACISA": Paleta(
        primaria="#376FC0", secundaria="#193474", terciaria="#C7D2E5"
    ),
}
