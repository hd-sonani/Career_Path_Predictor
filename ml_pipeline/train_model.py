import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import joblib
import os
import random

# Define features
skill_cols = [
    'Python', 'Java', 'C++', 'JavaScript', 'SQL', 'DataAnalysis',
    'GraphicDesign', 'UIUX', 'VideoEditing', 'Animation', 'Photography',
    'Communication', 'Management', 'Marketing', 'Sales',
    'ProblemSolving', 'CriticalThinking', 'Leadership', 'Teamwork', 'Creativity'
]
interest_categories = ['Technology', 'Creative', 'Business', 'Finance', 'Education', 'Social', 'Government']
subject_cols = ['Math', 'Science', 'Computer', 'English', 'Business', 'Economics', 'Accounts', 'Arts', 'Psychology']

careers = [
    "Software Engineer", "Data Scientist", "UX/UI Designer", "Financial Analyst", 
    "Marketing Manager", "Teacher", "Graphic Designer", "Video Editor", 
    "Sales Manager", "Database Administrator", "HR Manager", 
    "Content Writer", "Business Analyst", "Project Manager", "Game Developer"
]

def generate_synthetic_data(num_samples=2000):
    data = []
    
    for _ in range(num_samples):
        # Pick a target career first to bias the features appropriately
        target_career = random.choice(careers)
        
        # Base stats
        skills = {skill: random.randint(0, 5) for skill in skill_cols}
        subjects = {subj: 0 for subj in subject_cols}
        interest = random.choice(interest_categories)
        edu_level = random.randint(2, 5)
        salary_pref = random.randint(0, 2)
        work_pref = random.randint(0, 2) # 0: Remote, 1: Hybrid, 2: On-site
        
        # Bias features based on career to make the model learn logic
        if target_career == "Software Engineer":
            skills['Python'] = random.randint(3, 5)
            skills['Java'] = random.randint(3, 5)
            skills['JavaScript'] = random.randint(3, 5)
            skills['ProblemSolving'] = random.randint(4, 5)
            subjects['Computer'] = 1
            subjects['Math'] = 1
            interest = 'Technology'
            
        elif target_career == "Data Scientist":
            skills['Python'] = random.randint(4, 5)
            skills['DataAnalysis'] = random.randint(4, 5)
            skills['SQL'] = random.randint(3, 5)
            subjects['Math'] = 1
            subjects['Science'] = 1
            interest = 'Technology'
            
        elif target_career == "UX/UI Designer":
            skills['UIUX'] = random.randint(4, 5)
            skills['GraphicDesign'] = random.randint(3, 5)
            skills['Creativity'] = random.randint(4, 5)
            subjects['Arts'] = 1
            interest = 'Creative'
            
        elif target_career == "Financial Analyst":
            skills['DataAnalysis'] = random.randint(3, 5)
            skills['CriticalThinking'] = random.randint(4, 5)
            subjects['Math'] = 1
            subjects['Economics'] = 1
            subjects['Accounts'] = 1
            interest = 'Finance'
            
        elif target_career == "Marketing Manager":
            skills['Marketing'] = random.randint(4, 5)
            skills['Communication'] = random.randint(4, 5)
            skills['Leadership'] = random.randint(3, 5)
            subjects['Business'] = 1
            interest = 'Business'
            
        elif target_career == "Teacher":
            skills['Communication'] = random.randint(4, 5)
            skills['Leadership'] = random.randint(3, 5)
            skills['ProblemSolving'] = random.randint(3, 5)
            subjects['English'] = 1
            subjects['Psychology'] = random.choice([0, 1])
            interest = 'Education'
            
        elif target_career == "Graphic Designer":
            skills['GraphicDesign'] = random.randint(4, 5)
            skills['Creativity'] = random.randint(4, 5)
            subjects['Arts'] = 1
            interest = 'Creative'
            
        elif target_career == "Video Editor":
            skills['VideoEditing'] = random.randint(4, 5)
            skills['Creativity'] = random.randint(3, 5)
            interest = 'Creative'
            
        elif target_career == "Sales Manager":
            skills['Sales'] = random.randint(4, 5)
            skills['Communication'] = random.randint(4, 5)
            skills['Management'] = random.randint(3, 5)
            subjects['Business'] = 1
            interest = 'Business'
            
        elif target_career == "Database Administrator":
            skills['SQL'] = random.randint(4, 5)
            skills['Python'] = random.randint(2, 5)
            subjects['Computer'] = 1
            interest = 'Technology'
            
        elif target_career == "HR Manager":
            skills['Management'] = random.randint(3, 5)
            skills['Communication'] = random.randint(4, 5)
            skills['Teamwork'] = random.randint(4, 5)
            subjects['Psychology'] = 1
            subjects['Business'] = 1
            interest = 'Social'
            
        elif target_career == "Content Writer":
            skills['Communication'] = random.randint(4, 5)
            skills['Creativity'] = random.randint(3, 5)
            subjects['English'] = 1
            interest = 'Creative'
            
        elif target_career == "Business Analyst":
            skills['DataAnalysis'] = random.randint(3, 5)
            skills['Management'] = random.randint(3, 5)
            skills['Communication'] = random.randint(3, 5)
            subjects['Business'] = 1
            subjects['Computer'] = 1
            interest = 'Business'
            
        elif target_career == "Project Manager":
            skills['Management'] = random.randint(4, 5)
            skills['Leadership'] = random.randint(4, 5)
            skills['ProblemSolving'] = random.randint(4, 5)
            subjects['Business'] = 1
            interest = 'Business'
            
        elif target_career == "Game Developer":
            skills['C++'] = random.randint(4, 5)
            skills['Python'] = random.randint(2, 4)
            skills['ProblemSolving'] = random.randint(4, 5)
            subjects['Computer'] = 1
            subjects['Math'] = 1
            interest = 'Technology'

        row = {**skills, **subjects}
        row['Interest'] = interest
        row['EducationLevel'] = edu_level
        row['SalaryPreference'] = salary_pref
        row['WorkPreference'] = work_pref
        row['Target'] = target_career
        
        data.append(row)
        
    return pd.DataFrame(data)

def main():
    print("Generating synthetic dataset...")
    df = generate_synthetic_data(2500)
    
    # Save dataset to CSV for reference
    os.makedirs('ml_pipeline', exist_ok=True)
    df.to_csv('ml_pipeline/dataset.csv', index=False)
    
    X = df.drop('Target', axis=1)
    y = df['Target']
    
    numeric_features = skill_cols + subject_cols + ['EducationLevel', 'SalaryPreference', 'WorkPreference']
    categorical_features = ['Interest']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    print("Training model...")
    model.fit(X, y)
    
    # Evaluate
    score = model.score(X, y)
    print(f"Model accuracy on training set: {score:.2f}")
    
    print("Saving model...")
    joblib.dump(model, 'ml_pipeline/model.pkl')
    print("Model saved to ml_pipeline/model.pkl successfully!")

if __name__ == '__main__':
    main()
