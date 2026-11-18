# Protocolo congelado antes das estimações — 2026-11-16

Pergunta: associação das condições físicas e do apoio operacional em 2022 com IDEB AF 2023 nas escolas públicas elegíveis. Unidade escola, chave CO_ENTIDADE. Estudo observacional, sem identificação causal; exposição escolar agregada, alunos/coortes não acompanhados.

Fonte inicial: R1 (28.236; SHA-256 369e9ac1b7ea74e970dbbaaa4dd18a9aeaa99f05415b516bb55d60bd3003567b). Requer confirmar Censo 2022, dependência 1–3, ativa, IN_FUND_AF=1, ICG 2022 3–6 e IDEB AF 2023 válido. Esperadas 28.199 candidatas antes de complete cases. Sem objetivo de coincidir com a amostra histórica.

Indicadores binários oficiais, sem índice: IN_BIBLIOTECA_SALA_LEITURA, IN_BANHEIRO_PNE, IN_LABORATORIO_CIENCIAS. Usar o primeiro diretamente, sem somar biblioteca e sala. Códigos válidos 0/1 confirmados no dicionário. Apoio: QT_PROF_SERVICOS_GERAIS; 88888 vira missing apenas nesse campo conforme dicionário; zero permanece válido. Não representa gestão de FM nem manutenção isoladamente.

Controles: INSE 2021 contínuo, IRD 2022 contínuo, log natural das matrículas básicas 2022 (>0), ICG 2022 categórico 3–6, dependência categórica, localização categórica, UF categórica. Referências: menores códigos/UF em ordem alfabética presentes na amostra. Desfecho IDEB AF 2023 escala original. Pessoal em número bruto, separadamente de log(matrículas). INSE antecede exposição; IRD e demais condições são 2022; IDEB 2023 é posterior, mas isso não identifica causalidade. Nenhum controle contemporâneo de fluxo no principal.

M0: contexto; M1: M0 + três indicadores; M2: M1 + serviços gerais. Mesma amostra completa M2 em todos os modelos principais, inclusive município identificado. OLS sem pesos; erros agrupados por município CR1 com fator G/(G−1)*(N−1)/(N−k), inferência t com G−1 graus de liberdade. HC3 complementar, inferência t N−k. IC95% bilaterais. Efeitos binários 0→1, pessoal +1 profissional, demais +1 unidade da escala indicada. Reportar também beta*SD(X)/SD(Y) para variáveis numéricas.

Diagnósticos por modelo: resíduos/ajustados; BP-Koenker n*R² de regressão de resíduos² em X (referência qui-quadrado, diagnóstico i.i.d. complementar), VIF por colunas incluindo dummies (não GVIF), leverage e Cook, regressão acrescida de quadrados centrados das covariáveis contínuas com teste de Wald agrupado (não linearidade). Outliers IQR e Cook são sinalizados e mantidos; nenhum corte guiado por p. MCAR/MAR não serão inferidos de contagens de missing.

Exatamente duas sensibilidades M2, definidas antes de estimar: S1 trocar pessoal bruto por log1p(pessoal), mantendo a amostra principal; S2 acrescentar abandono AF 2022 em pontos percentuais, na subamostra disponível, com M2 reestimado na mesma subamostra como referência. S2 explora controle de fluxo possivelmente endógeno, não substitui principal. Não testar novas famílias em busca de significância.

QC: chaves únicas, limites/códigos, hashes, matriz de desenho com posto completo, contraste OLS lstsq/QR, covariância simétrica e diagonal não negativa, igualdade de amostras M0–M2. Versões e seed 20261116. Preservar dados brutos, R1 e manuscritos. Nenhum argumento científico de submissão gerado: manuscrito é estrutura com tabelas e marcadores autorais. Citações e autoria de passagens dependem de validação dos coautores.
