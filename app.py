import numpy as np
import pandas as pd
import streamlit as st

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from iso3166 import countries
# from statsmodels.tsa.arima.model import ARIMA
# from statsmodels.tsa.seasonal import seasonal_decompose

import matplotlib
import matplotlib.pyplot as plt
from PIL import Image

from datetime import datetime, timedelta
from collections import OrderedDict


df = pd.read_csv('dataset/Space_Corrected.csv')
df.columns = [
    'Unnamed: 0', 
    'Unnamed: 0.1', 
    'Company Name', 
    'Location', 
    'Datum', 
    'Detail', 
    'Status Rocket', 
    'Rocket', 
    'Status Mission'
]
df = df.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1)

df['Rocket'] = df['Rocket'].fillna(0.0).str.replace(',', '')
df['Rocket'] = df['Rocket'].astype(np.float64).fillna(0.0)
df['Rocket'] = df['Rocket'] * 1000000
df['date'] = pd.to_datetime(df['Datum'], infer_datetime_format=True)
df['year'] = df['date'].apply(lambda datetime: datetime.year)
df['month'] = df['date'].apply(lambda datetime: datetime.month)
df['weekday'] = df['date'].apply(lambda datetime: datetime.weekday())

countries_dict = {
            'Russia' : 'Russian Federation',
            'New Mexico' : 'USA',
            "Yellow Sea": 'China',
            "Shahrud Missile Test Site": "Iran",
            "Pacific Missile Range Facility": 'USA',
            "Barents Sea": 'Russian Federation',
            "Gran Canaria": 'USA'
        }
df['country'] = df['Location'].str.split(', ').str[-1].replace(countries_dict)

country_dict = dict()
for c in countries:
    country_dict[c.name] = c.alpha3
df['alpha3'] = df['country']
df = df.replace(
    {
        "alpha3": country_dict
    }
)
df.loc[df['country'] == "North Korea", 'alpha3'] = "PRK"
df.loc[df['country'] == "South Korea", 'alpha3'] = "KOR"


# Top navbar
st.set_page_config(page_title="Space Missions Analysis", page_icon=":🚀:", layout="wide")
    
with st.sidebar:
    st.title('🚀 Space Missions Analysis')
    pages = ['Home', 
             'About Data', 
             'Dataset Overview',  
             'Interesting Factors', 
             'The Cold war',
             'Best Every Year',
             'Geo Analysis',
             'India`s Place',
             'Reference'
             ]
    page = st.radio('Navigation', pages)

# Define icons for radio buttons
# home_icon = "🏠"
# data_icon = "📊"
# overview_icon = "🌐"
# factors_icon = "🤔"
# war_icon = "🧊"
# best_icon = "🏆"
# geo_icon = "🗺️"
# india_icon = "🇮🇳"

# Create main panel
main_panel = st.container()
with main_panel:
    # st.title(page)
    #####################################################################################
    ######                                                                         ######
    #####################################################################################
    if page == 'Home':
        st.title("🏠" + page)
        st.header(' **Data Analytics and Visualization Project** ')
        st.write('')
        st.write('')
        st.write('')
        
        image = Image.open("space_rocket.png")
        st.image(image)
    
    #####################################################################################
    ######                                                                         ######
    #####################################################################################
    elif page == 'About Data':
        st.title("📊" + page)
        st.markdown(''' _The Space Missions Analysis dataset contains information on space missions launched by various countries around the world from 1957 to present. The data includes details such as the launch date, country of origin, rocket used, mission status, and more. The dataset provides valuable insights into the history and trends of space exploration, and can be used to analyze the involvement of different countries in space missions, the success rates of missions, and the evolution of rocket technology over time. Through data visualization, this dataset can help to provide a deeper understanding of the past, present, and future of space exploration._ ''')
        st.write('## Data Frame')
        st.dataframe(df)
        st.markdown("""
            ### Data Wrangling
            Cleaning and wrangling the data involves several steps, including:

            - Any duplicate or irrelevant data was removed to ensure that the dataset is accurate and relevant for analysis. In addition, any rows or columns that had null values in the rocket name column were removed since this information is important for analyzing the rocket technology used in each mission. 

            - We have converted the date and time format in the data to a more suitable format that can be effectively analyzed and visualized. This conversion was carried out using the appropriate Python libraries and functions that ensure a professional and accurate handling of the data.

            - In the data wrangling process, the date column was parsed to extract additional information such as month, year, and weekday. This was done to facilitate the visualization of the data by grouping it into different time periods and identifying trends and patterns. 

            - We performed a scaling operation on the price data by multiplying the original values, which ranged from 0 to 1, by a factor of 1,000,000. This was done to convert the values into millions, enabling better comparability and analysis of the data.

        """)

        
    #####################################################################################
    ######                                                                         ######
    #####################################################################################
    elif page == 'Dataset Overview':
        st.title("🌐" + page)
        st.write(' _The higher number of rocket launches by certain countries can be attributed to a combination of historical context, technological advancements, and military applications._')
        ds = df['Company Name'].value_counts().reset_index()
        ds.columns = ['Company', 'Number of Launches']
        ds = ds.sort_values(['Number of Launches'], ascending=False)
        fig = px.treemap(ds, 
                        path=['Company'], 
                        values='Number of Launches', 
                        color='Number of Launches',
                        color_continuous_scale='YlOrRd',
                        title='Number of Launches by Every Company',
                        hover_data={'Number of Launches': ':d', 'Company': False},
                        custom_data=['Number of Launches'])
        fig.update_traces(
            hovertemplate='<br>'.join([
                'Company: %{label}',
                'Number of Launches: %{customdata[0]}'
            ]),
            hoverlabel=dict(
            bgcolor="yellow",
            font=dict(size=12, color = "black")
            ),
            marker=dict(cornerradius=15)
        )
        fig.update_layout(height = 400,
                          margin = dict(t=50, l=25, r=25, b=2))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('''
        ##### Insights

        - _**Historical Context**_: _The USSR and the USA were in a space race during the Cold War, which fueled significant investment in space exploration and a high number of rocket launches. Since then, these two countries have continued to maintain a strong presence in space exploration._

        - _**Technological Advancements**_: _NASA, Boeing, and SpaceX are all major players in the commercial space industry and have developed advanced rocket technology. This has allowed them to launch a larger number of rockets and achieve higher success rates than other countries._

        - _**Military Applications**_: _The US Air Force has been involved in launching rockets for military applications, such as spy satellites and communication networks, which require a high number of launches._

        ''')

        #--------------------------------------------------------------------------------------------------
        ds = df['Status Rocket'].value_counts().reset_index()
        ds.columns = ['status', 'count']
        ds = ds.sort_values('count', ascending=False)

        colors = ['rgb(75, 109, 153)', 'rgb(232, 114, 114)']

        fig = go.Figure(
            go.Pie(
                labels=ds['status'], 
                values=ds['count'],
                hole=0.5,
                marker=dict(colors=colors), 
                textfont=dict(size=14, color='black'),
                hoverinfo='label+percent',
                textinfo='label+percent'
            )
        )
        fig.update_layout(
            title=dict(
                text='Rocket Status',
                font=dict(size=20)
            ),
            font=dict(
                family='Arial',
                size=16,
                color='black'
            ),
            height=470
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(''' 
        ##### Insights
        - _The fact that around 80% of rockets are not currently in use highlights the fact that historically rockets were designed as expendable vehicles, meaning they were only intended to be used once and then discarded. This resulted in a significant amount of waste and high launch costs, as a new rocket had to be built for each launch._
        ''')
        
        #---------------------------------------------------------------------------------------------
        ds = df['Status Mission'].value_counts().reset_index()
        ds.columns = ['mission_status', 'count']
        ds = ds.sort_values('count', ascending=False)

        colors = ['#FFC300', '#FF5733', '#C70039', '#900C3F', '#581845']
        fig = px.bar(ds, 
                    x='mission_status', 
                    y='count', 
                    title='Mission Status Distribution',
                    color='mission_status',
                    color_discrete_sequence=colors,
                    height=500, 
                    width=800
                    )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            xaxis=dict(
                title='',
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=0.1,
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title='Count',
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=0.1,
                tickfont=dict(size=12),
                automargin=True
            ),
            font=dict(
                family='Arial',
                size=14,
                color='black'
            ),
            margin=dict(l=0, r=0, t=50, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''
        ##### Insights
         - _The high success rates of missions were likely due to a combination of technological advancements, rigorous testing and quality control procedures, experience and expertise, and strategic importance._

        ''')
        
        
    #####################################################################################
    ######                                                                         ######
    #####################################################################################
    elif page == 'Geo Analysis':
        st.title("🗺️" + page)
        st.write('_The sunburst chart visualizes the number of rockets launched by different companies in various countries, along with the mission status of each launch. The chart is divided into three concentric circles, with the innermost circle representing countries, the middle circle representing companies within each country, and the outer circle representing the mission status of each launch._')
        sun = df.groupby(['country', 'Company Name', 'Status Mission'])['Datum'].count().reset_index()
        sun.columns = [
            'country', 
            'company', 
            'status', 
            'count'
        ]
        fig = px.sunburst(
            sun, 
            path=[
                'country', 
                'company', 
                'status'
            ], 
            values='count', 
            title='Sunburst chart for all countries',
            width=800,
            height=500 
        )
        fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(''' 
        ##### Insights
          - _The disparity in the number of launches by the USSR and the US compared to other countries can be attributed to a combination of early development, budgetary constraints, technology transfer, and international cooperation. However, in recent years, other countries like China, India, and Japan have been investing heavily in their space programs and are catching up in terms of the number of launches and achievements in space exploration._
        ''')
        
        
        #--------------------------------------------------------------------------------------------     
        def plot_map(dataframe, target_column, title, width=800, height=600, color_scale='Viridis'):
            mapdf = dataframe.groupby(['country', 'alpha3'])[target_column].count().reset_index()
            fig = px.choropleth(
                mapdf, 
                locations="alpha3", 
                hover_name="country", 
                color=target_column, 
                projection="natural earth", 
                width=width, 
                height=height,
                color_continuous_scale=color_scale,
                range_color=[0, mapdf[target_column].max()],
                title=title,
                template='plotly_dark'
            )
            fig.update_geos(
                showcountries=True,
                countrycolor="white",
                showocean=True,
                oceancolor="MidnightBlue",
                showcoastlines=True,
                coastlinecolor="white",
                showland=True,
                landcolor="LightGrey"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        plot_map(
            dataframe=df, 
            target_column='Status Mission', 
            title='Number of launches per country',
            color_scale='YlOrRd'
        )
        st.markdown(''' 
        ##### Insights
        - _A world heat map that shows the number of space missions by country can provide valuable insights into the distribution of space exploration activity around the world.In this case, the map shows that the USSR and the US have had significantly more space missions than other countries.However, the map also shows that other countries like China, India, and Japan are becoming increasingly active in space exploration and are catching up to the US and the USSR in terms of the number of missions._
        ''')

        fail_df = df[df['Status Mission'] == 'Failure']
        plot_map(
            dataframe=fail_df, 
            target_column='Status Mission', 
            title='Number of Fails per country',
            color_scale='YlOrRd'
        )  
        st.markdown(''' 
        ##### Insights
        _The higher success rate of the USSR's space program may have been due to a combination of factors, including factors such as_

        - _The Soviet Union's space program was often characterized by a focus on simplicity and reliability._

        - _The Soviet Union was known for placing a high priority on the safety of its cosmonauts and spacecraft._

        - _The Soviet Union invested heavily in its launch infrastructure, building a network of launch facilities and associated infrastructure that could support a wide range of missions._

        ''')
        
    #####################################################################################
    ######                                                                         ######
    #####################################################################################
    elif page == 'Interesting Factors':
        st.title("🤔" + page)
        data = df.groupby(['Company Name'])['Rocket'].sum().reset_index()
        data = data[data['Rocket'] > 0]
        data.columns = [
            'company', 
            'money'
        ]
        fig = px.bar(
            data, 
            x='company', 
            y="money", 
            orientation='v', 
            title='Total money spent on missions', 
            width=800,
            height=500,
            color='money',
            color_continuous_scale=px.colors.sequential.YlOrRd,
            color_continuous_midpoint=data['money'].median()
        )
        fig.update_yaxes(title='', showticklabels=False)
        st.plotly_chart(fig, use_container_width=True)

        
        
        # #----------------------------------------------------------------------------------------
        money = df.groupby(['Company Name'])['Rocket'].sum()
        starts = df['Company Name'].value_counts().reset_index()

        starts.columns = [    'Company Name',     'count']

        av_money_df = pd.merge(money, starts, on='Company Name')
        av_money_df['avg'] = av_money_df['Rocket'] / av_money_df['count']
        av_money_df = av_money_df[av_money_df['avg']>0]
        av_money_df = av_money_df.reset_index()

        fig = px.bar(
            av_money_df, 
            x='Company Name', 
            y="avg", 
            orientation='v', 
            title='Average money per one launch', 
            width=800,
            height=500,
            color='avg',
            color_continuous_scale=px.colors.sequential.YlOrRd,
            color_continuous_midpoint=av_money_df['avg'].median()
        )

        fig.update_yaxes(title='', showticklabels=False)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(''' 
        ##### Insights
        
        - _The significant difference in funding between NASA and private companies reflects the different priorities and goals of each entity. NASA's focus on scientific research and pushing the boundaries of space exploration requires significant investment, which is made possible through government funding. Private companies, on the other hand, may focus more on commercial applications of space technology and therefore may not require as much funding._
        ''')
        
        #-----------------------------------------------------------------------------------------
        ds = df['year'].value_counts().reset_index()
        ds.columns = ['year', 'count']
        colors = ['#3c7ebf'] * len(ds)
        colors[0] = '#00bfff'
        bar = go.Bar(
            x=ds['year'],
            y=ds['count'],
            marker=dict(
                color=colors,
                line=dict(
                    color='#000000',
                    width=1
                )
            )
        )
        layout = go.Layout(
            title='Missions number by year',
            xaxis=dict(
                title='year',
                tickmode='linear',
                tick0=min(ds['year']),
                dtick=1
            ),
            yaxis=dict(
                title='Number of Missions',
                showgrid=True,
                gridwidth=0.5,
                gridcolor='#c0c0c0',
                tickmode='linear',
                tick0=0,
                dtick=100
            ),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        fig = go.Figure(data=[bar], layout=layout)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('''
        ##### Insights
        
        - _During the period between 1966 and 1978, there was a significant increase in the number of launches primarily driven by the space race between the United States and the Soviet Union. This was a period of intense competition between the two nations, and both were investing heavily in space exploration and technology development._

        - _In recent years, there has been renewed interest in space exploration and commercial space ventures. Private companies such as SpaceX have entered the market and are driving innovation and competition in the industry._
        ''')
        
        #-----------------------------------------------------------------------------------------
        ds = df['month'].value_counts().reset_index()
        ds.columns = [
            'month', 
            'count'
        ]
        fig = px.bar(
            ds, 
            x='month',
            y="count", 
            orientation='v', 
            title='Missions number by month', 
            width=800
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''
        ##### Insights
        ''')
        st.write('- _There is no clear pattern in terms of which days and month have more or fewer launches. Lack of dependence on the month and weekdays may be due to the fact that space agencies and companies have a relatively consistent schedule of launches throughout the year which includes careful planning, preparation, and monitoring to ensure a safe and successful launch._')
        
        #---------------------------------------------------------------------------------------
        res = list()
        for group in df.groupby(['Company Name']):
            res.append(group[1][['Company Name', 'year']].head(1))
        data = pd.concat(res)
        data = data.sort_values('year')
        data['year'] = 2020 - data['year']
        fig = go.Figure(go.Bar(
            x=data['year'],
            y=data['Company Name'],
            orientation='h',
            marker=dict(
                color=data['year'],
                coloraxis='coloraxis'
            ),
            text=data['year'],
            textposition='inside',
            hovertemplate='<b>%{y}</b><br>' +
                'Years since last start: %{x}<br>' +
                '<extra></extra>',
        ))
        fig.update_layout(
            title='Years since last Rocket launch from 2020',
            title_x=0.5,
            font=dict(size=12),
            width=900,
            height=1000,
            xaxis=dict(title='Years'),
            yaxis=dict(title='Company Name'),
            coloraxis=dict(
                colorscale='RdYlGn',
                colorbar=dict(
                    title='Years since last start',
                    titleside='right',
                    ticks='outside',
                    ticklen=5,
                    showticklabels=True
                )
            ),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''
        ##### Insights
        ''')
        st.write("- _Based on the graph, it appears that some of the older companies such as the US Navy and US Air Force have not launched rockets in several decades. Meanwhile, newer countries have emerged and are launching rockets more frequently. This suggests that the landscape of space exploration has shifted over time, with new players entering the field and taking on more active roles._")

        #--------------------------------------------------------------------------------------
        money = df[df['Rocket']>0]
        money = money.groupby(['year'])['Rocket'].mean().reset_index()
        fig = px.line(
            money, 
            x="year", 
            y="Rocket",
            title='Average money spent by year',
            width=800
        )
        fig.update_layout(
            yaxis_title='Money'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''
        ##### Insights
        ''')
        st.write("- _The average money spent on space exploration was higher between 1980 and 1990 could be the emergence of more nations beyond the US and the USSR entering the field of space exploration. As more countries developed their space programs, there was increased competition and a desire to keep up with the latest advancements in technology. This may have led to more spending on research and development in space exploration, and increased funding for space agencies in these countries._")
        
        #--------------------------------------------------------------------------------------
        ds = df.groupby(['Company Name'])['year'].nunique().reset_index()
        ds.columns = ['company','count']
        ds = ds.sort_values(by='count', ascending=False)
        fig = px.bar(
            ds, 
            x="company", 
            y="count", 
            title='Most experienced companies (years of launches)',
            height = 500,
            color_discrete_sequence=['#1f77b4']
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''
        ##### Insights
        - _Experience and expertise: Companies with a long history in space exploration, such as NASA, the USSR, General Dynamics and the US Air Force, have accumulated a wealth of experience and knowledge over the years, which can give them an advantage over newer players._

        - _Strategic partnerships: Arianespace has formed partnerships with several European countries to develop the Ariane rocket family, which has helped to establish it as a major player in the industry._

        - _Innovative technology: Companies that are able to develop innovative and cutting-edge technology can gain a competitive advantage in space exploration. SpaceX, for example, has made significant strides in reusable rocket technology, which has helped to reduce launch costs and increase efficiency._

        - _China faced initial setbacks in its early attempts to launch satellites into space during the 18th century, but it persisted with its efforts and continued to make progress. As a result, China has accumulated more years of experience in space exploration despite its initial failures._
 

        ''')
        
        #--------------------------------------------------------------------------------------
        data = df.groupby(['Company Name', 'year'])['Status Mission'].count().reset_index()
        data.columns = [
            'company', 
            'year', 
            'starts'
        ]
        top5 = data.groupby(['company'])['starts'].sum().reset_index().sort_values('starts', ascending=False).head(5)['company'].tolist()
        data = data[data['company'].isin(top5)]
        fig = px.line(
            data, 
            x="year", 
            y="starts", 
            title='Top 5 companies by number of launches', 
            color='company'
        )
        fig.update_layout(
            yaxis_title='Launches'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''
        ##### Insights

        - _The USSR had a significant advantage in rocket technology, with early successes in developing powerful rocket engines and launch vehicles. This combination of government support, early achievements, and technical expertise helped the USSR establish dominance in space exploration during the 1960s to 1990s._

        - _CASC, or the China Aerospace Science and Technology Corporation, was established in 1999 to consolidate China's aerospace industry. In the past, China faced challenges in developing its space technology due to limited resources and access to advanced technology. However, in recent years, the Chinese government has significantly increased its investment in space exploration, leading to rapid development and progress in China's space technology._

        - _One of the primary factors in decline of General Dynamics was the decline in funding for space exploration by the US government. During the 1960s and 1970s, the US government invested heavily in space exploration as part of the Cold War space race against the Soviet Union. However, with the end of the Cold War and a shift in government priorities, funding for space exploration declined significantly._

        - _In 2011 NASA transitioned to relying on commercial space companies like SpaceX and Boeing to transport astronauts to the International Space Station (ISS), rather than developing its own spacecraft. This shift was aimed at reducing the costs and risks of human spaceflight, and allowing NASA to focus on more ambitious goals like returning humans to the Moon and eventually sending humans to Mars._

        - _Compared to other space agencies like NASA and Roscosmos, Arianespace has not been as active in manned missions and deep space exploration. This is partly due to the fact that Arianespace is a commercial launch provider, and its focus is primarily on launching satellites for customers rather than conducting its own space exploration missions._


        ''')

        #----------------------------------------------------------------------------------------
        data = df.groupby(['Company Name', 'year'])['Status Mission'].count().reset_index()
        data.columns = [
            'company', 
            'year', 
            'starts'
        ]
        data = data[data['year']==2020]
        fig = px.bar(
            data, 
            x="company", 
            y="starts", 
            title='Number of starts for 2020', 
            width=800
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''
        ##### Insights
         - _Private companies like SpaceX have emerged as major players in the space industry in recent years, and they may have taken on more of the rocket launches that were previously done by government agencies._

        - _China has made significant investments in its space program, with a budget of over $8 billion in 2021. This has allowed them to develop advanced space technologies, including the Long March rockets, which have a high success rate and can carry heavy payloads._
        ''')
        
    #####################################################################################
    ######                                                                         ######
    #####################################################################################
    elif page == 'The Cold war':
        st.title("❄️" + page)
        st.write(' _During the Cold War, the United States and the Soviet Union were engaged in intense competition across a wide range of areas, including space exploration. The Cold War between the United States and the Soviet Union had a significant impact on space exploration, driving a rapid advancement in space technology and an increase in space-related investments. Both countries saw space exploration as a way to demonstrate their technological and military superiority and to gain an advantage over the other._')
        st.write('_Overall, the Cold War period saw a significant increase in the number of rockets launched and successful space missions by both the United States and the Soviet Union._ ')
        cold = df[df['year'] <= 1991]
        cold['country'].unique()
        cold.loc[cold['country'] == 'Kazakhstan', 'country'] = 'USSR'
        cold.loc[cold['country'] == 'Russian Federation', 'country'] = 'USSR'
        cold = cold[(cold['country'] == 'USSR') | (cold['country'] == 'USA')]
        
        ds = cold['country'].value_counts().reset_index()
        ds.columns = ['country', 'count']
        colors = px.colors.qualitative.Dark24
        title_font = dict(size=20, family='Arial')
        fig = px.pie(ds, 
                    names='country', 
                    values='count', 
                    title='Number of Launches by Country',
                    hole=0.5, # Change hole size
                    color_discrete_sequence=colors, # Assign custom colors
                    labels={'country': 'Country', 'count': 'Number of Launches'}, # Rename labels
                    width=700, 
                    height=450)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(title_font=title_font)
        st.plotly_chart(fig, use_container_width=True)
        st.write('- _The Cold War period saw a total of 2,332 successful space missions by both the United States and the Soviet Union. These missions included those related to satellite launches, human spaceflight, and planetary exploration._')
        
        #----------------------------------------------------------------------------------------
        ds = cold.groupby(['year', 'country'])['alpha3'].count().reset_index()
        ds.columns = ['Year', 'Country', 'Launches']
        colors = ['rgb(53, 83, 255)', 'rgb(255, 128, 0)']
        fig = px.line(
            ds, 
            x="Year", 
            y="Launches", 
            color='Country', 
            title='USA vs USSR: Launches Year by Year',
            color_discrete_sequence=colors, # Set custom color palette
            labels={'Year': 'Year', 'Launches': 'Number of Launches', 'Country': 'Country'}, # Rename labels
            height=500, 
            width=800
        )
        fig.update_xaxes(tickangle=45, tickfont=dict(size=10))
        fig.update_layout(
            legend=dict(
                title=None,
                orientation='h',
                yanchor='top',
                y=1.1,
                xanchor='left',
                x=0.15,
                font=dict(size=12)
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''
        ##### Insights

        - _Between 1957 and 1991, the Soviet Union launched a total of 1770 rockets, including those for military and civilian purposes.The Soviet Union also had several successful missions to the Moon and developed a number of key space technologies, such as space stations and interplanetary probes._

        - _Between 1958 and 2011, the United States launched a total of 1,736 rockets, including those for military and civilian purposes. The United States achieved several major milestones during the Cold War period, such as the successful landing of astronauts on the Moon and the development of the Space Shuttle program._
        ''')

        #------------------------------------------------------------------------------------------
        ds = cold.groupby(['year', 'country'])['Company Name'].nunique().reset_index()
        ds.columns = ['Year', 'Country', 'Companies']
        colors = ['rgb(53, 83, 255)', 'rgb(255, 128, 0)']
        fig = px.bar(ds, 
                    x='Year', 
                    y='Companies', 
                    color='Country',
                    color_discrete_sequence=colors,
                    title='USA vs USSR: Number of Companies Year by Year',
                    labels={'Year': 'Year', 'Companies': 'Number of Companies', 'Country': 'Country'},
                    height=500, 
                    width=800)
        fig.update_xaxes(tickangle=45, tickfont=dict(size=10))
        fig.update_layout(
            legend=dict(
                title=None,
                orientation='h',
                yanchor='top',
                y=1.1,
                xanchor='left',
                x=0.15,
                font=dict(size=12)
            ),
            font=dict(size=14)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''
        ##### Insights

        - _The fluctuations in the number of companies in both countries could also be due to changes in government policies or economic factors, which can have an impact on the funding and support available for space exploration._

        - _The US has a strong history of investing in space exploration through NASA and private companies like SpaceX and Blue Origin. This has led to more companies involved in space exploration in the US than in other countries. However, changes in government policies and economic factors can impact the number of companies involved._

        - _On the other hand, the number of companies involved in space exploration in the Soviet Union was more limited, with most space-related activities being controlled by the government. This could be a reason why the number of companies involved in space exploration in the Soviet Union did not increase as rapidly as in the US._
        ''')

        #-----------------------------------------------------------------------------------------
        ds = cold[cold['Status Mission'] == 'Failure']
        ds = ds.groupby(['year', 'country'])['alpha3'].count().reset_index()
        ds.columns = ['Year', 'Country', 'Failures']
        colors = ['rgb(53, 83, 255)', 'rgb(255, 128, 0)']
        fig = px.line(
            ds, 
            x="Year", 
            y="Failures", 
            color='Country', 
            title='USA vs USSR: Failures Year by Year',
            color_discrete_sequence=colors, # Set custom color palette
            labels={'Year': 'Year', 'Failures': 'Number of Failures', 'Country': 'Country'}, # Rename labels
            height=500, 
            width=800
        )
        fig.update_xaxes(tickangle=45, tickfont=dict(size=10))
        fig.update_layout(
            legend=dict(
                title=None,
                orientation='h',
                yanchor='top',
                y=1.1,
                xanchor='left',
                x=0.15,
                font=dict(size=12)
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''
        ##### Insights
        ''')
        st.write(''' _Overall, the higher success rate of the USSR's space program may have been due to a combination of factors-_''')
        st.write("-  _The US was playing catch-up to the Soviet Union, which had achieved several milestones before the US, such as launching the first satellite (Sputnik) and sending the first human (Yuri Gagarin) into space. As a result, the US was under pressure to make rapid progress in space exploration, which led to some rushed and risky decisions._")
        st.write("- _Secondly, the US was pushing the boundaries of technology and science in ways that had not been done before. This meant that there were more opportunities for things to go wrong._")
        st.write("- _Thirdly, there were technical challenges with the early American rockets, particularly the early versions of the Saturn rockets, which were prone to failures._ ")
    
    #####################################################################################
    ######                                                                         ######
    #####################################################################################
    elif page == 'Best Every Year':
        st.title("🏆" + page)
        ds = df.groupby(['year', 'country'])['Status Mission'].count().reset_index().sort_values(['year', 'Status Mission'], ascending=False)
        ds = pd.concat([group[1].head(1) for group in ds.groupby(['year'])])
        ds.columns = ['year', 'country', 'launches']
        fig = px.bar(
            ds, 
            x="year", 
            y="launches", 
            color='country', 
            title='Leaders by launches for every year (countries)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        #-------------------------------------------------------------------------------------
        ds = df[df['Status Mission']=='Success']
        ds = ds.groupby(['year', 'country'])['Status Mission'].count().reset_index().sort_values(['year', 'Status Mission'], ascending=False)
        ds = pd.concat([group[1].head(1) for group in ds.groupby(['year'])])
        ds.columns = ['year', 'country', 'launches']
        fig = px.bar(
            ds, 
            x="year", 
            y="launches", 
            color='country', 
            title='Leaders by success launches for every year (countries)',
            width=800
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''
        ##### Insights

        - _The USSR was the first country to launch a satellite, Sputnik 1, in 1957, which sparked the space race between the USSR and the USA.The combination of government support, early achievements, and technical expertise helped the USSR establish dominance in space exploration during the 1960s to 1990s._

        - _In recent years, the Chinese government has significantly increased its investment in space exploration, leading to rapid development and progress in China's space technology._

        ''')
        
        #----------------------------------------------------------------------------------------
        ds = df.groupby(['year', 'Company Name'])['Status Mission'].count().reset_index().sort_values(['year', 'Status Mission'], ascending=False)
        ds = pd.concat([group[1].head(1) for group in ds.groupby(['year'])])
        ds.columns = ['year', 'company', 'launches']
        fig = px.bar(
            ds, 
            x="year", 
            y="launches", 
            color='company', 
            title='Leaders by launches for every year (companies)',
            width=800
        )
        st.plotly_chart(fig, use_container_width=True)
        
        #---------------------------------------------------------------------------------------
        ds = df[df['Status Mission']=='Success']
        ds = ds.groupby(['year', 'Company Name'])['Status Mission'].count().reset_index().sort_values(['year', 'Status Mission'], ascending=False)
        ds = pd.concat([group[1].head(1) for group in ds.groupby(['year'])])
        ds.columns = ['year', 'company', 'launches']
        fig = px.bar(
            ds, 
            x="year", 
            y="launches", 
            color='company', 
            title='Leaders by success launches for every year (companies)',
            width=800
        )
        st.plotly_chart(fig, use_container_width=True)


        st.markdown('''
        ##### Insights

        - _The US and USSR had a head start in space exploration, with the US launching the first satellite in 1958 and the USSR launching the first human, Yuri Gagarin, into space in 1961. This early lead gave them a significant advantage in terms of experience and knowledge, which allowed them to develop more successful space programs. Additionally, both countries invested heavily in space exploration during the Cold War, which further advanced their programs._

        - _In recent years, companies like SpaceX and CASC have dominated the space industry due to their focus on innovation, cost-cutting measures, and a willingness to take risks. SpaceX, for example, has been able to develop reusable rockets and spacecraft, which has drastically reduced the cost of launching payloads into space._
        ''')

        
    #####################################################################################
    ######                                                                         ######
    #####################################################################################
    # elif page == 'Time Series Decomposition':
    #     st.write('This is Page 3.')
    #     df['month_year'] = df['year'].astype(str) + '-' + df['month'].astype(str)
    #     df['month_year'] = pd.to_datetime(df['month_year']).dt.to_period('M')
    #     ds = df.groupby(['month_year'])['alpha3'].count().reset_index()
    #     ds.columns = ['month_year', 'count']
    #     ds['month_year'] = ds['month_year'].astype(str)    
        
    #     dates = ['1957-10-01', '2020-08-02']
    #     start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
    #     dd = pd.DataFrame(
    #         list(
    #             OrderedDict(((start + timedelta(_)).strftime(r"%Y-%m"), None) for _ in range((end - start).days)).keys()
    #         ), 
    #         columns=['date']
    #     )
    #     dd['date'] = pd.to_datetime(dd['date'])
    #     ds['month_year'] = pd.to_datetime(ds['month_year'])
    #     res = pd.merge(ds, dd, how='outer', left_on='month_year', right_on='date')
    #     res = res.sort_values('date')[['date', 'count']]
    #     res = res.fillna(0).set_index('date')
        
    #     result = seasonal_decompose(res, model='additive', period=12)
    #     fig = make_subplots(rows=4, cols=1, shared_xaxes=True, 
    #                         vertical_spacing=0.07, subplot_titles=("Observed", "Trend", "Seasonal", "Residual"),
    #                         row_heights=[0.1, 0.1, 0.1, 0.1])
    #     for i, trace_name in enumerate(['observed', 'trend', 'seasonal', 'resid']):
    #         subplot = go.Scatter(x=result.observed.index, y=getattr(result, trace_name).values, mode='lines', showlegend=False)
    #         fig.add_trace(subplot, row=i+1, col=1)
    #     fig.update_layout(
    #         height=1300,
    #         title=dict(text='Seasonal Decomposition of Time Series', font=dict(size=24, color='white')),
    #         xaxis=dict(title='Date', showgrid=True, gridcolor='lightgray', gridwidth=0.1),
    #         yaxis=dict(title='Value', showgrid=True, gridcolor='lightgray', gridwidth=0.1),
    #         font=dict(family='Arial', size=16, color='white'),
    #         plot_bgcolor='rgba(0,0,0,0)',
    #         paper_bgcolor='rgba(0,0,0,0)'
    #     )
    #     st.plotly_chart(fig, use_container_width=True)
    
    #     #------------------------------------------------------------------------------------
    #     st.markdown('''
    #              ### Simple ARIMA Model
    #              not working
    #              ''')
    #     # MODEL
    #     model = ARIMA(ds['count'], order=(10,1,2))
    #     model_fit = model.fit()
        
    #     preds = model_fit.forecast(16)
    #     preds = preds.tolist()
    #     preds = [int(item) for item in preds]
    #     months = [
    #         '2020-09-01', '2020-10-01', '2020-11-01', '2020-12-01', 
    #         '2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01', 
    #         '2021-05-01', '2021-06-01', '2021-07-01', '2021-08-01', 
    #         '2021-09-01', '2021-10-01', '2021-11-01', '2021-12-01'
    #     ]
    #     new_df = pd.DataFrame()
    #     new_df['month_year'] = months
    #     new_df['count'] = preds
    #     data = pd.concat([ds, new_df])

    #     fig = px.line(
    #         data, 
    #         x="month_year", 
    #         y="count", 
    #         title='Launches per month prediction'
    #     )
    #     st.plotly_chart(fig, use_container_width=True)
        
    #####################################################################################
    ######                                                                         ######
    #####################################################################################
    elif page == 'India`s Place':
        st.title("" + page)
        st.markdown('''

        - _India and the United States have different histories and circumstances that have impacted their respective space exploration programs. The US has been a pioneer in space exploration, with NASA being established in 1958 and playing a significant role in space exploration since then._

        - _In contrast, India's space program started much later, with the establishment of the Indian Space Research Organisation (ISRO) in 1969. ISRO has faced challenges due to limited funding, technology, and infrastructure, which have hindered its progress in space exploration compared to the US._

        ''')
    
        compare = df[(df['country'] == 'India') | (df['country'] == 'USA')]
        india = compare[compare['country']=='India']
        years = india['year'].unique()
        years.sort()

        compare = compare[compare['year']>=1979]
        ds = compare['country'].value_counts().reset_index()
        ds.columns = ['country', 'count']
        colors = ['#1f77b4', '#ff7f0e']
        title_font = dict(size=20, color='#444444', family='Arial')

        fig = px.pie(ds, 
                    names='country', 
                    values='count', 
                    title='Number of Launches',
                    hole=0.5,
                    color_discrete_sequence=colors,
                    labels={'count': 'Number of Launches'},
                    width=700, 
                    height=500)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(title_font=dict(size=20, color='white', family='Arial'))
        st.plotly_chart(fig, use_container_width=True)

        #-----------------------------------------------------------------------------------
        ds = compare.groupby(['year', 'country'])['Status Mission'].count().reset_index()
        ds.columns = ['year', 'country', 'Launches']
        total = ds
        colors = ['rgb(255, 128, 0)', 'rgb(53, 83, 255)']
        fig = px.line(
            ds, 
            x="year", 
            y="Launches", 
            color='country', 
            title='USA vs India: Launches Year by Year',
            color_discrete_sequence=colors, # Set custom color palette
            labels={'year': 'Year', 'Launches': 'Number of Launches', 'country': 'Country'}, # Rename labels
            height=500, 
            width=800
        )
        fig.update_xaxes(tickfont=dict(size=10))
        fig.update_layout(
            legend=dict(
                title=None,
                orientation='h',
                yanchor='top',
                y=1.1,
                xanchor='left',
                x=0.75,
                font=dict(size=14),
                title_font=dict(size=20, color='white', family='Arial')
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''
        ##### Insights

        -  _India, on the other hand, has faced political and economic instability, which has affected its ability to invest in space exploration._

        - _Additionally, the geographic location of the two countries also plays a role. The US has easy access to space, with the presence of several launch sites. In contrast, India's location farther from the equator and lack of launch sites has made it more challenging to launch and access space._
        ''')

        #-----------------------------------------------------------------------------------------
        ds_total = compare.groupby(['year', 'country'])['Status Mission'].count().reset_index()
        ds_total.columns = ['year', 'country', 'Total']
        ds_success = compare[compare['Status Mission'] == 'Success'].groupby(['year', 'country'])['Status Mission'].count().reset_index()
        ds_success.columns = ['year', 'country', 'Success']
        ds_f = pd.merge(ds_total, ds_success, on=['year', 'country'], how='outer').fillna(0)
        ds_f['Success_pct'] = ds_f['Success'] / ds_f['Total'] * 100
        ds_mean = ds_f.groupby('country')['Success_pct'].mean().reset_index()
        
        fig = px.pie(ds_mean, 
             values='Success_pct', 
             names='country',
             title='Mean Success Percentage for USA vs India',
             color_discrete_sequence=['#1f77b4', '#ff7f0e'], 
             hole=0.5,
             labels={'country': 'Country', 'Success_pct': 'Mean Success Percentage'},
             width=700, 
             height=500)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(title_font=dict(size=20, color='white', family='Arial'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('''
        ##### Insights

        -  _India has a higher failure rate than the United States when it comes to space missions. This can be attributed to several factors, including the fact that India is still relatively new to the field of space exploration and is still developing its capabilities in this area._
        
        - _Additionally, India operates on a much smaller budget than the United States, which can impact the quality and reliability of its space missions._

        - _India's space exploration program has faced numerous political and geographic challenges over the years. For example, India has faced sanctions from other countries due to its nuclear program, which has impacted its ability to access certain technologies and resources needed for space exploration._
        ''')

        #####################################################################################
        ######                                                                         ######
        #####################################################################################

    elif page == 'Reference':
            url1 = "https://www.arianespace.com/press-release/ariane-5-successful-launch-webb-space-telescope/ "
            url2 = "https://chinapower.csis.org/china-space-launch/"
            url3 = "https://escholarship.org/content/qt0kj1q52j/qt0kj1q52j_noSplash_c9b2ab6f54dac13b34007979f3a8dd95.pdf?t=prfwji"
            url4 = "https://www.forbes.com/sites/startswithabang/2019/07/11/this-is-why-the-soviet-union-lost-the-space-race-to-the-usa/?sh=61cad0141925 "
            url5 = "https://www.nasa.gov/sites/default/files/files/SEINSI.pdf"
           
            st.markdown('''# Reference''')
            st.write(" - Arianespace Successful Launch[link](%s)" % url1 )
            st.write(" - China space launch [link](%s)" % url2 )
            st.write(" - Soviet union lost the space race [link](%s)" % url3 )
            st.write(" - The post Cold War issues [link](%s)" % url4 )
            st.write(" - Nasa Website [link](%s)" % url5 )
            

        
        
        #---------------------------------------------------------------------------------------
        # trace1 = go.Scatter(
        #     x=ds_f[ds_f['country'] == 'USA']['year'],
        #     y=ds_f[ds_f['country'] == 'USA']['Success_pct'],
        #     name='USA',
        #     line=dict(color='#1f77b4', width=2)
        # )
        # trace2 = go.Scatter(
        #     x=ds_f[ds_f['country'] == 'India']['year'],
        #     y=ds_f[ds_f['country'] == 'India']['Success_pct'],
        #     name='India',
        #     line=dict(color='#ff7f0e', width=2)
        # )
        # data = [trace1, trace2]
        # layout = go.Layout(
        #     title='Success Percentage by Year and Country',
        #     xaxis=dict(title='Year'),
        #     yaxis=dict(title='Success Percentage')
        # )
        # fig = go.Figure(data=data, layout=layout)
        # st.plotly_chart(fig, use_container_width=True)

        
        

# Add footer
# st.markdown("""
# <style>
# .footer {
#   position: fixed;
#   left: 0;
#   bottom: 0;
#   width: 100%;
#   background-color: #f5f5f5;
#   text-align: center;
# }
# </style>
# <div class="footer">
# <p>Made with ❤️ by [Your Name]</p>
# </div>
# """, unsafe_allow_html=True)
