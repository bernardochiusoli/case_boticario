"""Padrão visual dos gráficos: verde dominante, coral para destaque, resto em cinza."""
import matplotlib.pyplot as plt
import matplotlib as mpl

VERDE = "#0B5A43"
VERDE_CLARO = "#7FB8A4"
CORAL = "#E4572E"
CINZA = "#B8BDB5"
CINZA_ESC = "#4A4F4A"
FUNDO = "#FFFFFF"


def aplicar_estilo():
    mpl.rcParams.update({
        "figure.figsize": (11, 4.6), "figure.dpi": 110, "savefig.dpi": 200,
        "axes.spines.top": False, "axes.axisbelow": True, "axes.spines.right": False,
        "axes.edgecolor": CINZA, "axes.labelcolor": CINZA_ESC, "axes.titleweight": "bold",
        "axes.titlesize": 14, "axes.titlelocation": "left", "axes.titlepad": 14,
        "xtick.color": CINZA_ESC, "ytick.color": CINZA_ESC, "axes.grid": True,
        "grid.color": "#ECEEEA", "grid.linewidth": 0.8, "font.size": 11,
        "legend.frameon": False, "axes.prop_cycle": mpl.cycler(color=[VERDE, CORAL, VERDE_CLARO, CINZA]),
    })


def reais_mi(x, _=None):
    return f"R$ {x/1e6:,.1f} mi".replace(",", "X").replace(".", ",").replace("X", ".")


def salvar(fig, nome):
    """Salva o gráfico com título (relatório) e uma versão sem título para os slides."""
    import os
    fig.savefig(f"../reports/figures/{nome}.png", bbox_inches="tight", facecolor=FUNDO)
    os.makedirs("../reports/figures/slides", exist_ok=True)
    titulos = [(ax, ax.get_title(loc="left")) for ax in fig.axes]
    for ax, _ in titulos:
        ax.set_title("", loc="left")
    fig.savefig(f"../reports/figures/slides/{nome}.png", bbox_inches="tight", facecolor=FUNDO)
    for ax, t in titulos:
        ax.set_title(t, loc="left")
