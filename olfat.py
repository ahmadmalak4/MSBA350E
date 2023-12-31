


import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import streamlit as st


# Settings streamlit page configuration
st.set_page_config(layout="wide", page_title=None)
def main():
    st.markdown(
        """
        <style>
        .tab-label {
            text-align: center;
            color: red;
            font-size: 30px;
            font-weight: bold;
        }
        .tab-content {
            margin-top: 20px;
            color: red;
            font-size: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    st.markdown('<h1 style="font-size:3.5em;">Dashboards for Substance Use Analysis</h1>', unsafe_allow_html=True)


    tab_labels = ["Main", "Deaths from Substance Use", "Substance Use Disorders"]
    selected_tab = st.selectbox("Select a tab", tab_labels)

    if selected_tab == "Main":
        display_main_tab()
    elif selected_tab == "Deaths from Substance Use":
        display_deaths_tab()
    elif selected_tab == "Substance Use Disorders":
        display_disorders_tab()
def display_main_tab():
   
    # Create two columns
    col1, col2 = st.columns([2, 1])

    # Display the text in column 1
    with col1:
     st.markdown('<div style="font-size:2.5em;">In these dashboards, we examine <b><span style="color: red;">smoking, alcohol consumption</span></b>, and the utilization of illegal drugs. Our focus is on investigating the individuals who engage in these activities, observing how their usage patterns have evolved over time, and presenting estimations of the effects on their health. We analyze the overall effects of substance use, encompassing both indirect consequences on mortality and the direct repercussions of addiction and overdoses.</div>', unsafe_allow_html=True)
    # Display the image in column 2
    with col2:
     st.image('image.png', width=750)
    
def display_deaths_tab():
    st.header("Deaths from Substance Use")

    # Read the first CSV file
    df1 = pd.read_csv('1.csv')

    # Melt the dataframe to make it suitable for the stacked bar chart
    df1_melted = df1.melt(id_vars=['Entity', 'Year'],
                          value_vars=['Deaths - Drug use disorders - Sex: Both - Age: All Ages (Number)',
                                      'Deaths - Alcohol use disorders - Sex: Both - Age: All Ages (Number)',
                                      'Deaths - Cause: All causes - Risk: Tobacco - Sex: Both - Age: All Ages (Number)',
                                      'Deaths - Cause: All causes - Risk: Drug use - Sex: Both - Age: All Ages (Number)',
                                      'Deaths - Cause: All causes - Risk: Alcohol use - Sex: Both - Age: All Ages (Number)'],
                          var_name='Cause', value_name='Deaths')

    # Map the desired labels to the causes
    cause_labels = {
        'Deaths - Cause: All causes - Risk: Tobacco - Sex: Both - Age: All Ages (Number)': 'Tobacco (risk factor)',
        'Deaths - Cause: All causes - Risk: Drug use - Sex: Both - Age: All Ages (Number)': 'Illicit drug use (risk factor)',
        'Deaths - Cause: All causes - Risk: Alcohol use - Sex: Both - Age: All Ages (Number)': 'Alcohol use (risk factor)',
        'Deaths - Drug use disorders - Sex: Both - Age: All Ages (Number)': 'Drug use disorders',
        'Deaths - Alcohol use disorders - Sex: Both - Age: All Ages (Number)': 'Alcohol use disorders'
    }

    df1_melted['Cause'] = df1_melted['Cause'].map(cause_labels)

    # Sidebar for year slider and country selector for graph 1
    selected_year1 = st.select_slider('Year (Graph 1)', options=sorted(df1_melted['Year'].unique()), value=df1_melted['Year'].min())
    selected_country1 = st.selectbox('Country (Graph 1)', options=sorted(df1_melted['Entity'].unique()), index=0)

    # Filter data based on selections for graph 1
    df1_selected = df1_melted[(df1_melted['Entity'] == selected_country1) & (df1_melted['Year'] == selected_year1)]

    # Define the color map
    color_map = {
        'Tobacco (risk factor)': 'blue',
        'Alcohol use (risk factor)': 'blue',
        'Illicit drug use (risk factor)': 'blue',
        'Drug use disorders': 'red',
        'Alcohol use disorders': 'red'
    }

    # Create a horizontal bar chart with custom colors for graph 1
    fig1 = go.Figure()
    for cause in color_map.keys():
        subset = df1_selected[df1_selected['Cause'] == cause]
        fig1.add_trace(go.Bar(
            x=subset['Deaths'],
            y=subset['Cause'],
            orientation='h',
            name=cause,
            marker=dict(color=color_map[cause])
        ))

    # Set the layout for graph 1
    fig1.update_layout(
        title=dict(
            text='<b>Deaths from Tobacco, Alcohol and Drugs</b>',
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=24)
        ),
        annotations=[
            dict(
                x=0,
                y=-0.1,
                text='Direct deaths from substance use disorders (in red) result from alcohol or illicit drug use overdoses.',
                showarrow=False,
                xref='paper',
                yref='paper',
                font=dict(size=12)
            ),
            dict(
                x=0,
                y=-0.15,
                text='Indirect deaths (in blue) result from substance use as a risk factor for various diseases and injuries.',
                showarrow=False,
                xref='paper',
                yref='paper',
                font=dict(size=12)
            )
        ],
        xaxis_title='Deaths',
    yaxis_title='',
    barmode='stack',
    legend=dict(
        title='Cause of Death',
        orientation='h',
        yanchor='bottom',
        y=-0.3,
        xanchor='right',
        x=1
    ),
    width=800  # Add this line
)

    # Display graph 1
    st.plotly_chart(fig1)

    # Read the second CSV file
    df2 = pd.read_csv('2.csv')

    # Melt the data
    df2_melted = pd.melt(df2, id_vars=['Entity', 'Code', 'Year'],
                         value_vars=df2.columns[3:],
                         var_name='variable', value_name='value')

    # Simplify the Risk Factor column
    df2_melted['Risk Factor'] = df2_melted['variable'].apply(lambda x: x.split('- Risk: ')[1].split(' -')[0])

    # Sidebar for year slider and country selector for graph 2
    selected_years2 = st.slider('Select a year range (Graph 2)', min(df2['Year']), max(df2['Year']), (min(df2['Year']), max(df2['Year'])))
    selected_country2 = st.selectbox('Select a country (Graph 2)', df2['Entity'].unique())

    # Filter data according to the selected year and country for graph 2
    df2_filtered = df2_melted[(df2_melted['Year'] >= selected_years2[0]) &
                              (df2_melted['Year'] <= selected_years2[1]) &
                              (df2_melted['Entity'] == selected_country2)]

    # Check if only one year is selected for graph 2
    if selected_years2[0] == selected_years2[1]:
        # Sort by 'value' and select the top 5
        df2_filtered = df2_filtered.sort_values(by='value', ascending=False).head(5)
        # Create a bar chart for a single year for graph 2
        fig2 = px.bar(df2_filtered, x='value', y='Risk Factor',
                      labels={'value': 'Number of Deaths', 'Risk Factor': 'Risk Factor'},
                      title=f'Top 5 Risk Factors by Number of Deaths in {selected_years2[0]} for {selected_country2}')
    else:
        # Create a line chart for multiple years for graph 2
        fig2 = px.line(df2_filtered, x='Year', y='value', color='Risk Factor',
                       labels={'value': 'Number of Deaths', 'Risk Factor': 'Risk Factor'},
                       title=f'Number of Deaths by Risk Factor in {selected_years2[0]}-{selected_years2[1]} for {selected_country2}')

# Set the layout width
    fig2.update_layout(width=850)

# Display graph 2
    st.plotly_chart(fig2, use_container_width=False)

    # Load the third CSV file
    path = '3.csv'
    df3 = pd.read_csv(path)

    # Extract the disease names from the columns
    disease_cols = [col for col in df3.columns if 'Deaths - ' in col and '- Sex: Both' in col]
    disease_names = [col.split(' - ')[1] for col in disease_cols]
    df3_disease = df3.melt(id_vars=['Entity', 'Year'], value_vars=disease_cols, var_name='Cause', value_name='Number of Deaths')

    # Adjust disease names to be more readable
    df3_disease['Cause'] = df3_disease['Cause'].apply(lambda x: x.split(' - ')[1])

    # Sidebar for country and year range selection for graph 3
    selected_country3 = st.selectbox('Select a country (Graph 3):', df3_disease['Entity'].unique())
    year_range3 = st.slider('Select a year range (Graph 3):', int(df3_disease['Year'].min()), int(df3_disease['Year'].max()), (int(df3_disease['Year'].min()), int(df3_disease['Year'].max())))

    # Filter data by selected country for graph 3
    df3_filtered = df3_disease[df3_disease['Entity'] == selected_country3]

    # Check if one year or range of years is selected for graph 3
    if year_range3[0] != year_range3[1]:
        # Filter data by selected years for graph 3
        df3_filtered = df3_filtered[(df3_filtered['Year'] >= year_range3[0]) & (df3_filtered['Year'] <= year_range3[1])]

        # Plot for graph 3
        fig3 = go.Figure()
        for cause in df3_filtered['Cause'].unique():
            df3_cause = df3_filtered[df3_filtered['Cause'] == cause]
            fig3.add_trace(go.Scatter(x=df3_cause['Year'], y=df3_cause['Number of Deaths'], mode='lines+markers', name=cause))
            
        fig3.update_layout(
            title_text='Number of Deaths Over Time ',
            xaxis_title="Year",
            yaxis_title="Number of Deaths",
            autosize=False,
            width=800,
            height=500,
            hovermode="x"
        )
        # Set the layout width
        fig3.update_layout(width=850)
        st.plotly_chart(fig3)

    else:
        # Filter data for selected year for graph 3
        df3_filtered = df3_filtered[df3_filtered['Year'] == year_range3[0]]

        # Plot for graph 3
        fig3 = px.bar(df3_filtered.sort_values('Number of Deaths'), x='Number of Deaths', y='Cause', orientation='h')

        fig3.update_layout(
            title_text=f'Number of Deaths in {year_range3[0]} (Graph 3)',
            xaxis_title="Number of Deaths",
            autosize=False,
            width=800,
            height=500
        )

        st.plotly_chart(fig3)




def display_disorders_tab():
    st.header("Substance Use Disorders Prevalence")

    # Read the data for choropleth map
    choropleth_df = pd.read_csv('4.csv')

    # Rename the Disorder column
    choropleth_df = choropleth_df.rename(columns={'Prevalence - Substance use disorders - Sex: Both - Age: Age-standardized (Percent)': 'Substance use disorders'})

    # Create choropleth map
    choropleth_fig = px.choropleth(
        choropleth_df,
        locations='Code',
        color='Substance use disorders',
        hover_name='Entity',
        animation_frame='Year',
        projection='natural earth',
        color_continuous_scale=px.colors.sequential.Redor,
        title='Share of the Population with Substance Use Disorders Over the Years'
    )
    choropleth_fig.update_geos(showcountries=True)

    # Set the container width and height to make it square
    container_width = 900
    container_height = 800
    choropleth_fig.update_layout(width=container_width, height=container_height)
    choropleth_fig.update_layout(width=850)
    # Display the choropleth map
    st.plotly_chart(choropleth_fig)

    # Read the data for vector plot 1
    vector_df1 = pd.read_csv('5.csv')

    # Filter data based on selected countries
    selected_countries1 = st.multiselect('Select Countries (Vector Plot 1)', options=vector_df1['Entity'].unique())

    # Filter data based on selected countries
    vector_df_filtered1 = vector_df1[vector_df1['Entity'].isin(selected_countries1)]

    # Create vector plot 1
    vector_fig1 = go.Figure()

    for country in selected_countries1:
        country_data = vector_df_filtered1[vector_df_filtered1['Entity'] == country]
        years = country_data['Year']
        x = country_data['Prevalence - Substance use disorders - Sex: Male - Age: Age-standardized (Percent)']
        y = country_data['Prevalence - Substance use disorders - Sex: Female - Age: Age-standardized (Percent)']
        vector_fig1.add_trace(go.Scatter(x=x, y=y, mode='lines', name=country))

    vector_fig1.update_layout(
        title='Share with alcohol or drug use disorders, men vs. women, 1990 to 2003',
        xaxis_title='Share of men with alcohol or drug use disorders',
        yaxis_title='Share of women with alcohol or drug use disorders',
        width=container_width,
        height=container_height
    )
    vector_fig1.update_layout(width=850)
    # Display vector plot 1
    st.plotly_chart(vector_fig1)

    # Read the data for vector plot 2
    vector_df2 = pd.read_csv('6.csv')

    # Filter data based on selected countries
    selected_countries2 = st.multiselect('Select Countries (Vector Plot 2)', options=vector_df2['Entity'].unique())

    # Filter data based on selected countries
    vector_df_filtered2 = vector_df2[vector_df2['Entity'].isin(selected_countries2)]

    # Create vector plot 2
    vector_fig2 = go.Figure()

    for country in selected_countries2:
        country_data = vector_df_filtered2[vector_df_filtered2['Entity'] == country]
        x = country_data['Prevalence - Drug use disorders - Sex: Both - Age: Age-standardized (Percent)']
        y = country_data['Prevalence - Alcohol use disorders - Sex: Both - Age: Age-standardized (Percent)']
        vector_fig2.add_trace(go.Scatter(x=x, y=y, mode='lines', name=country))

    vector_fig2.update_layout(
        title='Share with alcohol or drug use disorders, men vs. women, 1990 to 2003',
        xaxis_title='Share of population with drug use disorder',
        yaxis_title='Share of population with alcohol use disorder',
        width=container_width,
        height=container_height
    )
    vector_fig2.update_layout(width=850)
    # Display vector plot 2
    st.plotly_chart(vector_fig2)

   
    
   # Load data
    data = pd.read_csv('7.csv')

    # Clean up column names
    column_names = {
        "Deaths - Cocaine use disorders - Sex: Both - Age: All Ages (Number)": "Cocaine",
        "Deaths - Drug use disorders - Sex: Both - Age: All Ages (Number)": "Illicit Drug",
        "Deaths - Opioid use disorders - Sex: Both - Age: All Ages (Number)": "Opioids",
        "Deaths - Alcohol use disorders - Sex: Both - Age: All Ages (Number)": "Alcohol",
        "Deaths - Other drug use disorders - Sex: Both - Age: All Ages (Number)": "Other Illicit",
        "Deaths - Amphetamine use disorders - Sex: Both - Age: All Ages (Number)": "Amphetamine"
    }

    data.rename(columns=column_names, inplace=True)
    
    # Melt DataFrame to a long format
    data_long = pd.melt(data, id_vars=['Entity', 'Code', 'Year'], value_vars=column_names.values(), var_name='Substance', value_name='Deaths')

    # Add color column
    colors = {'Alcohol': 'red', 'Illicit Drug': 'red', 'Opioids': 'blue', 'Other Illicit': 'blue', 'Amphetamine': 'blue', 'Cocaine': 'blue'}
    data_long['Color'] = data_long['Substance'].map(colors)

    # Create a bar chart
    fig = px.bar(data_long, y='Substance', x='Deaths', color='Color', 
                 labels={'Deaths':'Number of Deaths', 'Substance':'Substance Use Disorders'}, 
                 title='Number of Deaths from Substance Use Disorders',
                 animation_frame='Year', range_x=[0, data_long['Deaths'].max()],
                 hover_data=['Entity'], color_discrete_map='identity')

    # Sort bars by size
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    fig.update_layout(width=850)
    st.plotly_chart(fig)
    
# Load data
    data = pd.read_csv('8.csv')

    # Clean up column names
    column_names = {
        "Deaths - Substance use disorders - Sex: Both - Age: Age-standardized (Rate)": "Death Rate",
    }

    data.rename(columns=column_names, inplace=True)

    # Create a choropleth map
    fig = px.choropleth(data_frame=data, 
                        locations='Code', 
                        color='Death Rate', 
                        hover_name='Entity', 
                        animation_frame='Year', 
                        projection='natural earth',
                        color_continuous_scale='Reds',
                        labels={'Death Rate':'Death Rate from Alcohol and Drug Use Disorders'},
                        title='Death Rate from Alcohol and Drug Use Disorders')

    # Make the layout square and larger
    fig.update_layout(
        width=850,  # adjust as necessary
        height=850 # adjust as necessary
      
    )

    st.plotly_chart(fig)


        # Load data
    data = pd.read_csv('9.csv')

    # Clean up column names
    column_names = {
        "Deaths - Substance use disorders - Sex: Both - Age: 70+ years (Number)": "70+",
        "Deaths - Substance use disorders - Sex: Both - Age: 50-69 years (Number)": "50-69",
        "Deaths - Substance use disorders - Sex: Both - Age: 15-49 years (Number)": "15-49",
        "Deaths - Substance use disorders - Sex: Both - Age: Under 5 (Number)": "Under 5",
        "Deaths - Substance use disorders - Sex: Both - Age: 5-14 years (Number)": "5-14"
    }

    data.rename(columns=column_names, inplace=True)

    # Group by year and sum values
    data_grouped = data.groupby('Year').sum()

    # Create slider
    years = sorted(data_grouped.index.unique())
    selected_year = st.slider('Select year', min(years), max(years), min(years))

    # Filter data based on selected year
    filtered_data = data_grouped.loc[years[0]:selected_year]

    # Create area chart with Plotly
    fig = go.Figure()

    # Define gradient of blues for each age group
    colors = ['#d0e1f9', '#4d648d', '#283655', '#1e1f26', '#0b172a']

    for i, column in enumerate(filtered_data.columns):
        fig.add_trace(go.Scatter(
            x=filtered_data.index, 
            y=filtered_data[column], 
            mode='lines',
            name=column,
            stackgroup='one',
            line=dict(width=0.5, color=colors[i]),
            hovertemplate='<b>Year</b>: %{x}<br><b>Deaths</b>: %{y}<extra></extra>'
        ))

    fig.update_layout(
        title='Deaths from Substance Use Disorders by Age',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Number of Deaths'),
        hovermode='x'
    )
    fig.update_layout(width=850)
    st.plotly_chart(fig)

    

    # Load data
    data = pd.read_csv('10.csv')

    # Rename the long column for easier reference
    data.rename(columns={'DALYs (Disability-Adjusted Life Years) - Substance use disorders - Sex: Both - Age: All Ages (Percent)': 'DALYs %'}, inplace=True)

    # Allow user to select one or more countries
    countries = sorted(data['Entity'].unique())
    selected_countries = st.multiselect('Select country or countries', countries, default=countries[0])

    # Create line chart with Plotly
    fig = go.Figure()

    for country in selected_countries:
        # Filter data based on selected country
        country_data = data[data['Entity'] == country]

        fig.add_trace(
            go.Scatter(
                x=country_data['Year'], 
                y=country_data['DALYs %'], 
                mode='lines',
                name=country
            )
        )

    fig.update_layout(
        title='Alcohol and Drug Use Disorders as a Share of Total Disease Burden',
        xaxis_title='Year',
        yaxis_title='DALYs %',
        hovermode='x'
    )
    fig.update_layout(width=850)
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()




