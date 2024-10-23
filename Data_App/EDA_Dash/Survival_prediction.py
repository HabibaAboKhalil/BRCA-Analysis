from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
df = pd.read_csv("EDA/Cleaned_BRCA.csv")
df = df[df['Patient_Status']!='Unknown']
df= df.drop(columns=['Date_of_Surgery','Date_of_Last_Visit','Patient_ID'])
# Preprocessing
# Encode categorical columns
label_encoders = {}
categorical_cols = ['Gender', 'ER status', 'PR status', 'HER2 status', 'Histology', 'Surgery_type', 'Patient_Status']

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le  # Save encoder to reverse later if needed

# Prepare df for Model 1: Predict Patient_Status (Alive or Dead)
X_1 = df[['Age', 'Gender', 'Protein1', 'Protein2', 'Protein3', 'Protein4', 'ER status', 'PR status', 'HER2 status']]
y_1 = df['Patient_Status']

# Split the data for model 1
X_train_1, X_test_1, y_train_1, y_test_1 = train_test_split(X_1, y_1, test_size=0.2, random_state=42)
smote = SMOTE(n_jobs=-1,random_state=42)
X_resample_1,Y_resample_1 = smote.fit_resample(X_train_1,y_train_1)
# Train a Random Forest for Model 1
model_1 = XGBClassifier(learning_rate=1.0,max_depth=6,n_estimators=150,random_state=42)
model_1.fit(X_resample_1,Y_resample_1)
y_pred_1 = model_1.predict(X_test_1)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create layout
app.layout = dbc.Container([
    html.H1("Breast Cancer Prediction App"),
    
    # Input fields
    dbc.Row([
        dbc.Col(dbc.Input(id='age', type='number', placeholder='Age', min=0), width=3),
        dbc.Col(dcc.Dropdown(
            id='gender',
            options=[{'label': 'Female', 'value': 0}, {'label': 'Male', 'value': 1}],
            placeholder='Select Gender'
        ), width=3),
        dbc.Col(dbc.Input(id='protein1', type='number', placeholder='Protein1'), width=3),
        dbc.Col(dbc.Input(id='protein2', type='number', placeholder='Protein2'), width=3),
    ]),
    
    dbc.Row([
        dbc.Col(dbc.Input(id='protein3', type='number', placeholder='Protein3'), width=3),
        dbc.Col(dbc.Input(id='protein4', type='number', placeholder='Protein4'), width=3),
        dbc.Col(dcc.Dropdown(
            id='er_status',
            options=[{'label': 'Positive', 'value': 1}, {'label': 'Negative', 'value': 0}],
            placeholder='Select ER status'
        ), width=3),
        dbc.Col(dcc.Dropdown(
            id='pr_status',
            options=[{'label': 'Positive', 'value': 1}, {'label': 'Negative', 'value': 0}],
            placeholder='Select PR status'
        ), width=3),
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='her2_status',
            options=[{'label': 'Positive', 'value': 1}, {'label': 'Negative', 'value': 0}],
            placeholder='Select HER2 status'
        ), width=3),
    ]),
    
    # Button to predict
    dbc.Button('Predict', id='predict-btn', color='primary', className='mt-3'),
    
    # Output results
    html.Div(id='prediction-output', className='mt-4')
])

# Callback to make predictions
@app.callback(
    Output('prediction-output', 'children'),
    Input('predict-btn', 'n_clicks'),
    [Input('age', 'value'), Input('gender', 'value'), Input('protein1', 'value'),
     Input('protein2', 'value'), Input('protein3', 'value'), Input('protein4', 'value'),
     Input('er_status', 'value'), Input('pr_status', 'value'), Input('her2_status', 'value')]
)
def make_predictions(n_clicks, age, gender, protein1, protein2, protein3, protein4, er_status, pr_status, her2_status):
    if n_clicks is None:
        return ""
    
    # Prepare input for prediction
    features = np.array([[age, gender, protein1, protein2, protein3, protein4, er_status, pr_status, her2_status]])
    
    # Predict patient status (Alive or Dead) using Model 1
    status_pred = model_1.predict(features)[0]
    status = 'Alive' if status_pred == 1 else 'Dead' 
    # Display predictions
    return html.Div([
        html.H4(f'Patient Status: {status}')
    ])

# If running the script directly, start the app
if __name__ == '__main__':
    app.run_server(debug=False)

