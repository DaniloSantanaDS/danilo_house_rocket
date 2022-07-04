# House Rocket Company

<img src="https://i.ibb.co/NrShDJt/house-rocket-link2.png" alt="logo" style="zoom:100%;" />

[<img alt="Heroku" src="https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white"/>](https://danilo-house-rocket.herokuapp.com/)


## 1. DESCRIÇÃO
A House Rocket é uma empresa do ramo imobiliario, no qual trabalha na compra de imóveis, reforma e revenda para gerar lucro, procurando o melhor momento para revender o mesmo. A empresa solicitou a equipe de dados para fazer uma analise precisa para gerar o maior lucro possível dentro das compras e revenda de 10 imóveis. A estrátegia utilizada foi a compra de imóveis com boas condições, atrelando a venda a epóca do ano, visto que em diferentes épocas existe uma variação de preço.

- Quais casas o CEO da House Rocket deveria comprar e por qual preço de compra?

- Uma vez a casa em posse da empresa, qual o melhor momento para vendê-las e qual seria o preço da venda?

### FERRAMENTAS UTILIZADAS

- Jupyter Notebook
- Python 3.10.2
- PyCharm Community
- Streamlit
- Heroku

## 2. ATRIBUTOS
A base de dados foi do kaggle: https://www.kaggle.com/datasets/harlfoxem/housesalesprediction

|    Atributos   |	                                    Significado                             |
| :------------: | :----------------------------------------------------------------------------: |
|       id       |	                         Número de identificação do imóvel                  |
|      date	     |                     Data em que casa ficou disponivel para compra           |
|    bedrooms    |                              'Números de quartos da casa                    |
|    bathrooms   |                    Números de banheiros disponiveis                 |
|   sqft_living  |            Tamanho em pés quadrado do tamanho dos espaço dentro do imóvel' |
|    sqft_lot    |     	            'Tamanho em pés quadrado do terreno do imóvel            |
|     floors     |                       	Número de andares do imóvel                     |
|   waterfront   |    Indica se o imóvel tem vista para a água ou não, 0 = 'Não' ou 1 = Sim|
|      view      |                          Qualidade da vista do imóvel                    |
|    condition   |Condição do imóvel de 1 a 5, sendo 1 a pior condição e 5 a melhor condição|
|      grade     |	                       Um indicador de desing de construção           |
|  sqft_basement |                             A área do porão da residência                  |
|     yr_built   |	                           Ano que o imóvel foi construído                |
|   yr_renovated |                          	Ano que o imóvel foi reformado                  |
|     zipcode    |                                      	  CEP                              |
|       lat      |	                                      Latitude                            |
|       long     |	                                     Longitude                           |

## 3. PREMISSAS DO NEGOCIO

- Retirado um possível erro de um imóvel de 33 quartos
- Tomando como base, imóveis que tenha o (yr_renovated = 0), são casas que nunca passaram por uma reforma.
- Criado uma coluna para identificar a estação do ano que o imóvel foi vendido, baseada na data da coluna (date).
- A coluna (price), indica o preço que a casa será comprada pela empresa

## 4. ESTRATÉGIA UTILIZADA

1. Coleta de dados Via Kaggle Dados

2. Entedimento do negócio

3. Verificação de dados

- Criação de Variáveis
- Limpeza
- Criação de hipoteses
- Entendimento e criação de Insights

4. Respondendo problemas de negocio

5. Resultado para o negócio

6. Conclusão

## 5. HIPOTESES
| HIPOTESE |	RESULTADO	| VALOR PARA O NEGOCIO |
| :------------: | :----------: | :----------------------------------------------------------------------------: |
| H1: Imóveis com vista para a água são em média 30% mais caros	| FALSA	| A média de preço 212.64% para imóveis com vista para água. |
| H2: Imóveis com data de construção menor do que 1955, são 50% mais baratos na média.| FALSA |A média de preço como observado é de 0.79%. |
| H3: Imóveis sem porão são 50% maiores do que com porão. | VERDADEIRA | O valor é maior 89.56%. |
| H4: O crescimento do preço dos imóveis YoY ( Year overYear ) é de 10%. | FALSA | O ideial seria ter mais anos para realizar a analíse, em 2014 e 2015 o crescimento foi de 0.52%. |
| H5: Imóveis com 3 banheiros tem um crescimento de MoM de 15%|	FALSA |	A media é 0.45% |
| H6: Em média, os preços de venda ficam mais caros no verão |	FALSA |	Hipotese importante para o resultado final, os preços ficam melhores na primavera. | 
| H7: Ter mais quartos não necessariamente fará o imóvel ser mais caro | VERDADE | Casas com mais quartos não interferem no valor do imovel. |
| H8: A condição mais em conta para comprar os imóveis é a condição mais alta? | FALSA |	Pelo estudo feito, uma condicão 4 possuem menores valores que um imovel em condicao 3. |

## 6. TOP INSIGHTS

- Casas com vista para a água sã 212% mais caras, logo encontrar uma casa com um valor baixo, faz com que possamos vende-la no preço máximo.
- Procurar casas com condição 4, em mediana, elas possuem preços mais baratos que as casas de condição 3.
- O melhor periódo de compra é nos 3 meses de inverno, onde as casas ficam mais baratas.
- Comprar casa no inverno e vender na primavera, gera um lucro maior, e também a empresa não precisa segurar muito tempo um imóvel, visto que são estações uma ao lado da outra.

## 7. Conclusão
Foi entregue uma lista de recomendação de compra para o CEO, via site. Entregue no HEROKU.

| PROCESSO |	CAPITAL |
|:--------:|:--------:|
| Investimento Inicial | US$ 3219492.0 |
| Lucro	| US$ 965847.60 |

## 8. RELATORIO FINAL
Chegada a conclusão baseado na hipotese 1 e 8, onde imóveis com vista para água são bem mais caros e valiosos e que a condição 4, mantem um bom preço de compra, foi idenfiticado um imóvel em boa condição de compra no qual podemos aplicar 30% do valor na hora da venda. Também foi visto que a estação do ano da Primavera, contem os preços mais caros de venda, a empresa então deve manter a compra dos imóveis no inicio do inverno e então vender na primavera. O inverno, periódo onde os imóveis estão mais baratos, precede a primavera onde os imóveis ficam mais caros, então a empresa não precisa segurar muito tempo o imóvel e ter risco de perca de valor com o passar dos anos.

## 9. PRÓXIMOS PASSOS
Verificar o valor gasto em reformas e comparar com o preço de venda, quando gastariamos para reformar uma imóvel de condição 1 e deixa-lo em condição de venda e qual seria o lucro no processo de venda do imóvel.
