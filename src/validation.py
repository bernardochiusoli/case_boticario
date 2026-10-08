"""Métricas e backtest walk-forward (janela expansível)."""
import numpy as np
import pandas as pd


def wape(y, yhat):
    y, yhat = np.asarray(y), np.asarray(yhat)
    return np.abs(y - yhat).sum() / np.abs(y).sum()


def vies(y, yhat):
    y, yhat = np.asarray(y), np.asarray(yhat)
    return (yhat - y).sum() / y.sum()


def mape(y, yhat):
    y, yhat = np.asarray(y), np.asarray(yhat)
    return np.mean(np.abs(y - yhat) / y)


MESES = {1: "jan", 2: "fev", 3: "mar", 4: "abr", 5: "mai", 6: "jun", 7: "jul", 8: "ago", 9: "set", 10: "out", 11: "nov", 12: "dez"}
CORTES = ["2026-03-31", "2026-04-30", "2026-05-31"]


def backtest(y, X, ajustar_prever, cortes=CORTES):
    """ajustar_prever(X_tr, y_tr, X_te) -> previsão em reais para X_te."""
    linhas, preds = [], []
    for corte in cortes:
        corte = pd.Timestamp(corte)
        fim = corte + pd.offsets.MonthEnd(1)
        tr = (y.index <= corte) & X.notna().all(axis=1)
        te = (y.index > corte) & (y.index <= fim)
        p = ajustar_prever(X[tr], y[tr], X[te])
        preds.append(pd.Series(p, index=y.index[te]))
        linhas.append({"teste": f"{MESES[fim.month]}/{fim.year}", "dias_treino": int(tr.sum()),
                       "WAPE": wape(y[te], p), "MAPE": mape(y[te], p), "viés": vies(y[te], p)})
    return pd.DataFrame(linhas), pd.concat(preds)
