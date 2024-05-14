from django.db import models

# Create your models here.
class reviewer(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    
class team_admin(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class PID(models.Model):
    PID = models.CharField(max_length=10)
    Student_Name = models.CharField(max_length=30)
    Student_RollNo = models.CharField(max_length=15)
    Project_Name = models.CharField(max_length=100)
    
class Marks(PID):
    Initial_submission = models.IntegerField(default=0)
    Final_submission = models.IntegerField(default=0)
    Plagiarism = models.IntegerField(default=0)
    Reviewer_Mark = models.FloatField(default=0)
    Team_communication_mark = models.FloatField(default=0)
    Worklog = models.IntegerField(default=0)
