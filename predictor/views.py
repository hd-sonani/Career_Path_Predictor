from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Career, Prediction
import json
import joblib
import pandas as pd
import os
from django.conf import settings

# Load ML model
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_pipeline', 'model.pkl')
try:
    ml_model = joblib.load(MODEL_PATH)
except Exception as e:
    ml_model = None
    print("Warning: Model not found. Please train the model first.")

def home(request):
    return render(request, 'predictor/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('wizard')
    else:
        form = UserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('wizard')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def wizard_view(request):
    if request.method == 'POST':
        # Extract features from POST request
        # The form will be JS-based, we'll parse JSON or standard POST data
        try:
            data = json.loads(request.body)
            skills = data.get('skills', {})
            subjects = data.get('subjects', [])
            interest = data.get('interest', 'Technology')
            edu_level = int(data.get('education_level', 3))
            salary_pref = int(data.get('salary_preference', 1))
            work_pref = int(data.get('work_preference', 1))
            
            # Prepare row for pandas
            row = {}
            skill_cols = [
                'Python', 'Java', 'C++', 'JavaScript', 'SQL', 'DataAnalysis',
                'GraphicDesign', 'UIUX', 'VideoEditing', 'Animation', 'Photography',
                'Communication', 'Management', 'Marketing', 'Sales',
                'ProblemSolving', 'CriticalThinking', 'Leadership', 'Teamwork', 'Creativity'
            ]
            for sc in skill_cols:
                row[sc] = int(skills.get(sc, 0))
                
            subject_cols = ['Math', 'Science', 'Computer', 'English', 'Business', 'Economics', 'Accounts', 'Arts', 'Psychology']
            for sc in subject_cols:
                row[sc] = 1 if sc in subjects else 0
                
            row['Interest'] = interest
            row['EducationLevel'] = edu_level
            row['SalaryPreference'] = salary_pref
            row['WorkPreference'] = work_pref
            
            df = pd.DataFrame([row])
            
            # Predict
            if ml_model:
                probabilities = ml_model.predict_proba(df)[0]
                classes = ml_model.classes_
                
                # Zip and sort top 3
                pred_probs = list(zip(classes, probabilities))
                pred_probs.sort(key=lambda x: x[1], reverse=True)
                top_3 = pred_probs[:3]
                
                result_data = [{"career": c, "probability": float(p)} for c, p in top_3]
            else:
                result_data = [{"career": "Software Engineer", "probability": 0.85}] # Fallback
            
            # Save Prediction
            prediction = Prediction.objects.create(
                user=request.user,
                input_data=data,
                result=result_data
            )
            return redirect('result', prediction_id=prediction.id)
            
        except Exception as e:
            return render(request, 'predictor/wizard.html', {'error': str(e)})
            
    return render(request, 'predictor/wizard.html')

@login_required
def result_view(request, prediction_id):
    prediction = get_object_or_404(Prediction, id=prediction_id, user=request.user)
    
    # Smart suggestion logic
    skills = prediction.input_data.get('skills', {})
    total_skill_score = sum(int(v) for v in skills.values())
    salary_pref = int(prediction.input_data.get('salary_preference', 1))
    
    warning_message = None
    if salary_pref == 2 and total_skill_score < 40: # threshold of 40 out of 100 max (20 * 5)
        warning_message = "Improve your skills to match your high salary expectations and secure better career options."
    
    # Ensure careers exist in DB so we can link to them
    for res in prediction.result[:3]:
        career_name = res['career']
        if not Career.objects.filter(name=career_name).exists():
            Career.objects.create(
                name=career_name,
                description=f"A professional in the field of {career_name}.",
                salary="$70,000 - $100,000",
                skills="Problem Solving, Communication"
            )
            
    # Load career objects for the view
    top_careers = []
    for res in prediction.result[:3]:
        c = Career.objects.filter(name=res['career']).first()
        top_careers.append({
            'career_obj': c,
            'probability': res['probability'],
            'prob_percent': int(res['probability'] * 100)
        })
        
    context = {
        'prediction': prediction,
        'top_careers': top_careers,
        'warning_message': warning_message,
        'total_skill_score': total_skill_score
    }
    return render(request, 'predictor/result.html', context)

@login_required
def history_view(request):
    predictions = Prediction.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'predictor/history.html', {'predictions': predictions})

@login_required
def career_detail(request, career_id):
    career = get_object_or_404(Career, id=career_id)
    return render(request, 'predictor/career_detail.html', {'career': career})

@login_required
def compare_view(request):
    career_ids = request.GET.getlist('careers')
    careers = Career.objects.filter(id__in=career_ids)
    return render(request, 'predictor/compare.html', {'careers': careers})

@login_required
def roadmap_view(request, career_id):
    career = get_object_or_404(Career, id=career_id)
    # Simple static roadmap logic based on career name
    steps = [
        {"title": "Learn the Basics", "desc": f"Master fundamental concepts required for {career.name}."},
        {"title": "Build Projects", "desc": "Apply your knowledge by building 2-3 portfolio projects."},
        {"title": "Networking & Certifications", "desc": "Connect with professionals and get certified in key skills."},
        {"title": "Apply for Jobs", "desc": "Prepare your resume, practice interviews, and start applying."}
    ]
    return render(request, 'predictor/roadmap.html', {'career': career, 'steps': steps})
