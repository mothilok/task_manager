from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('project/', views.project, name='project'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('registration/', views.registration, name='registration'),
    path('select_project/', views.select_project, name='select_project'),
    path('manage_projects/', views.manage_projects, name='manage_projects'),
    #path('<int:project_id>/', views.project, name='project'),
    path('project_user/', views.project_user, name='project_user'),
    path('group/', views.group, name='group'),
    path('user_group/', views.user_group, name='user_group'),
    path('board/', views.board, name='board'),
    path('board_user/', views.board_user, name='board_user'),
    path('task/', views.task, name='task'),
    path('show_task_<int:show_task_id>/', views.show_task, name='show_task'),
    path('display_user_tasks/', views.display_user_tasks, name='display_user_tasks'),



]