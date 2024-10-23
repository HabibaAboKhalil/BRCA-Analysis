import pandas as pd
import numpy as np

# Set a random seed for reproducibility
np.random.seed(42)

# Number of rows to generate
num_rows = 1000

# Generate synthetic data
ages = np.random.randint(30, 90, size=num_rows)

# Simulate Tumour Stage based on Age (Older patients may have advanced stages)
tumour_stage_choices = ['Stage I', 'Stage II', 'Stage III']
tumour_stages = np.where(ages < 50, np.random.choice(tumour_stage_choices[:2], size=num_rows),
                         np.random.choice(tumour_stage_choices, size=num_rows, p=[0.1, 0.3, 0.6]))

# Simulate Histology based on Tumour Stage (Certain histologies may be more prevalent)
histology_choices = ['Invasive Ductal Carcinoma', 'Invasive Lobular Carcinoma', 'Other']
histologies = np.where(tumour_stages == 'Stage III', np.random.choice(histology_choices[:2], size=num_rows),
                       np.random.choice(histology_choices, size=num_rows))

# Generate other categorical data
er_status = np.random.choice(['Positive', 'Negative'], size=num_rows, p=[0.7, 0.3])  # 70% ER+
pr_status = np.random.choice(['Positive', 'Negative'], size=num_rows, p=[0.6, 0.4])  # 60% PR+
her2_status = np.random.choice(['Positive', 'Negative'], size=num_rows, p=[0.2, 0.8])  # 20% HER2+

# Surgery type depending on Tumour Stage (advanced stages may have different surgery types)
surgery_types = np.where(tumour_stages == 'Stage III',
                         np.random.choice(['Modified Radical Mastectomy', 'Chemotherapy'], size=num_rows),
                         np.random.choice(['Lumpectomy', 'Modified Radical Mastectomy'], size=num_rows))

# Generate realistic protein levels
protein_1 = np.random.normal(loc=1.5, scale=0.5, size=num_rows).clip(0, 3)
protein_2 = np.random.normal(loc=1.0, scale=0.5, size=num_rows).clip(0, 3)
protein_3 = np.random.normal(loc=0.8, scale=0.4, size=num_rows).clip(0, 3)
protein_4 = np.random.normal(loc=0.6, scale=0.3, size=num_rows).clip(0, 3)

# Generate dates
dates_of_surgery = pd.date_range(start='2010-01-01', periods=num_rows, freq='D')
dates_of_last_visit = dates_of_surgery + pd.to_timedelta(np.random.randint(0, 365, size=num_rows), unit='D')

# Patient status based on ER and PR status
patient_status = np.where((er_status == 'Negative') & (pr_status == 'Negative'), 
                          np.random.choice(['Alive', 'Dead'], size=num_rows, p=[0.4, 0.6]), 
                          np.random.choice(['Alive', 'Dead'], size=num_rows, p=[0.9, 0.1]))

# Create DataFrame
df = pd.DataFrame({
    'Patient_ID': range(1, num_rows + 1),
    'Age': ages,
    'Tumour_Stage': tumour_stages,
    'Histology': histologies,
    'ER status': er_status,
    'PR status': pr_status,
    'HER2 status': her2_status,
    'Surgery_type': surgery_types,
    'Protein_1': protein_1,
    'Protein_2': protein_2,
    'Protein_3': protein_3,
    'Protein_4': protein_4,
    'Date_of_Surgery': dates_of_surgery,
    'Date_of_Last_Visit': dates_of_last_visit,
    'Patient_Status': patient_status
})

# Replacing the Patient_Status with numerical values (for the model)
df['Patient_Status'] = df['Patient_Status'].map({'Alive': 1, 'Dead': 0})

# Save to CSV
df.to_csv('Synthetic_Breast_Cancer_Data_Realistic.csv', index=False)

print("Realistic synthetic dataset generated and saved as 'Synthetic_Breast_Cancer_Data_Realistic.csv'.")
