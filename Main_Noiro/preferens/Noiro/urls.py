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
    path('display_groups/', views.display_groups, name='display_groups'),
    path('group_id_<int:show_group_id>/', views.group, name='show_group'),
    path('board/', views.board, name='board'),
    path('board_user/', views.board_user, name='board_user'),
    path('display_boards/', views.display_boards, name='display_boards'),
    path('task/', views.task, name='task'),
    path('display_tasks/', views.display_tasks, name='display_tasks'),
    path('show_task_<int:show_task_id>/', views.show_task, name='show_task'),



]