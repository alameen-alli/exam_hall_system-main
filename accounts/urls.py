from django.urls import path
from .views import (StudentSignUpView, InvigilatorSignUpView, 
                    CustomLoginView, StudentProfileView, 
                    ChooseSignUpView, InvigilatorProfileView,
                    ProfileView, logout_view)

app_name = 'accounts'

urlpatterns = [
    path('signup/', ChooseSignUpView.as_view(), name='signup'),
    path('logout/now/', logout_view, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('signup/student/', StudentSignUpView.as_view(), name='student_signup'),
    path('signup/invigilator/', InvigilatorSignUpView.as_view(), name='invigilator_signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('student/<slug:slug>/', StudentProfileView.as_view(), name='student_profile'),
    path('invigilator/<slug:slug>/', InvigilatorProfileView.as_view(), name='invigilator_profile'),
    
]

