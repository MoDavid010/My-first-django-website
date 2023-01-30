from django.urls import path, reverse
from . import views

app_name = 'core'

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='core/login.html'), name="login"),
    path('register/', views.SignupView.as_view(), name="register"),
    path('logout/', views.logout_view, name="logout"),
    path('<int:user_id>/', views.ProfileView.as_view(), name="profile"),
    path('<int:user_id>/add_remove_friend/', views.AddRemoveFriend.as_view(), name="add_remove_friend"),
    path('<int:user_id>/edit/', views.ProfileEditView.as_view(), name="profile_edit"),
]