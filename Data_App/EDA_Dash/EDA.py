import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go 
import dash
from dash import dcc, html
from dash.dependencies import Input, Output 
df = pd.read_csv(r"E:\Projects\BreastCancer_Project\EDA\Cleaned_BRCA.csv")
df_desc = df.describe().reset_index()
df_co = df[['Age','Protein1','Protein2','Protein3','Protein4','Tumor_Stage_Numeric']]
df['Date_of_Last_Visit'] = pd.to_datetime(df['Date_of_Last_Visit'])
df['Date_of_Surgery'] = pd.to_datetime(df['Date_of_Surgery'])
df.loc[df['Date_of_Last_Visit'] == '1-1-1900', 'Date_of_Last_Visit'] = df.loc[df['Date_of_Last_Visit'] == '1/1/1900', 'Date_of_Surgery']
df['Time_Difference'] = (df['Date_of_Last_Visit'] - df['Date_of_Surgery']).dt.days
df.loc[df['Date_of_Last_Visit'] == '5/3/2026', 'Date_of_Last_Visit'] = '5/3/2018'
df.loc[df['Date_of_Last_Visit'] == '9/24/2026', 'Date_of_Last_Visit'] = '9/24/2019'
df['year_surgery_date'] = pd.to_datetime(df['Year_of_Surgery'], format='%Y')
year_surgery_counts = df.groupby('year_surgery_date')['Patient_ID'].count()
app = dash.Dash(__name__)
cols = ['Age','Protein1','Protein2','Protein3','Protein4','Tumor_Stage_numeric']
colm = ['Age','Protein1','Protein2','Protein3','Protein4']
options = [{'label': 'Complete Corelation map', 'value': ''}] + [{'label': f'{col} & Tumor stage', 'value': col} for col in colm]
gender_counts = df['Gender'].value_counts()
patient_status_counts = df['Patient_Status'].value_counts()
Age_distribution = px.histogram(df, x="Age", nbins=10, title="Age distribution",color_discrete_sequence=['#0496ff'])
Age_distribution.update_layout(
    annotations=[
        go.layout.Annotation(
            x=60,  # X position of the text box
            y=65,  # Y position of the text box
            text='1- The patients in average get cancer in the period between 35 to 89',
            showarrow=False,  # If you want an arrow pointing to the text box
            bordercolor='#3b3f43',  # Border color
            borderwidth=2,  # Border width
            borderpad=4,  # Padding between text and border
            bgcolor='white', 
            opacity=0.8  
        ),
        go.layout.Annotation(
            x=60,  # X position of the text box
            y=55,  # Y position of the text box
            text='2- Most of patients descover the disease at the second stage',  # Text content
            showarrow=False,  # If you want an arrow pointing to the text box
            bordercolor='#3b3f43',  # Border color
            borderwidth=2,  # Border width
            borderpad=4,  # Padding between text and border
            bgcolor='white', 
            opacity=0.8  
        )
    ],
    xaxis_title="Age",
    yaxis_title="Number of Patients",
    title={
            'text': f"Distribution of Age (totally)",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        plot_bgcolor='rgb(242,242,242)',
        paper_bgcolor='rgb(242,242,242)',
        font=dict(color='rgb(34,24,54)'),
        height=600,
        xaxis=dict(showgrid=False), 
        yaxis=dict(showgrid=False)
)
Age_distribution.update_traces(marker=dict(line=dict(color='rgb(34,24,54)', width=1)))
Age_distribution_stage = px.histogram(df, x='Age',
                  color_discrete_sequence=['#0496ff'],
                   title='Distribution of Age by Tumor Stage')
Age_distribution_stage.update_traces(marker=dict(line=dict(color='rgb(34,24,54)', width=1)))
Age_distribution_stage.update_layout(
    title={
            'text': f"Distribution of Age according to tumor stage",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        plot_bgcolor='rgb(242,242,242)',
        paper_bgcolor='rgb(242,242,242)',
        font=dict(color='rgb(34,24,54)'),
        height=600,
        xaxis=dict(showgrid=False), 
        yaxis=dict(showgrid=False),
        updatemenus=[
        {
            "buttons": [
                {
                    "args": [{"x": [df[df['Tumor_Stage_Numeric'] == 1]['Age']], "name": "Stage 1"}],
                    "label": "Stage 1",
                    "method": "restyle"
                },
                {
                    "args": [{"x": [df[df['Tumor_Stage_Numeric'] == 2]['Age']], "name": "Stage 2"}],
                    "label": "Stage 2",
                    "method": "restyle"
                },
                {
                    "args": [{"x": [df[df['Tumor_Stage_Numeric'] == 3]['Age']], "name": "Stage 3"}],
                    "label": "Stage 3",
                    "method": "restyle"
                }
            ],
            "direction": "down",
            "showactive": True
        }
    ]
)
gender_pie = px.pie(gender_counts, values=gender_counts.values, names=gender_counts.index,
            color_discrete_sequence=['#c9184a','#218380'])
gender_pie.update_layout(
    title={
            'text': f"Distribution of Patients by Gender",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        plot_bgcolor='rgb(242,242,242)',
        paper_bgcolor='rgb(242,242,242)',
        font=dict(color='rgb(34,24,54)'),
        height=600,
        xaxis=dict(showgrid=False), 
        yaxis=dict(showgrid=False)
)
status_pie = px.pie(df[df['Year_of_Surgery'].isin([2017, 2018, 2020])]['Patient_Status'].value_counts(),
                    values=df[df['Year_of_Surgery'].isin([2017, 2018, 2020])]['Patient_Status'].value_counts().values, 
                    names=df[df['Year_of_Surgery'].isin([2017, 2018, 2020])]['Patient_Status'].value_counts().index,
                    color_discrete_sequence=['#218380','#8c001a','#eadeda'])
status_pie.update_layout(
    title={
            'text': f"Distribution of Patients by Status",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        plot_bgcolor='rgb(242,242,242)',
        paper_bgcolor='rgb(242,242,242)',
        font=dict(color='rgb(34,24,54)'),
        height=600,
        xaxis=dict(showgrid=False), 
        yaxis=dict(showgrid=False),
        updatemenus=[{
        "buttons": [
            {
                "args": [{"values": [df[df['Year_of_Surgery'].isin([2017, 2018, 2020])]['Patient_Status'].value_counts().values],
                          "labels": [df[df['Year_of_Surgery'].isin([2017, 2018, 2020])]['Patient_Status'].value_counts().index]}],
                "label": "All Years",
                "method": "restyle"
            },
            {
                "args": [{"values": [df[df['Year_of_Surgery'] == 2017]['Patient_Status'].value_counts().values],
                          "labels": [df[df['Year_of_Surgery'] == 2017]['Patient_Status'].value_counts().index]}],
                "label": "2017",
                "method": "restyle"
            },
            {
                "args": [{"values": [df[df['Year_of_Surgery'] == 2018]['Patient_Status'].value_counts().values],
                          "labels": [df[df['Year_of_Surgery'] == 2018]['Patient_Status'].value_counts().index]}],
                "label": "2018",
                "method": "restyle"
            },
            {
                "args": [{"values": [df[df['Year_of_Surgery'] == 2019]['Patient_Status'].value_counts().values],
                          "labels": [df[df['Year_of_Surgery'] == 2019]['Patient_Status'].value_counts().index]}],
                "label": "2019",
                "method": "restyle"
            }
        ],
        "direction": "down",
        "showactive": True
    }]
)
count_per_time = px.line(year_surgery_counts, x=year_surgery_counts.index, y=year_surgery_counts.values,
              markers=True)
count_per_time.update_layout(
    xaxis_title='Year of Surgery',
    yaxis_title='Number of Patients')
count_per_time.update_layout(
        plot_bgcolor='rgb(242,242,242)',
        paper_bgcolor='rgb(242,242,242)',
        font=dict(color='rgb(34,24,54)'),
        height=600,
        xaxis=dict(showgrid=False), 
        yaxis=dict(showgrid=False)
)
collective_buble = px.scatter(df, x="Patient_Status",
                               y="Histology",
                                size="Tumor_Stage_Numeric",
                                color="Tumour_Stage",
                                hover_name="Patient_Status",
                                size_max=60)
collective_buble.update_layout(
        plot_bgcolor='rgb(242,242,242)',
        paper_bgcolor='rgb(242,242,242)',
        font=dict(color='rgb(34,24,54)'),
        height=600,
        xaxis=dict(showgrid=True), 
        yaxis=dict(showgrid=False))
days_difference = px.box(df, x='Patient_Status', y='Time_Difference', color='Patient_Status')
days_difference.update_layout(
    xaxis_title='Patient Status',
                  yaxis_title='Days Between Last Visit and Surgery',
                  plot_bgcolor='rgb(242,242,242)',
        paper_bgcolor='rgb(242,242,242)',
        font=dict(color='rgb(34,24,54)'),
        height=600,
        xaxis=dict(showgrid=True), 
        yaxis=dict(showgrid=False))
surgery_stage = px.histogram(df, x="Surgery_type", color="Patient_Status", barmode="stack")
surgery_stage.update_layout(xaxis_title='Surgery Type',
                  yaxis_title='Count of Pateints',
                  plot_bgcolor='rgb(242,242,242)',
        paper_bgcolor='rgb(242,242,242)',
        font=dict(color='rgb(34,24,54)'),
        height=600,
        xaxis=dict(showgrid=True), 
        yaxis=dict(showgrid=False))
surgery_hist = px.histogram(df, x="Surgery_type", color="Histology", barmode="stack")
surgery_hist.update_layout(xaxis_title='Surgery Type',
                  yaxis_title='Count of Pateints',
                  plot_bgcolor='rgb(242,242,242)',
        paper_bgcolor='rgb(242,242,242)',
        font=dict(color='rgb(34,24,54)'),
        height=600,
        xaxis=dict(showgrid=True), 
        yaxis=dict(showgrid=False))
proteins_hist = px.scatter_matrix(
    df,
    dimensions=['Protein1', 'Protein2', 'Protein3', 'Protein4'],
    color='Histology',
    title='Scatter Matrix of Protein Levels by Histology'
)
proteins_hist.update_layout(
                  plot_bgcolor='rgb(242,242,242)',
        paper_bgcolor='rgb(242,242,242)',
        font=dict(color='rgb(34,24,54)'),
        height=600,
        xaxis=dict(showgrid=True), 
        yaxis=dict(showgrid=False))
app.layout= html.Div(children=[
    html.Div(children=[html.Img(src='/assets/Header1.png',
                                style={'width':'100%',
                                       'height':'15%',
                                       'margin':'0auto',
                                       'padding':'0',
                                       'boxShadow': '8px 8px 8px rgba(0, 0, 0, 0.1)'})])
    ,html.H2("Data describtion table",style={"textAlign":'center',
                                             'color':'#3b3f43',
                                             'background-color':'white',
                                             'box-shadow':'5px 5px 15px rgba(0, 0, 0, 0.3)'})
    ,dash.dash_table.DataTable( id='table',
                              columns=[{'name':col,'id':col} for col in df_desc.columns],
                              data=df_desc.to_dict('records'),
                              style_table={'overflowX': 'auto'},
                              style_cell={'textAlign': 'center'},
                              style_header={
                                  'backgroundColor': 'lightgrey',
                                  'fontWeight': 'bold'})
    ,html.H2("Corelation Heat map (Select a Coloumn to see the relationship with Tumor stage)",
             style={"textAlign":'center',
                    'color':'#3b3f43',
                    'background-color':'white',
                    'box-shadow':'5px 5px 15px rgba(0, 0, 0, 0.3)'},id='cor')
    ,html.Div(children=[
        dcc.Dropdown(id='choose X',options=options,placeholder="Click here to select one Column",style={
            'color':'blue'
        })
    ])
    ,html.Div(children=[
        dcc.Graph(id='correlation')
    ]),
    html.H2("Total Age distribution V.s Age distribution according to tumor stage",
             style={"textAlign":'center',
                    'color':'#3b3f43',
                    'background-color':'white',
                    'box-shadow':'5px 5px 15px rgba(0, 0, 0, 0.3)'})
    ,html.Div(children=[
        dcc.Graph(figure=Age_distribution_stage,
                  style={'width':'50%','display':'inline-block'}),
        dcc.Graph(figure=Age_distribution,
                  style={'width':'50%','display':'inline-block'})
    ],style={
    'borderRadius': '8px',
    'boxShadow': '8px 8px 8px rgba(0, 0, 0, 0.1)',
    'fontFamily': 'Arial, sans-serif',
    'fontSize': '16px',
    'lineHeight': '1.5',
    'alignItems': 'center'
}
),
html.H2("Most year from the number of surgries",
             style={"textAlign":'center',
                    'color':'#3b3f43',
                    'background-color':'white',
                    'box-shadow':'5px 5px 15px rgba(0, 0, 0, 0.3)'}),
    html.Div(children=[
        dcc.Graph(figure=count_per_time)
    ]),
    html.H2("Distribution of Pateints by gender & Status",
             style={"textAlign":'center',
                    'color':'#3b3f43',
                    'background-color':'white',
                    'box-shadow':'5px 5px 15px rgba(0, 0, 0, 0.3)'}),
    html.Div(children=[
        dcc.Graph(figure=gender_pie,style={
            'width':'50%',
            'display':'inline-block'
        }),
        dcc.Graph(figure=status_pie,
                  style={
            'width':'50%',
            'display':'inline-block'
        })
    ]
    ),
    html.H2("Difference between Days of surgery and Last visit",
             style={"textAlign":'center',
                    'color':'#3b3f43',
                    'background-color':'white',
                    'box-shadow':'5px 5px 15px rgba(0, 0, 0, 0.3)'})
    ,html.Div(children=[
        dcc.Graph(figure=days_difference)
    ]

    ),
    html.H2("Discovering the Histology - Tumor stage relationship",
             style={"textAlign":'center',
                    'color':'#3b3f43',
                    'background-color':'white',
                    'box-shadow':'5px 5px 15px rgba(0, 0, 0, 0.3)'}),
    html.Div(children=[
        dcc.Graph(figure=collective_buble)
    ]
    ),
    html.Div(children=[html.H2("Discovering the Surgery type - Tumor stage relationship",
             style={"textAlign":'center',
                    'color':'#3b3f43',
                    'background-color':'white',
                    'box-shadow':'5px 5px 15px rgba(0, 0, 0, 0.3)'})
    ,html.Div(children=[
        dcc.Graph(figure=surgery_stage)
    ]

    )]),
    html.Div(children=[
        html.H2("Discovering the Surgery type - Histology relationship",
             style={"textAlign":'center',
                    'color':'#3b3f43',
                    'background-color':'white',
                    'box-shadow':'5px 5px 15px rgba(0, 0, 0, 0.3)'})
    ,html.Div(children=[
        dcc.Graph(figure=surgery_hist)
    ]
    ) 
    ]),
    html.Div(children=[
        html.H2("Proteins and Histology type",
             style={"textAlign":'center',
                    'color':'#3b3f43',
                    'background-color':'white',
                    'box-shadow':'5px 5px 15px rgba(0, 0, 0, 0.3)'})
    ,html.Div(children=[
        dcc.Graph(figure=proteins_hist)
    ]
    ) 
    ])
    ,
    html.Div(children=[
        html.Img(src='/assets/Footer1-1.png',
                                style={'width':'100%',
                                       'height':'15%',
                                       'margin':'0auto',
                                       'padding':'0',
                                       'boxShadow': '8px 8px 8px rgba(0, 0, 0, 0.1)'})
    ])
])
@app.callback(
    Output('correlation', 'figure'),
    [Input('choose X', 'value')]
)
def update_graph(selected_column):
    cor = df_co.corr()
    text = np.round(cor.values, 2).astype(str)
    heatmap_cor = go.Figure(data=go.Heatmap(
        z = cor.values,
        x = cor.columns,
        y=cor.columns,
        zmin = -1 , zmax = 1,
        colorscale='blues',
        colorbar=dict(title="Correlation"),
        text=text
    ))
    heatmap_cor.update_traces(text=text, texttemplate="%{text}", textfont_size=12)
    heatmap_cor.update_layout(title = {'x':.5,'xanchor':'center','yanchor':'top'},
                                    xaxis_nticks=36,
                                    plot_bgcolor='rgb(242,242,242)',
                                    paper_bgcolor='rgb(242,242,242)',
                                    font=dict(color='rgb(34,24,54)'),
                                    height=750)

    if selected_column is None or selected_column == '':
        return heatmap_cor

    # Calculate the correlation between 'Tumor_Stage_Numeric' and the selected column
    cor_value = df['Tumor_Stage_Numeric'].corr(df[selected_column])
    cor_text = np.round(cor_value, 2).astype(str)

    # Create a simple bar plot to show the correlation
    fig = go.Figure(data=[go.Bar(
        x=[selected_column], 
        y=[cor_value], 
        text=cor_text,
        textposition='auto',
        marker_color='#0496ff'
    )])

    fig.update_layout(
        title={
            'text': f"Correlation with Tumor Stage Numeric",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        plot_bgcolor='rgb(242,242,242)',
        paper_bgcolor='rgb(242,242,242)',
        font=dict(color='rgb(34,24,54)'),
        height=600,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    return fig
if __name__ == '__main__':
    app.run_server(debug=True)
