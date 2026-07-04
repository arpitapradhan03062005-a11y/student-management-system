
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('dashboard/', views.home, name="dashboard"),

    path('register/', views.register, name="register"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),

    path('profile/', views.profile, name="profile"),
    path('contact/', views.contact, name="contact"),

    path('add_student/', views.add_student, name="add_student"),
    path('view_student/', views.view_student, name="view_student"),

    path('update_student/<int:id>/', views.update_student, name="update_student"),
    path('delete_student/<int:id>/', views.delete_student, name="delete_student"),

    path('student/<int:id>/', views.student_detail, name="student_detail"),

    path('student/<int:id>/id-card/', views.student_id_card, name='student_id_card'),

    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('results/enter/', views.enter_marks, name='enter_marks'),
]