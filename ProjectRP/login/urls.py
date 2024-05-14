from django.urls import path,include
from .views import login_view,admin_page,reviewer_page,helloworld,create_review

urlpatterns = [
    path('',login_view,name='login'),
    path('admin_page/',admin_page),
    path('helloworld/',helloworld),
    path('reviewer_page/',reviewer_page),
    path('create_review/',create_review)
]