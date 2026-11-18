# Implementação de políticas públicas e infraestrutura escolar — Replicabilidade

**Pacote técnico de reprodução numérica** preparado em 18 de novembro de 2026. Este repositório não representa artigo submetido, aceito ou publicado. O manuscrito, as decisões dos coautores e o histórico editorial não são disponibilizados aqui.

## O que este repositório permite reproduzir

A partir da base analítica final, o código reproduz os modelos M0, M1 e M2, as sensibilidades S1 e S2, a especificação flexível S3 e as estimativas com erros-padrão CR1 agrupados por município e HC3. Foram analisadas **27.315 escolas públicas**, distribuídas por **5.228 municípios**, utilizando Censo Escolar 2022, INSE 2021, IRD/ICG 2022 e IDEB dos anos finais de 2023.

Os três indicadores físicos observam dependências declaradas como existentes e utilizadas. Não são medidas de conservação, manutenção, intensidade de uso ou qualidade do Facilities Management. O estudo é observacional e não identifica efeitos causais.

**Limite de replicabilidade:** os scripts aqui publicados partem da base analítica final. A reconstrução integral dessa base desde os microdados brutos do INEP depende da consolidação e validação de uma rotina ETL pública adicional.

## Estrutura

- [Base analítica](data/base_analitica_final.csv): 27.315 linhas, 17 colunas, registro por escola.
- [Script de reprodução](scripts/reproduzir_resultados.py): cálculo independente das pastas e dos documentos privados dos autores.
- [Resultados congelados](resultados/): coeficientes dos modelos, sensibilidades, diagnósticos e comparação CR1/HC3.
- [Protocolos e dicionário](protocolo/): especificações do estudo e das medidas.
- [Fontes INEP](FONTES_INEP.md) e [notas de publicação](NOTAS_ETICA_E_PUBLICACAO.md).
- [Arquivo ZIP auditado](pacote_replicabilidade_RAP_INEP_2022_2023.zip): cópia completa do pacote técnico original, incluindo manifesto de hashes. **O script PUBLICAR_GITHUB.ps1 contido nesse ZIP é apenas histórico de distribuição, e não deve ser executado neste repositório já criado.**

## Instruções de execução

Recomendado: Python 3.11 ou superior, com NumPy, pandas e SciPy.

~~~bash
python -m pip install -r requirements.txt
python scripts/reproduzir_resultados.py --rapido
python scripts/reproduzir_resultados.py --saida reproducao_local
~~~

A opção **--rapido** executa M0–M2. A execução completa também reestima S1, S2 e S3. A pasta **reproducao_local/** é gerada apenas quando solicitada e não é versionada. O script valida o SHA-256 da base e confronta coeficientes, intervalos de 95% e valores p com os resultados congelados.

Verificação técnica realizada em 18/11/2026: M0–M2 (230 linhas), S1/S2 (242 linhas) e S3 (46 linhas), tolerância absoluta de 2×10⁻⁷. R² reproduzidos: M0 0,450677525; M1 0,451773782; M2 0,451902623; S3 0,459297950.

A inferência principal usa CR1 por município. O estimador HC3, embora robusto à heterocedasticidade, não considera correlação entre escolas do mesmo município.

## Integridade, licenças e atribuição

A base foi derivada de dados públicos institucionais do **INEP**, sem registros de indivíduos. As fontes oficiais estão documentadas em [FONTES_INEP.md](FONTES_INEP.md). O uso de dados públicos exige respeitar os termos aplicáveis de reutilização; nenhuma licença de terceiros é concedida aqui. A licença autoral do código permanece pendente de decisão dos coautores.

O código de replicação foi organizado com assistência de IA a partir de scripts e protocolo congelados, e foi confrontado numericamente com os resultados originais. A responsabilidade científica e a decisão sobre publicação do artigo permanecem com os autores.

**Atenção para avaliação duplo-cega:** a vinculação direta deste repositório a um manuscrito anonimizado pode revelar seus responsáveis. Sua utilização em submissão deverá respeitar as orientações da RAP/FGV.

Não há DOI do artigo ou do conjunto de dados nesta versão. Para arquivamento estável e DOI, recomenda-se depósito posterior em um repositório de dados como Zenodo, após deliberação dos autores.
