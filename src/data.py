"""Carga, limpeza e agregações da base de vendas do e-commerce."""
import numpy as np
import pandas as pd

CATEGORIAS = ["PERFUMARIA FEMININA", "PERFUMARIA MASCULINA", "PERF. DE ENTRADA E DEOS",
              "GIFTS", "CORPO E BANHO", "MAQUIAGEM", "CABELOS", "FACIAL"]
METRICAS = ["receita_aprovada", "nr_pedidos", "qt_material", "vlr_venda_desconto"]
NAO_ID = "NAO IDENTIFICADA"

EVENTOS = {
    "Black Friday": "2025-11-28", "Cyber Monday": "2025-12-01", "Natal": "2025-12-25",
    "Réveillon": "2025-12-31", "Carnaval": "2026-02-16", "Dia do Consumidor": "2026-03-15",
    "Páscoa": "2026-04-05", "Dia das Mães": "2026-05-10", "Dia dos Namorados": "2026-06-12",
}
FERIADOS = ["2025-11-02", "2025-11-15", "2025-11-20", "2025-12-25", "2026-01-01",
            "2026-02-16", "2026-02-17", "2026-04-03", "2026-04-21", "2026-05-01", "2026-06-04"]


def carregar(caminho: str) -> pd.DataFrame:
    if caminho.endswith((".xlsx", ".xls")):
        df = pd.read_excel(caminho)
    else:
        df = pd.read_csv(caminho, parse_dates=["dt_hr_venda"])
    return df.rename(columns={"DES_CANAL_VENDA_FINAL_AGRUP": "canal",
                              "DES_CATEGORIA_MATERIAL": "categoria"})


def diagnostico(df: pd.DataFrame) -> pd.DataFrame:
    """Resumo dos problemas de qualidade encontrados na base crua."""
    cat_invalida = ~df.categoria.isin(CATEGORIAS)
    linhas = {
        "Linhas totais": len(df),
        "Categoria inválida (número no lugar do nome)": int(cat_invalida.sum()),
        "Receita negativa com itens e pedidos positivos": int((df.receita_aprovada < 0).sum()),
        "Receita zero (itens 100% descontados)": int((df.receita_aprovada == 0).sum()),
        "Nulos": int(df.isna().sum().sum()),
        "Duplicadas (hora, canal, categoria)": int(df.duplicated(["dt_hr_venda", "canal", "categoria"]).sum()),
        "Itens < pedidos (incoerência)": int((df.qt_material < df.nr_pedidos).sum()),
    }
    out = pd.DataFrame({"qtd": linhas})
    out["% das linhas"] = (out.qtd / len(df) * 100).round(2)
    return out


def limpar(df: pd.DataFrame) -> pd.DataFrame:
    """1) corrige sinal da receita; 2) recupera categoria quando é a única ausente na hora/canal."""
    df = df.copy()
    df["receita_negativa_corrigida"] = df.receita_aprovada < 0
    df["receita_aprovada"] = df.receita_aprovada.abs()

    invalida = ~df.categoria.isin(CATEGORIAS)
    df.loc[invalida, "categoria"] = NAO_ID
    df["categoria_recuperada"] = False
    grupos = df.groupby(["dt_hr_venda", "canal"])
    for (hora, canal), g in grupos:
        if (g.categoria == NAO_ID).sum() == 1:
            faltantes = set(CATEGORIAS) - set(g.categoria)
            if len(faltantes) == 1:
                idx = g.index[g.categoria == NAO_ID][0]
                df.loc[idx, "categoria"] = faltantes.pop()
                df.loc[idx, "categoria_recuperada"] = True
    return df


def grid_completo(df: pd.DataFrame) -> pd.DataFrame:
    """Toda hora x canal x categoria, preenchendo com zero onde não houve venda."""
    horas = pd.date_range(df.dt_hr_venda.min().floor("D"), df.dt_hr_venda.max().ceil("D"),
                          freq="h", inclusive="left")
    cats = sorted(df.categoria.unique())
    idx = pd.MultiIndex.from_product([horas, sorted(df.canal.unique()), cats],
                                     names=["dt_hr_venda", "canal", "categoria"])
    return (df.groupby(["dt_hr_venda", "canal", "categoria"])[METRICAS].sum()
              .reindex(idx, fill_value=0).reset_index())


def diario(df: pd.DataFrame) -> pd.DataFrame:
    d = df.assign(data=df.dt_hr_venda.dt.normalize()).groupby("data")[METRICAS].sum()
    d["preco_medio_item"] = d.receita_aprovada / d.qt_material
    d["ticket_medio"] = d.receita_aprovada / d.nr_pedidos
    d["itens_por_pedido"] = d.qt_material / d.nr_pedidos
    d["pct_desconto"] = d.vlr_venda_desconto / (d.receita_aprovada + d.vlr_venda_desconto)
    return d
