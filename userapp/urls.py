from django.urls import path

from userapp import views

urlpatterns = [
    path("user/", views.user),
    path("users/", views.UserView.as_view()),
    path("users/<str:pk>/", views.UserView.as_view()),

    path("students/", views.StudentView.as_view()),
    path("students/<str:pk>/", views.StudentView.as_view()),

    path("employees/", views.EmployeeAPIView.as_view()),
    path("employees/<str:id>/", views.EmployeeAPIView.as_view()),

]
