# Case Técnico · Especialista de Dados I · Grupo Boticário

Previsão de venda diária do e-commerce e proposta de pipeline de IA para pontuar banners.

## O problema

Prever a receita diária do e-commerce (App + Site) com antecedência de até 7 dias, extrair insights sobre preço médio, dia da semana e comportamento intradiário, e propor uma solução viável de IA para classificar e pontuar banners do site.

## Principais resultados

**Qualidade da base:** três problemas encontrados e tratados antes de qualquer análise. 6% das linhas tinham a categoria trocada por um número (57% recuperadas pela lógica hora × canal); 4% tinham receita com sinal invertido (corrigido, evitando subestimar R$ 42 mi); `nr_pedidos` duplica entre categorias (documentado).

**Insights**
- Novembro fez **26% da receita de 8 meses**, com preço por item 37% menor e desconto de 53%: volume comprado com desconto.
- **Black Friday é demanda comprada; Dia das Mães é demanda orgânica.** No pico do Dia das Mães o preço por item foi R$ 70 com 29% de desconto, contra R$ 33 e 55% na Black Friday.
- **Sexta vende 10% acima da média e domingo 22% abaixo** (sem eventos). No sábado, o App segura e o Site cai 14%.
- Dois picos no dia: **10h-14h** (principal) e **20h-21h**. Ao meio-dia, 31% da receita do dia já aconteceu.
- Em datas de presente, **Gifts triplica de share** (8% para 21% no Dia das Mães). O App foi de 72% para 79% da receita.

**Forecast**
- LightGBM com features de calendário, eventos e lags a partir de 7 dias, validado com backtest walk-forward (abril, maio e junho).
- **WAPE de 24,6%, 16% menor que a melhor regra simples** (média do mesmo dia nas últimas 4 semanas). Em abril e junho, 18,9%.
- A semana do Dia das Mães, nunca vista no treino, responde por 30% de todo o erro. Recomendação: modelo como linha de base + ajuste comercial para datas sazonais.

**Seção 2 · IA para banners:** MVP de 6 semanas na stack homologada (embeddings CLIP/SigLIP, zero-shot, LLM multimodal com rubrica de marca, score de performance), com gates de investimento e validação por teste A/B.

## Estrutura

```
├── notebooks/
│   ├── 01_raio_x_e_qualidade.ipynb   # base crua, problemas de qualidade, tratamentos
│   ├── 02_eda_insights.ipynb         # preço médio, dia da semana, intradiário, extras
│   ├── 03_modelagem_forecast.ipynb   # decisões, baselines, backtest, LightGBM, SHAP, faixa
│   └── 04_secao2_ia_imagens.md       # condução, arquitetura, MVP, custo vs retorno
├── src/
│   ├── data.py         # carga, diagnóstico, limpeza, agregações
│   ├── features.py     # features sem vazamento para horizonte de 7 dias
│   ├── validation.py   # WAPE, viés, backtest walk-forward
│   └── viz.py          # padrão visual dos gráficos
├── reports/
│   ├── apresentacao_case_boticario.pptx
│   └── figures/        # gráficos usados na apresentação
└── data/README.md      # como posicionar a base (não versionada)
```

## Como rodar

```bash
pip install -r requirements.txt
# coloque a base em data/vendas.xlsx (ver data/README.md)
cd notebooks
jupyter nbconvert --to notebook --execute --inplace 01_raio_x_e_qualidade.ipynb 02_eda_insights.ipynb 03_modelagem_forecast.ipynb
```

Seed fixa (`random_state=42`). Os notebooks já estão salvos com as saídas.
