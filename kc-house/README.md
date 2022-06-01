![2022-01-17-19-53-36](https://user-images.githubusercontent.com/67663958/149845434-135dc4b3-46e2-4c44-a361-4ff156c6b73a.gif)


### Aplicação construída para a resolução:

https://share.streamlit.io/hedvaldocosta/datascience_business/main/kc-house/main.py

### Relatório 
https://app.powerbi.com/view?r=eyJrIjoiNWRjMzM4MTktZjA0NS00NzAyLTk1OGUtMmNjNzVlYWY1MzUyIiwidCI6ImU0NmMwZTRiLThhY2YtNDMyZC05NjE3LWM4ZWJmNDdlMjY3NSJ9&pageName=ReportSection



# Resumo do problema

A **House Rocket** é uma plataforma digital que tem como modelo de negócio, a compra e a venda de imóveis usando tecnologia.

Você é um Data Scientist contratado pela empresa para ajudar a encontrar as melhores oportunidades de negócio no mercado de imóveis. O CEO da House Rocket gostaria de maximizar a receita da empresa encontrando boas oportunidades de negócio.



# Questão de negócios

1. **Quais casas o CEO da House Rocket deveria comprar e por qual preço de compra?**
2. **Uma vez a casa em posse da empresa, qual o melhor momento para vendê-las e qual seria o preço da venda?**
3. **A House Rocket deveria fazer uma reforma para aumentar o preço da venda? Quais seriam as sugestões de mudanças? Qual o incremento no preço dado por cada opção de reforma?**



# Levantamento de hipóteses

1. **Casas com muitos quartos costumam ter a média de preço mais alta?** Sim, casas com 5 a 6 possuem uma média de preço maior do que as com 1 a 4 quartos. No entanto, o total somado de casas com 5 a 6 quartos é inferior ao total de casas que possuem 3 quartos e a média do preço dessas casas é aproximadamente metade das com 5 quartos.
2. **Existem mais casas que não sejam beira-mar?** Sim. O total de casas sem beira-mar totaliza em 99%
3. **Em que região estão as casas mais caras?** As regiões com maior média de preço costumam ficar próximas da água.



# Planejamento da solução

Retirando os dados do kaggle (https://www.kaggle.com/shivachandel/kc-house-data), e importando no Jupyter Notebook para fazer a análise exploratória de dados, é possível criar insights para um melhor desenvolvimento da solução e descobrir dados que tendem a ser desnecessários para a aplicação. Aplicando a limpeza e transformação dos dados, que irão aprimorar o que necessitamos para resolver o problema, a partir do pycharm, e selecionando os melhores atributos, levando em conta o que é pedido, é possível construir um relatório utilizando mapa e filtros que sejam colocados em produção no Streamlit, assim, facilitando a tomada de decisão.
