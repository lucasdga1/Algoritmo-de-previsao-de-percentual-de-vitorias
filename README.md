# Algoritmo-de-previsao-de-percentual-de-vitorias

# Objetivo
* O objetivo principal deste projeto é desenvolver um algoritmo de machine learning capaz de prever a quantidade percentual de vitórias esperadas de uma equipe de basquete, ao final de uma temporada, de acordo com as estatísticas fornecidas ao modelo.
* Neste projeto também foi feita uma análise do desempenho da equipe de basquete profissional do Brasília na temporada 2025/2026 em comparação com a temporada 2024/2025.
* Também foi feita uma análise dos jogos da equipe do Brasília contra as 5 equipes mais bem colocadas na temporada 2025/2026 relatando achados importantes.
* Ao final do projeto, foi feita uma análise do que pode mudar na equipe do Brasília, em termos estatísticos, para alcançar o percentual necessário para a 1ª colocação na temporada 2026/2027, de acordo com a previsão do MML gerado.

# Dataset
## Resultados das temporadas e partidas
* O dataset foi retirado a partir de um scrape das tabelas salvas em html no site: https://basketball.realgm.com
* Os HTMLs podem ser encontrados nas seguintes pastas do projeto: 
* <a href="https://github.com/lucasdga1/Algoritmo-de-previsao-de-percentual-de-vitorias/blob/main/HTML_Classificacao.zip">HTML_Classificação parte 1</a>
* <a href="https://github.com/lucasdga1/Algoritmo-de-previsao-de-percentual-de-vitorias/blob/main/HTML_Classificacao_2.zip">HTML_Classificação parte 2</a>
* <a href="https://github.com/lucasdga1/Algoritmo-de-previsao-de-percentual-de-vitorias/blob/main/HTML_Classificacao_3.zip">HTML_Classificação parte 3</a> 
* <a href="https://github.com/lucasdga1/Algoritmo-de-previsao-de-percentual-de-vitorias/blob/main/HTML_Partidas.zip">HTML_Partidas</a>

## Shot charts utilizados
* Os Shot charts foram obtidos de capturas de tela do site oficial da NBB: https://lnb.com.br/
* Os PNGs podem ser encontrados na seguinte pasta do projeto: 
* <a href="https://github.com/lucasdga1/Algoritmo-de-previsao-de-percentual-de-vitorias/tree/main/PNGs">PNGs</a>

# Tecnologias Utilizadas
* Python: Linguagem de programação utilizada para análise de dados e machine learning.
* Pandas: Biblioteca para manipulação e análise de dados.
* NumPy: Biblioteca para operações numéricas.
* Matplotlib e Seaborn: Bibliotecas para visualização de dados.
* Plotly: Biblioteca para visualização de dados.
* Scikit-learn: Biblioteca para machine learning, utilizada para aplicação dos algoritmos.
* Beautiful Soup: Biblioteca para parser de HTML.
* MplBasketball: Biblioteca para criação de shot charts (visualização de arremessos na quadra).
* OpenCV: Biblioteca para processamento de imagens.


# Metodologia
## Coleta e processamento dos dados
1. Os dados das temporadas e das partidas foram extraídos do HTML, processados e salvos em CSV para serem utilizados como dataframes nas análises e códigos posteriores.
2. Cada dataframe gerado pode ser acessado nas seguintes pastas:
3. <a href="https://github.com/lucasdga1/Algoritmo-de-previsao-de-percentual-de-vitorias/tree/main/Df_Partidas">Df_partidas</a> (para os dataframes das partidas)
4. <a href="https://github.com/lucasdga1/Algoritmo-de-previsao-de-percentual-de-vitorias/tree/main/Classificacao_NBB">Classificação_NBB</a> (para os dataframes das temporadas)
5. Cada dataframe conta com dados que foram limpos, selecionados e processados de acordo com a importância para a modelagem e análise.
6. Para o shot chart foram tiradas capturas de tela, dos acertos e erros das equipes, em PNG de cada um dos 10 jogos (ida e volta) da temporada regular da equipe do Brasília contra os 5 melhores colocados na temporada 2025/2026. 
7. Os PNGs foram processados pelo OpenCV e transformados em um dataframe de coordenadas x e y de acordo com os parâmetros utilizados pela biblioteca MplBasketball.
8. Os dataframes foram separados em acertos e erros, dos adversários e do Brasília.
9. Os dataframes podem ser acessados na seguinte pasta:
10. <a href="https://github.com/lucasdga1/Algoritmo-de-previsao-de-percentual-de-vitorias/tree/main/Shot_Charts">Shot_Charts</a> 

## Análise entre temporadas e contra adversários
1. Foram comparadas as estatísticas que demonstraram maior correlação com a variável alvo (Win %: percentual de vitórias na temporada):
2. PPG: Média de pontos por jogo.
3. Ast/TO: Razão entre a média de assistências geradas pelo time e a média de perdas de posse de bola.
4. ORtg: Medida de potenciais pontos gerados por 100 posses.
5. DRtg: Medida de potenciais pontos concedidos por 100 posses dos adversários.
6. eDiff: Diferença líquida entre ORtg e DRtg.
7. TS%: Uma medida de eficiência em tentativas, considerando tentativas de 3 pontos e lances livres. 
8. Def: Média de rebotes defensivos.
9. Reb: Média de rebotes totais.
10. FTM: Média de lances livres convertidos.
11. 3PM: Média de tentativas de 3 pontos convertidas .
12. Na análise contra os principais adversários, os dados foram divididos em 4 dataframes diferentes para que a comparação fosse realizada. Quando os adversários venceram, quando perderam, quando o Brasília venceu e quando perdeu.

### Cores utilizadas nas análises
* Como eu simulei um trabalho feito para a equipe de basquete profissional do Brasília, as cores foram escolhidas a partir da paleta de cores da equipe para gerar uma identidade visual.
* Dourado: #AB9034
* Azul escuro: #1C2846
* Creme: #E8E7E4
* Cinza: #A1A2A5
* Cinza escuro: #5B6070
* Amarelo pálido: #C1AF77
 
### Escolha das temporadas e adversários
* Para a análise comparativa e relatório de melhorias, foram escolhidas a temporada 2024/2025 e a temporada 2025/2026.
* Os adversários foram escolhidos de acordo com suas classificações finais na temporada 2025/2026. Sendo escolhidos os 5 melhores.

## Análise de variáveis pré-modelagem
1. Foram comparadas variáveis das 8 temporadas mais recentes (contando com a temporada alvo do modelo: 2025/2026) por causa das adaptações feitas ao torneio a partir da temporada 2017/2018.
2. Foi dado destaque às equipes com performances mais consistentes nas temporadas analisadas e à equipe do Brasília por ser o ponto focal do projeto.
3. Foram criados gráficos de correlação entre as variáveis para observar quais tinham maior impacto na variável alvo e se existia uma diferença considerável na lista de variáveis impactantes entre as temporadas.
4. Foi criado um dataframe com os primeiros colocados das temporadas para observar qual era a média e o desvio padrão da variável alvo para que uma equipe conquistasse essa colocação.
5. Foi observado que o primeiro colocado da temporada 2016/2017 se apresentava como um outlier e, por isso, foi retirado da análise.
<img width="1299" height="450" alt="Boxplot_outlier" src="https://github.com/user-attachments/assets/10cab0ad-b4a2-4d5b-82cb-a30438cef522" />

### Escolha de equipes a serem observadas
* Para a análise de variáveis foram escolhidas as equipes que demonstram estar mais consistentemente presentes nas disputas finais do campeonato, e o próprio Brasília por ser o ponto focal do projeto.
* As equipes selecionadas foram: Franca, Flamengo, Minas e Bauru

## Treinamento dos modelos
1. Para a definição do modelo preditor foram testadas as performances do ElasticNet, Random Forest e XGBoost.
2. Foi criada uma coluna com o ano da temporada em cada dataframe para realizar o cross-validation com validação por temporada, para que as previsões fossem mais robustas e próximas da utilização em ambientes reais.
3. Os dataframes foram separados em 2, sendo que o teste seria somente a temporada 2025/2026 para que o modelo pudesse prever num ambiente mais próximo do real, e o dataframe de treino foi uma concatenação das outras temporadas.
4. Os modelos foram treinados com o uso de um pipeline, para maior consistência, de PCA, para redução e equalização de dimensionalidade, de scaler, para normalização das variáveis, e de random search, para definição dos melhores hiperparâmetros.
5. Também foi feito um treinamento de Stacking para tentar alcançar uma performance melhor.

## Avaliação
1. A avaliação dos modelos no treinamento e sua escolha foram baseadas nos scores de erro quadrático médio (mse) e no desvio padrão das previsões.
2. O método, na etapa de treino, foi o uso de cross-validation dividido nos grupos de temporadas disponíveis.
3. Na etapa de teste foram avaliados os scores de R² e erro médio quadrado (mse)

# Resultados 
## Análise de variáveis
* É possível perceber que não há correlação clara entre o ritmo de jogo médio de um time (Pace) e sua quantidade de vitórias na temporada.
<img width="1299" height="450" alt="Pace_Vitorias" src="https://github.com/user-attachments/assets/4e2223e9-ce30-4b0b-95a6-2f910a32a9b4" />

* Porém, podemos notar que existe uma concentração dos times com maior número de vitórias próxima à média de Pace da liga.
* Não há uma correlação clara entre o volume de tentativas de 3PT e a quantidade de vitórias, mas uma boa parte dos times com maior número de vitórias se encontra perto da média da liga (entre 43.5% e 45.8%).
<img width="1299" height="450" alt="Volume3PT_Vitorias" src="https://github.com/user-attachments/assets/105cd4f5-4e06-455a-bd62-c49b5ab9e403" />

* A análise retornou uma correlação positiva. Logo, os times que pegam mais rebotes de todas as tentativas (ofensivas e defensivas) tendem a ter uma performance líquida melhor.
* É importante perceber que o time do Brasília Basquete se apresentou como outlier em duas situações:
* A primeira na temporada 2023/2024, na qual teve um total percentual de rebotes baixo, e, por isso, obteve uma performance líquida baixa;
* A segunda na temporada 2021/2022, na qual, mesmo tendo um percentual de rebotes acima da média geral da liga, obteve uma performance líquida negativa.
<img width="1299" height="450" alt="TotalRebotes_NetRating" src="https://github.com/user-attachments/assets/8f1d361d-b618-4c46-a304-ae2314777062" />

* A análise demonstra que não há correlação entre o percentual de assistências em tentativas certas e o percentual de acertos efetivos.
* Isso indica que ter uma boa parte das jogadas convertidas terminando em passes não garante um percentual de conversões efetivas maior.
<img width="1299" height="450" alt="Assistencias_eFG" src="https://github.com/user-attachments/assets/b2aa49ca-ebc3-46a9-8723-3e636cd39f4a" />

* A análise demonstra haver correlação positiva entre a performance líquida de um time e o percentual de vitórias daquele time na temporada.
* A análise também demonstra que o time do Brasília Basquete conseguiu obter mais de 50% de vitórias quando superou a média de performance líquida da liga na temporada 2024/2025.
<img width="1299" height="450" alt="NetRating_Vitorias" src="https://github.com/user-attachments/assets/131a9634-ba4c-4cb0-baee-7b86c22165f6" />


### Os que demonstram correlação positiva, excluída a variável alvo (W%), são:

* ASS/TO = 0,86
* eDiff = 0,95
* ORTG = 0,93
* TS% = 0,90
* eFG% = 0,91
* FT% = 0,70
* 3PT% = 0,83
* FG% = 0,87
* PPG = 0,87

###Os que demonstram correlação negativa são:

* DRTG = -0,81
* TOV = -0,61

<img width="1299" height="450" alt="Correlacao_25-26" src="https://github.com/user-attachments/assets/bd185ee5-bbe9-427a-a3d9-58c0342c7197" />

## Análise entre temporadas
* Baseados nos fatores que mais impactam as vitórias das equipes, segundo o gráfico de correlação de variáveis, podemos perceber que as maiores mudanças entre a temporada passada e a atual foram o aumento de pontos por partida e a melhora na eficiência defensiva (DRtg).
* Pode-se inferir que as maiores diferenças estatísticas positivas entre as temporadas são o aumento percentual dos acertos de quadra (FG%), o percentual total de rebotes (TRB%) e a quantidade média de rebotes defensivos por jogo (DRB).
* Com relação aos acertos de quadra, veremos mais adiante se é reflexo de uma concentração maior em tentativas de meia distância ou finalizações perto da cesta.
<img width="1310" height="450" alt="Comparacao_BSB_1" src="https://github.com/user-attachments/assets/7b304e2e-e798-4227-9fbb-721b68425a45" />
<img width="1310" height="450" alt="Comparacao_BSB_2" src="https://github.com/user-attachments/assets/88ed9812-eda5-4c6e-98c3-bb9a7056de71" />


## Análise de confrontos
Quando comparamos as performances do Brasília contra os principais adversários na temporada atual podemos inferir que:

* Em termos de pontos por jogo, o Brasília ganha jogos quando marca mais pontos (+10.75), mas sem limitar necessariamente os pontos do adversário. O que mostra uma predominância ofensiva na equipe;
<img width="1310" height="450" alt="PTS_Adv_x_BSB" src="https://github.com/user-attachments/assets/0777c72d-c3f3-4900-b489-4863d1c52a58" />

* Em termos de assistências e turnovers, a figura se repete e permite inferir que um ataque que comete menos turnovers por jogo auxilia nas vitórias da equipe (+ 0.43);
<img width="1310" height="450" alt="AST-TO_Adv_x_BSB" src="https://github.com/user-attachments/assets/35b1b9fa-3fec-4bf0-bc81-717ed001077d" />

* Quando comparamos eficiências ofensivas, defensivas e líquidas, é possível confirmar os pontos anteriores porque a maior diferença, em termos de vitória e derrota, ocorre na diferença na eficiência ofensiva (+ 13.69);
<img width="1310" height="450" alt="ORtg_Adv_x_BSB" src="https://github.com/user-attachments/assets/79295a12-a77f-43b4-bfdc-a095a69ddf28" />

* Em termos de aproveitamento de quadra corrigido (TS%), podemos inferir que existe uma diferença positiva percentual significativa quando o Brasília vence (+ 4.72%). Porém, para os adversários, essa diferença se mostrou negativa, ou seja, quando vencem, têm um aproveitamento corrigido menor (- 4.38%).
<img width="1310" height="450" alt="TS_Adv_x_BSB" src="https://github.com/user-attachments/assets/3e314ebb-caf7-4d76-8e5f-1ca044b801db" />


Vamos comparar mais alguns fatores para tentar encontrar mais variáveis que podem impactar as vitórias do Brasília.

Pode-se observar alguns pontos interessantes a partir dos gráficos:
* Os adversários registram, em média, 4.42 rebotes defensivos a mais quando vencem o time do Brasília. Isso pode ocorrer pelo fato do time do Brasília pegar menos rebotes ofensivos quando perde e/ou errar mais arremessos quando perde;
<img width="1310" height="450" alt="DREB_Adv_x_BSB" src="https://github.com/user-attachments/assets/7aac1966-8639-414f-9776-c7f2b2733c62" />

* O time do Brasília não registrou diferença significativa nas estatísticas de rebotes (defensivos ou totais) nem de cestas de 3 pontos convertidas quando venceu ou perdeu as partidas;
<img width="1310" height="450" alt="TREB_Adv_x_BSB" src="https://github.com/user-attachments/assets/a1915029-16ce-497e-a26e-4bebf4b22925" />

* O Brasília registrou uma diferença de 4.58 lances livres convertidos quando vence as partidas;
<img width="1310" height="450" alt="FTM_Adv_x_BSB" src="https://github.com/user-attachments/assets/acb50540-6bcb-4a2e-bd4b-3489ae436df3" />

* Quando os adversários venceram as partidas, registraram mais rebotes totais, porém registraram menos lances livres convertidos e menos arremessos de 3 pontos convertidos (-2.83) também.
<img width="1310" height="450" alt="3PM_Adv_x_BSB" src="https://github.com/user-attachments/assets/d246a4d8-ef3d-493f-9208-7ea1d4ab0bcb" />


## Análise de shot charts
### Adversários
* Observa-se que há uma concentração de erros no topo da linha de 3 pontos, na cabeça do garrafão, nas zonas mortas de 3 pontos e perto da cesta.
* Os erros perto da cesta causam estranheza em um primeiro momento por ser, teoricamente, o local com maior chance de acertos. Logo, esses erros podem ser consequência de segundas chances criadas, rebotes ofensivos ou algum trabalho de dobra defensiva.
<img width="1589" height="720" alt="Shot_erros_Adv" src="https://github.com/user-attachments/assets/6ca6e18c-8eb7-44b9-9d61-dc86e33b3034" />


Observa-se uma concentração de arremessos convertidos no topo da linha de 3 pontos, nas zonas mortas da linha de 3 pontos e perto da cesta.
<img width="1589" height="720" alt="Shot_acertos_Adv" src="https://github.com/user-attachments/assets/27783964-2f6f-4767-94c3-b6136f4955c4" />

Se comparado com o gráfico de arremessos errados, faz-se necessário avaliar alternativas defensivas que forcem o time adversário a arremessar mais da meia distância e das alas da linha de 3 pontos, porque são áreas da quadra onde a concentração de erros supera bastante a de acertos.


### Brasília
A distribuição de arremessos errados do Brasília é mais uniforme que a dos adversários, mas ainda com pontos de concentração perto da cesta, dentro do garrafão (incluindo a cabeça do garrafão) e no topo da linha de 3 pontos.
<img width="1589" height="720" alt="Shot_erros_BSB" src="https://github.com/user-attachments/assets/d90fc89b-48b9-4286-99cf-2179e95673ad" />


Observa-se que o gráfico de arremessos convertidos se assemelha, em termos de concentração, ao gráfico de erros. Isso significa que a equipe concentra seus ataques nessas áreas da quadra.

Tendo em vista o pequeno volume de acertos ao redor da linha de 3 pontos, em comparação com os erros, mostra-se necessário melhorar o aproveitamento dessa região da quadra, não só para aumentar a diversidade ofensiva, mas também para aumentar a eficiência no garrafão (tornando esta área ainda mais efetiva para a equipe), uma vez que uma alta eficiência nos 3 pontos tende a gerar mais espaços perto da cesta.
<img width="1589" height="720" alt="Shot_acertos_BSB" src="https://github.com/user-attachments/assets/850cdb12-5640-47c5-83f1-9475e1c9d003" />


## Performance dos modelos
### Treino
Após análise dos resultados de erros quadrados médios dos hiperparâmetros pode-se observar:

* O modelo Elastic Net apresenta um erro médio nas previsões de 7.7 pontos percentuais, enquanto o XGboost e o Random Forest apresentam um erro médio de 9.8 pontos percentuais. Isso é um ganho de 38% para o primeiro modelo.

### Teste
* Resultados do Elastic Net. R2: 0.9559351744750954. MSE: 0.002182975862986331
* Resultados do Random Forest. R2: 0.8703204306713141. MSE: 0.006424338832500031
* Resultados do XGboost. R2: 0.9152803988893227. MSE: 0.0041970175109830666

* Os resultados obtidos indicam que o modelo linear regularizado (Elastic Net) explica melhor a variação de Win%.
* O R² alto e o MSE baixo indicam previsões mais estáveis entre seasons, podendo ser valiosos para metas operacionais.
<img width="1299" height="450" alt="R2score_ElasticNet" src="https://github.com/user-attachments/assets/e5065527-a559-48a4-91be-6a51c68bbf68" />


### Stacking
* Resultados do Elastic Net Stack. R2: 0.8817855597249803. MSE: 0.005856355192668505
* O stack dos modelos apresentou um desempenho inferior ao do ElasticNet, por isso este foi escolhido.

## Mudanças a serem implementadas pela equipe
* O percentual de vitórias dos primeiros colocados em uma temporada apresentou média de 85,5% e desvio padrão de 4.9%, com máximo de 94,7%.

### Estatísticas e impactos percentuais na construção do modelo
Impacto percentual no modelo considerando a variação isolada de cada uma dessas features: 
* FG%                 0.586553
* 3P%                 0.395115
* TS%                 0.386241
* eFG%                0.382010
* FT%                 0.249253
* Ast/TO              0.074449
* BPG                 0.017217
* TOV                -0.015072
* SPG                 0.013408
* STL%                0.012729

* Com média de 32% de acertos de 3 pts, o time do Brasília conseguiu obter 73% de vitórias na temporada.
* Como o aumento das estatísticas no esporte não acontece de maneira isolada, fiz um aumento proporcional em todas as estatísticas afetadas pelo aumento no 3PT%. 
* Conforme o modelo, o time do Brasília poderia aumentar os acertos percentuais médios de 3pt em 4 pontos percentuais, ou cerca de 1 cesta de 3pts a mais por jogo, para obter 84% de vitórias totais na temporada regular.

# Próximos Passos
* Aplicação de melhorias estratégicas na equipe do Brasília, tendo em vista os resultados acima.
* Futuras iterações deste projeto podem incluir a modelagem utilizando mais temporadas, mudando outras estatísticas, alterando a quantidade de colunas dos dataframes e utilizando a biblioteca TensorFlow (por ter uma capacidade computacional maior e possibilidade de deep learning).


# Como Executar
* Clone o repositório.
* Os códigos foram feitos na versão 3.12 do Python para compatibilidade com a biblioteca MplBasketball.
* Instale as dependências listadas no `requirements.txt`.
* Execute o script 'Scrape_Classificação.ipynb' para transformar HTML de temporadas em dataframe.
* Execute o script 'Scrape_Partidas.ipynb' para transformar HTML de partidas em dataframe.
* Execute o script 'Shot_import.ipynb' para transformar os PNGs em dataframes.
* Execute o script 'Analise_Brasilia.ipynb' para analisar performances.
* Execute o script 'Modelo_vitorias.ipynb' para executar o modelo de machine learning.


# Contribuições
* Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

# Autoria
Lucas Danziger Guimarães de Andrade

# Contato
<a href="mailto:lucas.dga1@gmail.com">Me envie um email<a/>
