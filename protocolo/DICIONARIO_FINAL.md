# Dicionário final

| campo | descricao | tipo | codigos | aba | linha |
|---|---|---|---|---|---|
| IN_BANHEIRO_PNE | Dependências físicas existentes e utilizadas na escola - Banheiro acessível, adequado ao uso de pessoas com deficiência ou mobilidade reduzida | Num | 0 - Não 1 - Sim | Cadastro_Escolas | 121 |
| IN_BIBLIOTECA_SALA_LEITURA | Dependências físicas existentes e utilizadas na escola - Biblioteca e/ou Sala de leitura | Num | 0 - Não 1 - Sim | Cadastro_Escolas | 126 |
| IN_LABORATORIO_CIENCIAS | Dependências físicas existentes e utilizadas na escola - Laboratório de ciências | Num | 0 - Não 1 - Sim | Cadastro_Escolas | 131 |
| QT_PROF_SERVICOS_GERAIS | Quantidade de profissionais que atuam na escola - Auxiliar de serviços gerais, porteiro(a), zelador(a), faxineiro(a), horticultor(a), jardineiro(a) | Num | 88888 - registro com marcação de valor extremo (valor superior ao limite máximo* definido com base na distribuição da razão de profissionais por matrícula) | Cadastro_Escolas | 224 |

Mapeamento das colunas herdadas de R1

| campo_origem | campo_novo |
|---|---|
| VL_OBSERVADO_2023 | ideb23 |
| Media_INSE_oficial_2021 | inse21 |
| IRD_oficial_2022 | ird22 |
| QT_MAT_BAS | matriculas |
| QT_PROF_SERVICOS_GERAIS | servicos_gerais |
| IN_BIBLIOTECA_SALA_LEITURA | biblioteca_leitura |
| IN_BANHEIRO_PNE | banheiro_acessivel |
| IN_LABORATORIO_CIENCIAS | lab_ciencias |
| Nivel_Complexidade_Gestao_2022 | icg22 |
| TP_DEPENDENCIA | dependencia |
| TP_LOCALIZACAO | localizacao |
| SG_UF | uf |
| CO_MUNICIPIO | municipio |
| Abandono_oficial_2022_3_CAT_FUN_AF | abandono22 |

log_matriculas = ln(QT_MAT_BAS), exigindo matrículas positivas. log1p_servicos = ln(1+serviços gerais), apenas S1. Pessoal 88888 vira missing por definição documentada; zero válido. Binários 0/1 sem soma. ICG, dependência, localização e UF categóricos. Município é cluster, não efeito fixo. Demais indicadores mantêm unidades originais. IDEB 2023: 0–10; abandono 2022: pontos percentuais, somente S2. Missing exigidos removem escola da amostra comum. Definições detalhadas de INSE/IRD continuam dependentes da documentação oficial arquivada; não são escalas de FM.
