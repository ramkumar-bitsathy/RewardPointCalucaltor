from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
# Create your models here.
class reviewer(models.Model):
    reviewer_name = models.CharField(max_length=100,default=None)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100,default=None)
    
class team_admin(models.Model):
    admin_name = models.CharField(max_length=100,default=None)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class PID(models.Model):
    PID = models.CharField(max_length=10)
    Student_Name = models.CharField(max_length=30)
    Student_RollNo = models.CharField(max_length=15)
    Project_Name = models.CharField(max_length=100)
    
    
class Marks(PID):
    Initial_submission = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)])
    Final_submission = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(10)])
    Plagiarism = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(10)])
    Reviewer_Mark = models.FloatField(default=-1,validators=[MinValueValidator(-1), MaxValueValidator(60)])
    Team_communication_mark = models.FloatField(default=-1,validators=[MinValueValidator(-1), MaxValueValidator(10)])
    Worklog = models.IntegerField(default=0 ,validators=[MinValueValidator(0), MaxValueValidator(5)])
    Total = models.FloatField(default=-1,validators=[MinValueValidator(-1), MaxValueValidator(100)])
