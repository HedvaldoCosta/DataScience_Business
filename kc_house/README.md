<p align="center">
  <img src="https://user-images.githubusercontent.com/67663958/122058746-4fbbf680-cdc2-11eb-9da7-8853ecf8894e.gif" width="600" />
</p>

### Link para o aplicativo: (https://insight-project-rocket-house.herokuapp.com/)
## Objetivo
Utilizar a análise e manipulação de dados para auxiliar na tomada de decisões do time de negócios de uma empresa de imóveis denominada como Kc House
 
## Questão de negócio
<p>Kc House é uma empresa de imóveis que deseja comprar casas, para poder reformá-las e depois vendê-las, na cidade de Seattle.</p>
<p>O CEO da empresa deseja um relatório com as melhores casas para a compra com o seu preço e o porquê, após a compra é necessário relatar qual seria o melhor momento para a venda do imóvel e o quanto de lucro o imóvel arrecadaria.</p>

| compras  | vendas  |   
|---|---|
| compras > mediana  | valor da compra + 30%  |  
|  compras < mediana | valor da compra + 10%  |  

## Premissas de negócio
* Casas beira-mar possuem um preço maior de venda
* Casas com número de quartos igual a 0 ou maior do que 10 devem ser excluídas do dataset

## Planejamento da solução
* Extração dos dados: Dataset retirado de: (https://www.kaggle.com/shivachandel/kc-house-data)
* Análise dos dados: Limpeza e transformação dos dados com o objetivo de encontrar informações úteis e construir insights para a resolução do problema
* Seleção de recursos: Selecionando os melhores atributos para a construção do relatório utilizando mapa e filtros
* Publicação: Publicação do relatório no Heroku

## Principais insights
* O zipcode com a maior média de preços é o 98103 por possuir mais imóveis beira-mar
<p>Falso: O zipcode com maior média de preços é o 98039</p>

* Casas com a condição nível 3 são a maioria entre os imóveis

* Casas mais novas são mais caras do que antigas
<p>Falso: A média de preços entre casas antigas e novas é muito variada para achar uma afirmação</p>
