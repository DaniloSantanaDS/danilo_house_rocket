import streamlit as st
import pandas as pd
import numpy as np
import folium
import geopandas
import plotly.express as px
from datetime import datetime
from PIL import Image
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

st.set_page_config(layout='wide')
image=Image.open('house_rocket_link2.png')
st.sidebar.image(image,use_column_width=True,caption='HOUSE ROCKET COMPANY')


@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv('kc_house_data.csv')
    return data

def get_geofile(url):
    geofile = geopandas.read_file(url)

    return geofile

def set_feature(data):
    # conversions
    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')
    data['month'] = pd.to_datetime(data['date']).dt.month
    data['estacao_venda'] = data['month'].apply(lambda month: 'Verão' if (month >= 6) & (month <= 8) else
                                                              'Outuno' if (month >= 9) & (month <= 11) else
                                                              'Primavera' if (month >= 3) & (month <= 5) else
                                                              'Inverno')
    # add new feature
    data['mes'] = data['month'].apply(lambda month: 1 if (month == 1) else
                                                    2 if (month == 2) else
                                                    3 if (month == 3) else
                                                    4 if (month == 4) else
                                                    5 if (month == 5) else
                                                    6 if (month == 6) else
                                                    7 if (month == 7) else
                                                    8 if (month == 8) else
                                                    9 if (month == 9) else
                                                    10 if (month == 10) else
                                                    11 if (month == 11) else
                                                    12)


    data['m2_lot'] = data['sqft_lot'] * 0.093
    data['m2_basement'] = data['sqft_basement'] * 0.093
    data['price_m2'] = data['price'] / data['m2_lot']
    data['yr_built_1955'] = data['yr_built'].apply(lambda x: '1955_diante' if x >= 1955 else 'antes_1955')
    data['waterfrontview'] = data['waterfront'].apply(lambda x: 'Sim' if x == 1 else 'Não')
    data['not_basement'] = data['m2_basement'].apply(lambda sqft_basement: 'No_basement' if sqft_basement > 0 else 'Yes_basement')
    return data
# get data
path = 'kc_house_data.csv'
data = get_data(path)

# get geofile
url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
geofile = get_geofile(url)



# ========================
# Data Overview
# ========================

options = st.sidebar.radio(
     "Selecione a Opção que deseja",
     ('Premissa', 'Dados Gerais/Analises Descritivas', 'Mapas regionais', 'Atributos Comerciais', 'Hipóteses', 'Relatório Final'))


if options == 'Premissa':
    st.title ('Questão de Negócio')
    st.subheader('House Rocket Company')
    st.write('A House Rocket é uma empresa do ramo imobiliario, no qual trabalha na compra de imóveis, reforma e revenda para gerar lucro, procurando o melhor momento para revender o mesmo. A empresa solicitou a equipe de dados para fazer uma analise precisa para gerar o maior lucro possível dentro das compras e revenda de 15 imóveis. A estrátegia utilizada foi a compra de imóveis com boas condições, atrelando a venda a epóca do ano, visto que em diferentes épocas existe uma variação de preço.')
    st.subheader('Perguntas do CEO')
    st.write('1. Quais casas o CEO da House Rocket deveria comprar e por qual preço de compra?')
    st.write('2. Uma vez a casa comprada pela empresa, qual o melhor momento para vender a mesma?')
    st.subheader('Premisas de Negócio')
    st.write('* Retirado um possível erro de um imóvel de 33 quartos')
    st.write('* Tomando como base, imóveis que tenha o (yr_renovated = 0), são casas que nunca passaram por uma reforma.')
    st.write('* Criado uma coluna para identificar a estação do ano que o imóvel foi vendido, baseada na data da coluna (date).')
    st.write('* A coluna (price), indica o preço que a casa será comprada pela empresa')
    st.subheader('Estratégia Utilizada')
    link1 = '[Dados](https://www.kaggle.com/harlfoxem/housesalesprediction/discussion/207885)'
    st.write('1. Coleta de dados Via Kaggle')
    st.write(link1)
    st.write('2. Entedimento do negócio')
    st.write('3. Verificação de dados')
    st.write('3.1 Criação de Variáveis')
    st.write('3.2 Limpeza')
    st.write('3.3 Criação de hipoteses')
    st.write('3.4 Entendimento e criação de Insights')
    st.write('4. Respondendo problemas de negocio')
    st.write('5. Resultado para o negócio')
    st.write('6. Conclusão')
    st.subheader('Ferramentas Utilizadas')
    st.write('* Jupyter Notebotak')
    st.write('* Python 3.10.0')
    st.write('* PyCharm Community')
    st.write('* Streamlit')
    st.write('* Heroku')
    st.subheader('Conclusão')
    st.write('Chegada a conclusão baseado na hipotese 1 e 8, onde imóveis com vista para água são bem mais caros e valiosos e que a condição 4, mantem um bom preço de compra, foi idenfiticado um imóvel em boa condição de compra no qual podemos aplicar 30% do valor na hora da venda. Também foi visto que a estação do ano da Primavera, contem os preços mais caros de venda, a empresa então deve manter a compra dos imóveis no inicio do inverno e então vender na primavera. O inverno, periódo onde os imóveis estão mais baratos, precede a primavera onde os imóveis ficam mais caros, então a empresa não precisa segurar muito tempo o imóvel e ter risco de perca de valor com o passar dos anos.')
    st.subheader('Próximos Passos')
    st.write('Verificar o valor gasto em reformas e comparar com o preço de venda, quando gastariamos para reformar uma imóvel de condição 1 e deixa-lo em condição de venda e qual seria o lucro no processo de venda do imóvel.')

def overview_data(data):
    if options == 'Dados Gerais/Analises Descritivas':

        st.title('Dados Gerais')

        f_attributes = st.sidebar.multiselect('Enter columns', data.columns)
        f_zipcode = st.sidebar.multiselect('Enter Zipcode', data['zipcode'].unique())
        data1 = data.copy()

        if (f_zipcode != []) & (f_attributes != []):
            data = data.loc[data['zipcode'].isin(f_zipcode), f_attributes]

        elif (f_zipcode != []) & (f_attributes == []):
            data = data.loc[data['zipcode'].isin(f_zipcode), :]

        elif (f_zipcode == []) & (f_attributes != []):
            data = data.loc[:, f_attributes]

        else:
            data = data.copy()

        st.dataframe(data, height=400)

        c1, c2 = st.columns((1, 1))

        # average metrics

        if 'floors' or 'id' or 'zipcode' or 'price' or 'price_m2' or 'lat' or 'long' or 'date' or 'bathrooms' or 'yr_built' or 'bedrooms' or 'sqft_living' or 'sqft_lot' or 'waterfront' or 'view' or 'condition' or 'grade' or 'sqft_above' or 'sqft_basement' or 'yr_renovated' or 'sqft_living15' or 'sqft_lot15' or 'm2_lot' not in data:
            data['floors'] = data1['floors']
            data['id'] = data1['id']
            data['zipcode'] = data1['zipcode']
            data['price'] = data1['price']
            data['price_m2'] = data1['price_m2']
            data['lat'] = data1['lat']
            data['long'] = data1['long']
            data['date'] = pd.to_datetime(data1['date']).dt.strftime('%Y-%m-%d')
            data['bathrooms'] = data1['bathrooms']
            data['yr_renovated'] = data1['yr_renovated']
            data['yr_built'] = data1['yr_built']
            data['bedrooms'] = data1['bedrooms']
            data['sqft_living'] = data1['sqft_living']
            data['sqft_living15'] = data1['sqft_living15']
            data['sqft_lot'] = data1['sqft_lot']
            data['sqft_lot15'] = data1['sqft_lot15']
            data['waterfront'] = data1['waterfront']
            data['view'] = data1['view']
            data['condition'] = data1['condition']
            data['grade'] = data1['grade']
            data['sqft_above'] = data1['sqft_above']
            data['sqft_basement'] = data1['sqft_basement']
            data['m2_lot'] = data1['m2_lot']


        df1 = data[['id', 'zipcode']].groupby('zipcode').count().reset_index()
        df2 = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
        df3 = data[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
        df4 = data[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()

        # merge

        m1 = pd.merge(df1, df2, on='zipcode', how='inner')
        m2 = pd.merge(m1, df3, on='zipcode', how='inner')
        df = pd.merge(m2, df4, on='zipcode', how='inner')

        df.columns = ['zipcode', 'total houses', 'price', 'SQFT_living', 'PRICE/M2']

        c1.header('Média de valores do CEP')
        c1.dataframe(df, height=400)

        # Statistic Descriptive
        num_attributes = data.select_dtypes(include=['int64', 'float64'])
        media = pd.DataFrame(num_attributes.apply(np.mean))
        mediana = pd.DataFrame(num_attributes.apply(np.median))
        std = pd.DataFrame(num_attributes.apply(np.std))

        max_ = pd.DataFrame(num_attributes.apply(np.max))
        min_ = pd.DataFrame(num_attributes.apply(np.min))

        df1 = pd.concat([max_, min_, media, mediana, std], axis=1).reset_index()

        df1.columns = ['attributes', 'max', 'min', 'mean', 'median', 'std']

        c2.header('Análise Descritiva')
        c2.dataframe(df1, height=400)

    return None
# ========================
# Density Portfolio
# ========================

def portfolio_density(data, geofile):
    if options == 'Mapas regionais':
        st.title('Region Overview')
        st.subheader('Nessa secção você irá encontrar a distribução das casas e a densidade de preço por região.')
        c1, c2 = st.columns((1, 1))
        c1.header('Portfolio Density')

        df = data.sample(20000)

        # Base Map - Folium
        density_map = folium.Map(location=[data['lat'].mean(),
                                 data['long'].mean()],
                                 default_zoom_start=15)

        maker_cluster = MarkerCluster().add_to(density_map)
        for name, row in df.iterrows():
            folium.Marker([row['lat'], row['long']],
                popup='Sold R${0} on: {1}. Features: {2} sqft, {3} bedrooms, {4} bathrooms, year built: {5}'.format(row['price'],
                                                                                                                    row['date'],
                                                                                                                    row['sqft_living'],
                                                                                                                    row['bedrooms'],
                                                                                                                    row['bathrooms'],
                                                                                                                    row['yr_built'])).add_to(maker_cluster)
        with c1:
            folium_static(density_map)

        # Region Price Map
        c2.header('Price Density')

        df = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
        df.columns = ['ZIP', 'PRICE']

        df = df.sample(10)
        geofile = geofile[geofile['ZIP'].isin(df['ZIP'].tolist() )]

        region_price_map = folium.Map(location=[data['lat'].mean(),
                                      data['long'].mean()],
                                      default_zoom_start=15)

        region_price_map.choropleth(data = df,
                                    geo_data = geofile,
                                    columns = ['ZIP', 'PRICE'],
                                    key_on = 'feature.properties.ZIP',
                                    fill_color='YlOrRd',
                                    fill_opacity = 0.7,
                                    line_opacity = 0.2,
                                    legend_name='AVG PRICE')

        with c2:
            folium_static(region_price_map)
    return None
# ===================================================
# Distribuição dos imóveis por categorias comerciais
# ===================================================

def commercial_distribution(data):
    if options == 'Atributos Comerciais':

        st.sidebar.title('Commercial Options')
        st.title('Commercial Attributes')

        #======= Average price per Year

        # filters
        min_year_built = int(data['yr_built'].min())
        max_year_built = int(data['yr_built'].max())

        st.sidebar.subheader('Select Max Year Built')
        f_year_built = st.sidebar.slider('Year Built', min_year_built,
                                                       max_year_built,
                                                       min_year_built)


        st.header('Average Price per Year')
        df = data.loc[data['yr_built'] < f_year_built]
        df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

        fig = px.line(df, x='yr_built', y='price')
        st.plotly_chart(fig, use_container_width=True)

        #======= Average price per day
        st.header('Average Price per Day')
        st.sidebar.subheader('Select Max Date')
        #filters
        min_date = datetime.strptime(data['date'].min(), '%Y-%m-%d')
        max_date = datetime.strptime(data['date'].max(), '%Y-%m-%d')

        f_date = st.sidebar.slider('Date', min_date, max_date, min_date)

        # data selection
        data['date'] = pd.to_datetime(data['date'])
        df = data.loc[data['date'] < f_date]
        df = df[['date', 'price']].groupby('date').mean().reset_index()

        # plot
        fig = px.line(df, x='date', y='price')
        st.plotly_chart(fig, use_container_width=True)

        # -------------- Histogram
        st.header('Price Distribution')
        st.sidebar.subheader('Select Max Price')

        #filter
        min_price = int(data['price'].min())
        max_price = int(data['price'].max())
        avg_price = int(data['price'].mean())

        # data filtering
        f_price = st.sidebar.slider('Price', min_price, max_price, avg_price)
        df = data.loc[data['price'] < f_price]

        # data plot
        fig = px.histogram(df, x='price', nbins=50)
        st.plotly_chart(fig, use_container_width=True)

        #========================
        # Distribuilção dos imóveis por categorias físicas
        #========================

        st.sidebar.title('Attributes Options')
        st.title('House Attributes')

        #filters
        f_bedrooms = st.sidebar.selectbox('Max number of bedrooms',
                                           sorted(set(data['bedrooms'].unique())))
        f_bathrooms = st.sidebar.selectbox('Max number of bathrooms',
                                            sorted(set(data['bathrooms'].unique())))

        c1, c2 = st.columns(2)

        # House per bedrooms
        c1.header('House per bedrooms')
        df = data[data['bedrooms']<f_bedrooms]
        fig = px.histogram(data, x='bedrooms', nbins=19)
        c1.plotly_chart(fig, use_container_width=True)

        # House per bathrooms
        c2.header('House per bathrooms')
        df = data[data['bathrooms']<f_bathrooms]
        fig = px.histogram(data, x='bathrooms', nbins=19)
        c2.plotly_chart(fig, use_container_width=True)

        #filters

        f_floors = st.sidebar.selectbox('Max number of floors',
                                         sorted(set(data['floors'].unique())))
        f_waterview = st.sidebar.checkbox('Only Houses with water View')

        c1, c2 = st.columns(2)
        # House per floors
        c1.header('House per floors')
        df = data[data['floors'] < f_floors]
        # plot
        fig = px.histogram(df, x='floors', nbins=19)
        st.plotly_chart(fig, use_container_width=True)

        # Waterview
        st.header('Houses with Waterview')
        if f_waterview:
            data = data[data['waterfront'] == 1]
        else:
            df = data.copy()
        fig = px.histogram(df, x='waterfront', nbins=10)
        st.plotly_chart(fig, use_container_width=True)

    return None

def hipoteses(data):
    if options == 'Hipóteses':

        st.title('Hipoteses para o negócio')
        st.write('Com a analise das hipoteses, ')
        c1, c2 = st.columns(2)
        hipotese_1 = data[['price', 'waterfrontview']].groupby('waterfrontview').mean().reset_index()
        hipotese_1['percent'] = hipotese_1['price'].pct_change()
        h1_mean = hipotese_1['percent'].mean()

        c1.subheader('Hipótese 1:  Imóveis com vista para a água são em média 30% mais caros')
        c1.write(f'- Hipotese falsa, a média de preço {h1_mean:.2%} para imóveis com vista para água.')

        fig1 = px.bar(hipotese_1, x='waterfrontview', y = 'price', color = 'waterfrontview',  labels={"waterfrontview": "Vista para  água",
                                                                                              "price": "Preço"},
                                                                                               template= 'simple_white')

        #fig1.update_layout(showlegend=False)
        c1.plotly_chart(fig1, use_container_width=True)

        hipotese_2 = data[['price', 'yr_built_1955']].groupby('yr_built_1955').mean().reset_index().sort_values(by='yr_built_1955', ascending=False)
        hipotese_2['percent'] = hipotese_2['price'].pct_change()
        media_hipo_2 = hipotese_2['percent'].mean()

        c2.subheader('Hipotese 2: Imóveis com data de construção menor do que 1955, são 50% mais baratos na média.')
        c2.write(f'- Hipotese falsa, a média de preço como observado é de {media_hipo_2:.2%}.\n'
                 '')


        fig2 = px.bar(hipotese_2, x='yr_built_1955', y='price', color='yr_built_1955', labels={"yr_built_1955": "Périodo de Construção",
                                                                                              "price": "Preço"},
                                                                                              template='simple_white')
        fig2.update_layout(showlegend=False)
        c2.plotly_chart(fig2, use_container_width=True)

        c3, c4 = st.columns(2)


        hipotese_3 = data[['not_basement', 'm2_lot']].groupby('not_basement').sum().reset_index()

        hipotese_3['percent'] = hipotese_3['m2_lot'].pct_change()
        media_hipo_3 = hipotese_3['percent'].mean()
        media_hipo_3_true = media_hipo_3 * (1)
        c3.subheader('Hipotese 3: Imóveis sem porão são 50% maiores do que com porão.')
        c3.write(f'A hipotese é verdadeira, o valor é de {media_hipo_3_true:.2%}, o interesse ter porão vai variar com a.')

        fig3 = px.bar(hipotese_3, x='not_basement', y='m2_lot', color='not_basement', labels={'not_basement': 'Basement',
                                                                                               'm2_lot': 'Lot for m²'},
                                                                                               template='simple_white')

        fig3.update_layout(showlegend=False)
        c3.plotly_chart(fig3, use_container_width=True)

        hipo_04 = data.copy()
        hipo_04['date'] = pd.to_datetime(hipo_04['date']).dt.year
        hipo_04['cres_ano'] = hipo_04['date'].apply(lambda date: '2015' if (date == 2015) else '2014')
        hipotese_4 = hipo_04[['price', 'cres_ano']].groupby('cres_ano').mean().reset_index()
        hipotese_4['percent'] = hipotese_4['price'].pct_change()
        c4.subheader('Hipotese 4: O crescimento do preço dos imóveis YoY ( Year overYear ) é de 10%')
        c4.write(f'O ideial seria ter mais anos para realizar a analíse, em 2014 e 2015 o crescimento foi de {hipotese_4.iloc[1, 2]:.2%}')

        fig4 = px.bar(hipotese_4, x='cres_ano', y='price', color='cres_ano', labels={'price': 'Preço',
                                                                              'cres_ano': 'Ano'},
                                                                              template='simple_white')

        fig4.update_layout(showlegend=False)
        c4.plotly_chart(fig4, use_container_width=True)

        c5, c6 = st.columns(2)


        hipotese_5 = data[['price', 'mes']].loc[data['bathrooms'] == 3].groupby('mes').mean().reset_index().sort_values(by='mes', ascending=False)
        hipotese_5['percent'] = hipotese_5['price'].pct_change()
        mom_mean = hipotese_5['percent'].mean() * (-1)

        c5.subheader('Hipotse 5: Imóveis com 3 banheiros tem um crescimento de MoM de 15%')
        c5.write(f'Falsa a media é {mom_mean:.2%}')

        fig5 = px.bar(hipotese_5, x='mes', y='price', color='price', labels={'price': 'Preço',
                                                                              'mes': 'Mês'},
                                                                              template='simple_white')

        fig5.update_layout(showlegend=True)
        c5.plotly_chart(fig5, use_container_width=True)

        hipotese_6 = data[['estacao_venda', 'price']].groupby('estacao_venda').mean().reset_index()
        c6.subheader('Hipotese_6: Em média, os preços de venda ficam mais caros no verão')
        c6.write(f'A Hipotese é falsa, os preços ficam mais caros na primavera, com uma mediana de US${hipotese_6.iloc[3, 1]:.2f}')

        fig6 = px.bar(hipotese_6, x='estacao_venda', y='price', color='price', labels={'estacao_venda: Estacão do ano,'
                                                                                       'price': 'Mediana Preço'},
                                                                                        template='simple_white')

        fig6.update_layout(showlegend=True)
        c6.plotly_chart(fig6, use_container_width=True)

        c7, c8 = st.columns(2)

        c7.subheader('Hipotese_7: Ter mais quartos não necessariamente fará o imóvel ser mais caro')
        c7.write(f'A hipotese é verdadeira, casas com mais quartos não são as mais caras.')

        hipotese_7 = data[['bedrooms', 'price']].loc[data['bedrooms'] != 33].groupby('bedrooms').median().reset_index()
        fig7 = px.bar(hipotese_7, x='bedrooms', y='price', color='price', labels={'bedrooms': 'Quartos',
                                                                                  'price': 'Preço'},
                                                                                  template='simple_white')

        fig7.update_layout(showlegend=True)
        c7.plotly_chart(fig7, use_container_width=True)

        c8.subheader('Hipotese_8: A condição mais em conta para comprar os imóveis é a condição mais alta?')
        c8.write('Falsa, como pode ser se ver no gráfico a condição 4, contem os melhores preços.')

        hipotese_8 = data[['condition', 'price']].groupby('condition').median().reset_index()
        fig8 = px.bar(hipotese_8, x='condition', y='price', color='price', labels={'condition':'Condicão',
                                                                                   'price': 'Preço'},
                                                                                   template='simple_white')
        fig8.update_layout(showlegend=True)
        c8.plotly_chart(fig8, use_container_width=True)
    return None

def relat_final(data):

    if options == 'Relatório Final':
        st.title ('Relatório e Recomendação Final')

        st.subheader('Top Insights')
        st.write('* Casas com vista para a água sã 212% mais caras, logo encontrar uma casa com um valor baixo, faz com que possamos vende-la no preço máximo')
        st.write('* Procurar casas com condição 4, em mediana, elas possuem preços mais baratos que as casas de condição 3.')
        st.write('* O melhor periódo de compra é nos 3 meses de inverno, onde as casas ficam mais baratas.')
        st.write('* Comprar casa no inverno e vender na primavera, gera um lucro maior, e também a empresa não precisa segurar muito tempo um imóvel, visto que são estações uma ao lado da outra.')

        price_median = data[['price', 'zipcode']].groupby('zipcode').median().reset_index()
        df2 = pd.merge(data, price_median, on='zipcode', how='inner')
        df2['status'] = 'NA'

        for i in range(len(df2)):
            if ((df2.loc[i, 'price_x'] < df2.loc[i, 'price_y']) & (df2.loc[i, 'condition'] >= 3) & (df2.loc[i, 'bedrooms'] >= 1) & df2.loc[i, 'waterfront'] == 1):
                df2.loc[i, 'status'] = 'Compra'
            else:
                df2.loc[i, 'status'] = 'Não Compra'

        recomendacao = df2[df2['status'] == 'Compra']
        st.subheader('Recomendações de casas com condição de 3-5 e com vista para a água')
        st.dataframe(recomendacao)

        df3 = df2.copy()

        for i in range(len(df3)):
            if ((df3.loc[i, 'price_x'] < df3.loc[i, 'price_y']) & (df3.loc[i, 'condition'] ==4) & (df3.loc[i, 'bedrooms'] >= 1) & df3.loc[i, 'waterfront'] == 1):
                df3.loc[i, 'status'] = 'Compra'
            else:
                df3.loc[i, 'status'] = 'Não Compra'

        recomendacao_1 = df3[df3['status'] == 'Compra']
        st.subheader('Recomendações de casas com condição de 4 e com vista para a água' )
        st.write('Alta prioridade de compra, visto que temos as melhores condições do mercado')
        st.dataframe(recomendacao_1)

        investimento = recomendacao['price_x'].sum()
        #lucro10 = (recomendacao['price_x'].sum() * 1.1) - (recomendacao['price_x'].sum())
        lucro30 = (recomendacao['price_x'].sum() * 1.3) - (recomendacao['price_x'].sum())

        #print(f'US$ {lucro10:.2f}\n')
        st.subheader('Investimento necessário e lucro')
        st.write(f'O investimento necessário para comprar esses imóveis é de {investimento}')
        st.write(f'Tomando como base, todas as casas sendo vendidas com 30% a mais no valor de compra, o lucro será de US$ {lucro30:.2f}')

    return None


if __name__ == '__main__':
    # ETL
    # data extration
    path = 'kc_house_data.csv'

    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'


    data = get_data(path)
    geofile = get_geofile(url)

    # transformation
    data = set_feature(data)

    overview_data(data)

    portfolio_density(data, geofile)

    commercial_distribution(data)

    hipoteses(data)

    relat_final(data)