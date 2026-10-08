# Dados

A base do case não é versionada no repositório. Para rodar:

1. Salve o arquivo do case como `data/vendas.xlsx` (ou `.csv`, ajustando o caminho em `notebooks/01_raio_x_e_qualidade.ipynb`).
2. Rode os notebooks na ordem 01 → 02 → 03. O 01 gera `data/vendas_tratadas.pkl`, usado pelos demais.

Colunas esperadas: `dt_hr_venda`, `DES_CANAL_VENDA_FINAL_AGRUP`, `DES_CATEGORIA_MATERIAL`, `receita_aprovada`, `nr_pedidos`, `qt_material`, `vlr_venda_desconto`.
