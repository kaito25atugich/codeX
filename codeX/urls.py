from django.urls import path

from . import views

app_name='codeX'
urlpatterns = [
    path('', views.Top.as_view(), name="top"),
    path('edit/<int:pk>/', views.Edit.as_view(), name='edit'),
    path('update/<int:pk>/', views.Update.as_view(), name='update'),
    path('update_page/<int:pk>/<int:mod_id>/<str:mod>/', views.update_page, name='update_page'),
    path('delete/<int:pk>/<int:mod_id>/<str:mod>/', views.delete, name='delete'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('update_profile/<int:pk>/', views.UpdateProfile.as_view(), name='update_profile'),
    path('login/',views.LoginPage.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('password_change/', views.PasswordChange.as_view(), name='change_password'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='change_password_done'),
    path('password_reset/', views.PasswordReset.as_view(), name='reset_password'), 
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='reset_password_done'), 
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='reset_password_confirm'), 
    path('reset/done/', views.PasswordResetComplete.as_view(), name='reset_password_complete'), 
]