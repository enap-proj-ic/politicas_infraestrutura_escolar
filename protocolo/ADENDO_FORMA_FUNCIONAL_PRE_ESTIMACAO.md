# Adendo dirigido de forma funcional — congelado antes da estimação

Autorização: prompt de encerramento empírico recebido nesta rodada. Alteração limitada à não linearidade previamente detectada. O protocolo e modelos principais permanecem preservados.

Uma única especificação adicional S3: M2 acrescido de termos de spline cúbica restrita (caudas lineares) para INSE 2021, IRD 2022 e log(matrículas 2022). Cada spline terá quatro nós nos percentis 5, 35, 65 e 95 da amostra completa já fixada, com interpolação linear dos quantis. São três graus de liberdade por covariável (um linear preexistente e dois não lineares), seis parâmetros adicionais no total. Os nós serão registrados, nunca selecionados por p ou ajuste.

Biblioteca/sala de leitura, banheiro acessível, laboratório de ciências e quantidade de serviços gerais mantêm suas escalas e coeficientes focais. A quantidade de pessoal continua linear para permitir comparação direta com M2; a transformação log1p já foi coberta pela S1. Assim S3 não é prova de adequação de toda a forma funcional, mas verifica a estabilidade focal ao flexibilizar controles contínuos. ICG, dependência, localização e UF permanecem categóricos, com as mesmas referências.

Usar os mesmos 27.315 IDs, 5.228 municípios, desfecho e regras de missing. OLS com CR1 municipal e t(G−1) para IC95%/p. Reportar todos os coeficientes, R², comparação focal com M2, diferenças absolutas e IC, teste conjunto dos seis termos adicionais por Wald-F agrupado. Não substituir modelos principais ou escolher transformações por significância. Não excluir observações ou iniciar outra família.

Base de spline, com t1<...<t4 e j=1,2: termo não linear = [(x−tj)+³ − (x−t3)+³*(t4−tj)/(t4−t3) + (x−t4)+³*(t3−tj)/(t4−t3)]/(t4−t1)². A transformação linear já está em M2. Validar posto da matriz, equivalência numérica de soluções OLS, hash da amostra e preservação dos outputs anteriores.

A estabilidade será descrita por magnitude, sinal e intervalos, sem transformar p=0,05 em critério de seleção. Limitações e possíveis mudanças de interpretação serão encaminhadas aos autores. Encerrar as estimações após S3, salvo erro material.
