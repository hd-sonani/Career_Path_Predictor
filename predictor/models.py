from django.db import models
from django.contrib.auth.models import User

class Career(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    salary = models.CharField(max_length=100) # e.g., "$80,000 - $120,000"
    skills = models.TextField() # Comma separated list of key skills
    work_type = models.CharField(max_length=100, default='Hybrid') # Remote, On-site, Hybrid
    
    def __str__(self):
        return self.name

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    input_data = models.JSONField() # Store the submitted features
    result = models.JSONField() # Store top N predictions and probabilities
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Prediction for {self.user.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
