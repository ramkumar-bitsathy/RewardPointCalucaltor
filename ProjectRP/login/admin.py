from django.contrib import admin
from .models import reviewer,Marks,team_admin
# Register your models here.

admin.site.register(reviewer)
admin.site.register(team_admin)
admin.site.register(Marks)
