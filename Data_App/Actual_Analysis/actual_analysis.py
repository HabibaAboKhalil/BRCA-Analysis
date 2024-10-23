import pandas as pd 
import numpy as np
import plotly.express as px
import plotly.graph_objs as go 
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
df = pd.read_csv(r"E:\Projects\BreastCancer_Project\EDA\Cleaned_BRCA.csv")
df['Date_of_Last_Visit'] = pd.to_datetime(df['Date_of_Last_Visit'])
df['Date_of_Surgery'] = pd.to_datetime(df['Date_of_Surgery'])
df.loc[df['Date_of_Last_Visit'] == '1-1-1900', 'Date_of_Last_Visit'] = df.loc[df['Date_of_Last_Visit'] == '1/1/1900', 'Date_of_Surgery']
df['Time_Difference'] = (df['Date_of_Last_Visit'] - df['Date_of_Surgery']).dt.days
df.loc[df['Date_of_Last_Visit'] == '5/3/2026', 'Date_of_Last_Visit'] = '5/3/2018'
df.loc[df['Date_of_Last_Visit'] == '9/24/2026', 'Date_of_Last_Visit'] = '9/24/2019'
df['year_surgery_date'] = pd.to_datetime(df['Year_of_Surgery'], format='%Y')
def calculate_survival_rate(histology_type):
    histology_data = df[df['Histology'] == histology_type]
    survived_count = histology_data[histology_data['Patient_Status'] == 'Alive'].shape[0]
    total_count = histology_data.shape[0]
    survival_rate = (survived_count / total_count) * 100 if total_count > 0 else 0
    return survived_count, total_count - survived_count
def most_surgical_type(histology_type):
    hist_type = df[df['Histology'] == histology_type]
    survival_by_surgery = hist_type.groupby('Surgery_type')['Patient_Status'].apply(
    lambda x: (x == 'Alive').mean() * 100).reset_index()
    survival_by_surgery.columns = ['Surgery_type', 'Survival_Rate']
    return survival_by_surgery
def stage_each_hist(histology_type):
    stage_each=df[df['Histology']==histology_type]
    stage_each_count=stage_each['Tumour_Stage'].value_counts()
    stage_each_count=stage_each_count.reset_index()
    stage_each_count.columns=['Tumour_Stage','Count']
    return stage_each_count
surgery_counts_by_histology = df.groupby(['Histology', 'Surgery_type']).size().reset_index(name='Count')
survival_by_histology_surgery = df.groupby(['Histology', 'Surgery_type'])['Patient_Status'].apply(
    lambda x: (x == 'Alive').mean() * 100).reset_index()
survival_by_histology_surgery.columns = ['Histology', 'Surgery_type', 'Survival_Rate']
ductal_stages_count = stage_each_hist('Infiltrating Ductal Carcinoma')
lobular_stages_count = stage_each_hist('Infiltrating Lobular Carcinoma')
mucinous_stages_count = stage_each_hist('Mucinous Carcinoma')
combined_data = pd.merge(surgery_counts_by_histology, survival_by_histology_surgery, on=['Histology', 'Surgery_type'])
surgery_lobular = most_surgical_type("Infiltrating Lobular Carcinoma")
surgery_ductal = most_surgical_type("Infiltrating Ductal Carcinoma")
surgery_mucinous = most_surgical_type("Mucinous Carcinoma")
tumor_stage_counts = df['Tumour_Stage'].value_counts().reset_index()
tumor_stage_counts.columns = ['Tumour_Stage', 'Count']
most_common_tumor_stage = tumor_stage_counts.loc[tumor_stage_counts['Count'].idxmax()]
surgery_distribution = df.groupby(['Tumour_Stage', 'Surgery_type']).size().reset_index(name='Count')
df['Survival'] = df['Patient_Status'].apply(lambda x: 1 if x == 'Alive' else 0)
survival_rate_by_stage = df.groupby('Tumour_Stage')['Survival'].mean().reset_index()
survival_rate_by_stage['Survival'] = survival_rate_by_stage['Survival'] * 100
app = dash.Dash(__name__,serve_locally=True)
most_common_diagnosis = px.bar(tumor_stage_counts,
             y='Count',
             x='Tumour_Stage',
             color = 'Tumour_Stage',
             labels={'Tumour_Stage': 'Tumor Stage', 'Count': 'Number of Cases'})
most_common_diagnosis.update_layout(
                                title=dict(text="Number of Cases by Tumor Stage at the Time of Diagnosis",
                                           x=0.5,
                                            xanchor='center'),
                                xaxis=dict(showgrid=False),
                                yaxis=dict(showgrid=False),
                                plot_bgcolor='rgb(242,242,242)',
                                paper_bgcolor='rgb(242,242,242)')

surgery_each_type = px.bar(surgery_distribution,
             x='Tumour_Stage',
             y='Count',
             color='Surgery_type',
             title="Distribution of Surgery Types Across Different Tumor Stages",
             labels={'Tumour_Stage': 'Tumor Stage', 'Count': 'Number of Cases'},
             barmode='group')
surgery_each_type.update_layout(
    title = dict(x=0.5,
                 y=.96,
                 xanchor='center'),
                 xaxis=dict(showgrid=False),
                 yaxis=dict(showgrid=False),
    xaxis_title='Tumor Stage',
    yaxis_title='Number of Cases',
    legend_title='Surgery Type',
    plot_bgcolor='rgb(242,242,242)',
    paper_bgcolor='rgb(242,242,242)'
)
survival_rate_pie= px.pie(survival_rate_by_stage,
             names='Tumour_Stage',
             values='Survival',
             title="Survival Rate (%) Based on Tumor Stage at the Time of Surgery")
survival_rate_pie.update_layout(
    plot_bgcolor='rgb(242,242,242)',
    paper_bgcolor='rgb(242,242,242)',
    title = dict(x=0.5,
        xanchor='center')
)
survived_lobular, dead_lobular = calculate_survival_rate('Infiltrating Lobular Carcinoma')
survived_ductal, dead_ductal = calculate_survival_rate('Infiltrating Ductal Carcinoma')
survived_mucinous, dead_mucinous = calculate_survival_rate('Mucinous Carcinoma')
tumor_histology = go.Figure()

# Adding traces for both histology types (initially only one will be visible)
tumor_histology.add_trace(go.Pie(values=[survived_lobular, dead_lobular],
                     labels=['Alive', 'Dead'],
                     name='Infiltrating Lobular Carcinoma',
                     marker=dict(colors=['#636efa', '#ef553b'])))

tumor_histology.add_trace(go.Pie(values=[survived_ductal, dead_ductal],
                     labels=['Alive', 'Dead'],
                     name='Infiltrating Ductal Carcinoma',
                     marker=dict(colors=['#636efa', '#ef553b']),
                     visible=False))
tumor_histology.add_trace(go.Pie(values=[survived_mucinous, dead_mucinous],
                     labels=['Alive', 'Dead'],
                     name='Mucinous Carcinoma',
                     marker=dict(colors=['#636efa', '#ef553b']),
                     visible=False))
tumor_histology.update_layout(
    title=dict(text = 'Survival Rate of Patients by Histology Type',
               x=0.5,
                xanchor='center'),
    plot_bgcolor='rgb(242,242,242)',
    paper_bgcolor='rgb(242,242,242)',
    updatemenus=[dict(
        type="buttons",
        direction="down",
        buttons=[
            dict(label="Infiltrating Lobular Carcinoma",
                 method="update",
                 args=[{"visible": [True, False,False]}, 
                       {"title": "Survival Rate of Patients with Infiltrating Lobular Carcinoma"}]),
            dict(label="Infiltrating Ductal Carcinoma",
                 method="update",
                 args=[{"visible": [False, True,False]},  
                       {"title": "Survival Rate of Patients with Infiltrating Ductal Carcinoma"}]),
            dict(label="Mucinous Carcinoma",
                 method="update",
                 args=[{"visible": [False, False,True]},  
                       {"title": "Survival Rate of Patients with Infiltrating Ductal Carcinoma"}])
        ]
    )]
)
surgery_by_hist_bar = go.Figure()
surgery_by_hist_bar.add_trace(go.Bar(
    x=surgery_lobular['Surgery_type'],
    y=surgery_lobular['Survival_Rate'],
    name="Infiltrating Lobular Carcinoma",
    marker_color=px.colors.qualitative.Pastel[0]  # Using marker_color directly
))

# Add trace for Infiltrating Ductal Carcinoma
surgery_by_hist_bar.add_trace(go.Bar(
    x=surgery_ductal['Surgery_type'],
    y=surgery_ductal['Survival_Rate'],
    name="Infiltrating Ductal Carcinoma",
    marker_color=px.colors.qualitative.Pastel[1]  # Unique color
))

# Add trace for Mucinous Carcinoma
surgery_by_hist_bar.add_trace(go.Bar(
    x=surgery_mucinous['Surgery_type'],
    y=surgery_mucinous['Survival_Rate'],
    name="Mucinous Carcinoma",
    marker_color=px.colors.qualitative.Pastel[2]  # Another unique color
))

# Update layout and dropdown buttons for interactivity
surgery_by_hist_bar.update_layout(
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    title=dict(text='Survival Rate Based on Surgery Type', x=0.5, xanchor='center'),
    plot_bgcolor='rgb(242,242,242)',
    paper_bgcolor='rgb(242,242,242)',
    showlegend=False,
    updatemenus=[dict(
        type="buttons",
        direction="down",
        buttons=[
            dict(label="Infiltrating Lobular Carcinoma",
                 method="update",
                 args=[{"visible": [True, False, False]}, 
                       {"title": "Survival Rate of Patients with Infiltrating Lobular Carcinoma"}]),
            dict(label="Infiltrating Ductal Carcinoma",
                 method="update",
                 args=[{"visible": [False, True, False]},  
                       {"title": "Survival Rate of Patients with Infiltrating Ductal Carcinoma"}]),
            dict(label="Mucinous Carcinoma",
                 method="update",
                 args=[{"visible": [False, False, True]},  
                       {"title": "Survival Rate of Patients with Mucinous Carcinoma"}])
        ]
    )]
)
surgery_by_hist_scatter= px.scatter(combined_data,
                 x='Surgery_type',
                 y='Survival_Rate',
                 size='Count',
                 size_max=60,
                 color='Histology',  
                 title='Survival Rate Based on Surgery Type for Different Histology Types',
                 labels={'Surgery_type': 'Surgery Type', 'Survival_Rate': 'Survival Rate (%)'},
                 hover_data=['Count'],
                 color_discrete_sequence=['#f6cf71','#66c5cc','#f89c74']) 


surgery_by_hist_scatter.update_traces(textposition='top center')


surgery_by_hist_scatter.update_layout(
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    plot_bgcolor='rgb(242,242,242)',
    paper_bgcolor='rgb(242,242,242)',
    yaxis_title='Survival Rate (%)',
    showlegend=True
)
stage_hist_count = go.Figure()
stage_hist_count.add_trace(go.Bar(
    x=lobular_stages_count['Tumour_Stage'],
    y=lobular_stages_count['Count'],
    name="Infiltrating Lobular Carcinoma",
    marker_color=px.colors.qualitative.Pastel[0]  # Using marker_color directly
))

stage_hist_count.add_trace(go.Bar(
    x=ductal_stages_count['Tumour_Stage'],
    y=ductal_stages_count['Count'],
    name="Infiltrating Ductal Carcinoma",
    marker_color=px.colors.qualitative.Pastel[1] 
))

# Add trace for Mucinous Carcinoma
stage_hist_count.add_trace(go.Bar(
    x=mucinous_stages_count['Tumour_Stage'],
    y=mucinous_stages_count['Count'],
    name="Mucinous Carcinoma",
    marker_color=px.colors.qualitative.Pastel[2]  # Another unique color
))
stage_hist_count.update_layout(
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    title=dict(text='Survival Rate Based on Surgery Type', x=0.5, xanchor='center'),
    plot_bgcolor='rgb(242,242,242)',
    paper_bgcolor='rgb(242,242,242)',
    showlegend=True,
    xaxis_title="Tumour Stage",
    yaxis_title="Count",
    updatemenus=[dict(
        type="buttons",
        direction="down",
        buttons=[
            dict(label="Infiltrating Lobular Carcinoma",
                 method="update",
                 args=[{"visible": [True, False, False]}, 
                       {"title": "Survival Rate of Patients with Infiltrating Lobular Carcinoma"}]),
            dict(label="Infiltrating Ductal Carcinoma",
                 method="update",
                 args=[{"visible": [False, True, False]},  
                       {"title": "Survival Rate of Patients with Infiltrating Ductal Carcinoma"}]),
            dict(label="Mucinous Carcinoma",
                 method="update",
                 args=[{"visible": [False, False, True]},  
                       {"title": "Survival Rate of Patients with Mucinous Carcinoma"}])
        ]
    )]
)
app.layout = html.Div(children=[
    html.Div(children=[
        html.Img(src='/assets/Header.png',style={'width':'100%',
                                       'height':'15%',
                                       'margin':'0auto',
                                       'padding':'0',
                                       'boxShadow': '8px 8px 8px rgba(0, 0, 0, 0.1)'}),
        html.H1("",style={"textAlign":'center',
                    'color':'white',
                    'background-color':'black',
                    'box-shadow':'5px 5px 15px rgba(0, 0, 0, 0.3)'})
    ]),
    html.Div(children=[
        html.H2("What is the most common age group among males and females diagnosed with cancer?",style={"textAlign":'center',
                    'color':'#221836',
                    'background-color':'white',
                    'box-shadow':'5px 5px 15px rgba(0, 0, 0, 0.3)',
                    'margin-top':'25px'})
    ]),
    html.Div(children=[dcc.Graph(id="tumor_box")]),
    dcc.Slider(df['Year_of_Surgery'].min(),
               df['Year_of_Surgery'].max(),
               step=None,
               value=df['Year_of_Surgery'].max(),
               marks={str(year): str(year) for year in df['Year_of_Surgery'].unique()},
               id="slider-year")
    ,html.P('It\'s clear that women from different ages get cancer, but the most common age is between 56 and 60, with the minimum age being 26 years old.For men, the number of cases isn\'t a lot, but the most common age is 51.', id="par1"),
    html.Div(children=[
        html.H2("What is the most common stage at the time of diagnosis and the most surgery for each type?",
                style={"textAlign":'center',
                    'color':'#221836',
                    'background-color':'white',
                    'box-shadow':'5px 5px 15px rgba(0, 0, 0, 0.3)'})
    ])
    ,html.Div(children=[dcc.Graph(figure=most_common_diagnosis,style={'display':'inline-block',
                                                                'width':'50%','margin-top':'20px'}),
                       dcc.Graph(figure=surgery_each_type,style={'display':'inline-block',
                                                                'width':'50%'})
                        ]),

    html.P('Large number of patients come with stage II of breast cancer. The first choice for this stage is operations other than 3 mentioned types then Modified Radical Mastectomy ', id="par1")
    ,html.Div(children=[
         html.H2("Survival rate based on Tumor stage and type after surgery",
                style={"textAlign":'center',
                    'color':'#221836',
                    'background-color':'white',
                    'box-shadow':'5px 5px 15px rgba(0, 0, 0, 0.3)'})
    ]),
    html.Div(children=[dcc.Graph(figure=survival_rate_pie,style={'display':'inline-block',
                                                                'width':'50%'}),
                       dcc.Graph(figure=tumor_histology,style={'display':'inline-block',
                                                                'width':'50%'})
    ]),
    html.P('Survival rate after surgery from all stages is near to eachother. And this is a good sign. Also in different types of histology', id="par1")
    ,html.Div(children=[
         html.H2("Most cancer stage for each histology",
                style={"textAlign":'center',
                    'color':'#221836',
                    'background-color':'white',
                    'box-shadow':'5px 5px 15px rgba(0, 0, 0, 0.3)'})
    ]),
    html.Div(children=[
        dcc.Graph(figure=stage_hist_count)
    ]),
    html.P('Stage 2 is the most common stage in all histology types. And stage 3 is not found in Mucinous', id="par1")
    ,html.Div(children=[
         html.H2("Most surgery type performed with different Carcinomas, and how did it impact survival?",
                style={"textAlign":'center',
                    'color':'#221836',
                    'background-color':'white',
                    'box-shadow':'5px 5px 15px rgba(0, 0, 0, 0.3)'})
    ]),
    html.Div(children=[
        dcc.Graph(figure=surgery_by_hist_bar,style={'display':'inline-block','width':'50%'}),
        dcc.Graph(figure=surgery_by_hist_scatter,style={'display':'inline-block','width':'50%'})
    ]),
    html.P('It seems that Lumpectomy is the major surgery in the histology types (Lobular and Ductal) beside other surgeries and the most surgery in Mucinous is Simple Mastectomy', id="par1"),

])
@app.callback(
    Output("tumor_box","figure"),
    [Input("slider-year","value")]
)
def select_year(year):
    filtered_df = df[df['Year_of_Surgery'] == year]
    age_gender_counts = filtered_df.groupby(['Gender', 'Age', 'Tumor_Stage_Numeric'])['Patient_ID'].count().reset_index()
    tumor_stage_box = px.box(
    age_gender_counts,
    x='Gender',
    y='Age',
    color='Tumor_Stage_Numeric',
    labels={'Age': 'Age', 'Gender': 'Gender'},
    hover_data=['Tumor_Stage_Numeric']
    )
    tumor_stage_box.update_layout(
                                xaxis=dict(showgrid=False),
                                yaxis=dict(showgrid=False),
                                plot_bgcolor='rgb(242,242,242)',
                                paper_bgcolor='rgb(242,242,242)')
    return tumor_stage_box
if __name__ == '__main__':
    app.run_server(debug=True)