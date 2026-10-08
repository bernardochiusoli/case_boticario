"""Features de calendário, eventos e histórico para o forecast diário (horizonte de 7 dias)."""
import numpy as np
import pandas as pd
from .data import EVENTOS, FERIADOS

HORIZONTE = 7
EVENTOS_PRESENTE = ["Natal", "Dia das Mães", "Dia dos Namorados", "Páscoa"]
EVENTOS_PROMO = ["Black Friday", "Cyber Monday", "Dia do Consumidor"]


def _dias_ate(datas, alvos):
    alvos = pd.to_datetime(sorted(alvos))
    out = []
    for d in datas:
        fut = alvos[alvos >= d]
        out.append((fut[0] - d).days if len(fut) else 60)
    return np.clip(np.array(out), 0, 60)


def _dias_desde(datas, alvos):
    alvos = pd.to_datetime(sorted(alvos))
    out = []
    for d in datas:
        pas = alvos[alvos <= d]
        out.append((d - pas[-1]).days if len(pas) else 60)
    return np.clip(np.array(out), 0, 60)


def montar_features(y: pd.Series) -> pd.DataFrame:
    """y: série diária (índice = data). Retorna X alinhado a y.
    Lags começam em 7 dias: no momento da previsão (D0) só conhecemos até D0-1,
    para os dias D+1 a D+7: lag 7 é o menor lag conhecido para todo o horizonte."""
    X = pd.DataFrame(index=y.index)
    d = y.index
    X["dia_semana"] = d.dayofweek
    X["dia_mes"] = d.day
    X["fim_de_semana"] = (d.dayofweek >= 5).astype(int)
    X["inicio_mes"] = (d.day <= 7).astype(int)
    X["quinzena_pagamento"] = ((d.day >= 15) & (d.day <= 22)).astype(int)
    X["feriado"] = d.isin(pd.to_datetime(FERIADOS)).astype(int)
    presente = [EVENTOS[e] for e in EVENTOS_PRESENTE]
    promo = [EVENTOS[e] for e in EVENTOS_PROMO]
    X["dias_ate_evento_presente"] = _dias_ate(d, presente)
    X["dias_ate_evento_promo"] = _dias_ate(d, promo)
    X["semana_pre_presente"] = (X.dias_ate_evento_presente.between(1, 10)).astype(int)
    X["dia_evento_promo"] = (X.dias_ate_evento_promo == 0).astype(int)
    X["pos_evento_presente"] = (_dias_desde(d, presente).clip(0, 60) <= 4).astype(int) * (X.dias_ate_evento_presente > 0)
    log_y = np.log1p(y)
    X["lag_7"] = log_y.shift(7)
    X["lag_14"] = log_y.shift(14)
    X["media_7_lag7"] = log_y.shift(7).rolling(7).mean()
    X["media_28_lag7"] = log_y.shift(7).rolling(28).mean()
    X["mesmo_dia_media_4sem"] = (log_y.shift(7) + log_y.shift(14) + log_y.shift(21) + log_y.shift(28)) / 4
    return X
