from django.shortcuts import render, redirect
from . import models
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout



def home(request):

    return render(request, 'noiro/home.html')


def registration(request):
    if request.POST:
        name = request.POST['username']
        password = request.POST['password']
        status = models.Status_db.objects.get(status='1')

        try:
            models.Custom_user.objects.create_user(username=name, password=password, status=status).save()
        except:
            context = {'error':'error'}
            return render(request, 'noiro/registration.html', context=context)
        login(request, authenticate(username=name, password=password))

    return render(request, 'noiro/registration.html')


def login_user(request):
    if request.POST:
        login(request, authenticate(username=request.POST['user_name'], password=request.POST['password']))
    return render(request, 'noiro/login.html')


def logout_user(request):
    logout(request)
    return render(request, 'noiro/logout.html')

def project(request):
    if request.user.is_authenticated:
        if request.POST:
            name = request.POST['name']
            curent_project = models.Project_db(name=name,user_created=request.user)
            curent_project.save()
            role = models.Project_role_db.objects.get(id=1)
            models.Project_user_db(project_id=curent_project, user_id=request.user, role_id=role).save()
            context = {'successfully':'successfully'}
            return render(request, 'noiro/project.html',context=context)

    else:
        return redirect('login')
    return render(request, 'noiro/project.html')

def project_user(request):
    if request.user.is_authenticated:
        if request.POST:
            try:
                name = int(request.POST['name'])
                user = models.Custom_user.objects.get(id=name)
            except:
                name = request.POST['name']
                user = models.Custom_user.objects.get(username=name)

            user = models.Custom_user.objects.get(id=user.id)
            project_id = request.user.project_active
            role_id = models.Project_role_db.objects.get(roles=request.POST['project_role'])
            models.Project_user_db(project_id=project_id, user_id=user, role_id=role_id).save()

        roles = models.Project_role_db.objects.order_by('-id')
        context = {'roles':roles}

    else:
        return redirect('login')
    return render(request, 'noiro/project_user.html', context=context)


def manage_projects(request):
    if request.user.is_authenticated:
        if request.user.project_active == None:
            return  redirect('select_project')
        else:

            if request.POST:
                if request.POST['menu'] == 'select_project':
                    models.Custom_user.objects.filter(username=request.user).update(project_active=None)
                    return redirect('select_project')

                elif request.POST['menu'] == 'project_user':
                    return redirect('project_user')

                elif request.POST['menu'] == 'group':
                    return redirect('group')

                elif request.POST['menu'] == 'user_group':
                    return redirect('user_group')

                elif request.POST['menu'] == 'board':
                    return redirect('board')

                elif request.POST['menu'] == 'board_user':
                    return redirect('board_user')

                elif request.POST['menu'] == 'task':
                    return redirect('task')

        curent_project = request.user.project_active
        data = {'curent_project':curent_project}
        return render(request, 'noiro/manage_projects.html', context=data)
    else:
        return redirect('login')


def select_project(request):
    if request.user.is_authenticated:
        if request.POST:
            models.Custom_user.objects.filter(id=request.user.id).update(project_active=request.POST['select_project'])
            return redirect('manage_projects')
        else:#сделать проверку на роль в проекте

            curent_project = models.Project_db.objects.filter(user_created=request.user.id)
            print(curent_project)
            context = {
                'curent_project':curent_project
            }
            return render(request, 'noiro/select_project.html', context=context)
    else:
        return redirect('login')

def group(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            if request.POST:
                models.Group_db(name=request.POST['name_group'], project_id=request.user.project_active).save()

                return render(request, 'noiro/group.html')
        else:
            return redirect('login')
        return render(request, 'noiro/group.html')
    else:
        return redirect('login')

def user_group(request):
    if request.user.is_authenticated:
        if request.POST:
            user_id = models.Custom_user.objects.get(username=request.POST['username'])
            group_id = models.Group_db.objects.get(name=request.POST['group_name'], project_id=request.user.project_active)

            models.User_groups_db(user_id=user_id, group_id=group_id).save()


        all_group = models.Group_db.objects.filter(project_id=request.user.project_active)
        context = {
            'all_group':all_group
        }
        return render(request, 'noiro/user_group.html', context=context)
    else:
        return redirect('login')

def board(request):
    if request.user.is_authenticated:
        if request.POST:
            name = request.POST['name']
            project_id = request.user.project_active
            user_created = request.user

            models.Board_db(name=name, project_id=project_id, user_created=user_created).save()
        return render(request, 'noiro/board.html')
    else:
        return redirect('login')

def board_user(request):
    if request.user.is_authenticated:
        if request.POST:
            board_id = models.Board_db.objects.get(name=request.POST['board_name'])
            user_id = models.Custom_user.objects.get(username=request.POST['username'])
            role_id = models.Project_role_db.objects.get(roles=request.POST['role'])

            models.Board_user_db(board_id=board_id, user_id=user_id, role_id=role_id).save()

        boards = models.Board_db.objects.filter(project_id=request.user.project_active)
        roles = models.Project_role_db.objects.order_by('-id')

        context = {
            'boards':boards,
            'roles':roles
        }
        return render(request, 'noiro/board_user.html', context=context)
    else:
        return redirect('login')

# drop
def add_work_category(request):
    if request.user.is_authenticated:
        if request.POST:
            models.Work_category_db(name=request.POST['name_category'], project_id=request.user.project_active).save()
        return render(request, 'noiro/add_work_category.html')
    else:
        return redirect('login')

def task(request):
    if request.user.is_authenticated:
        if request.POST:
            name = request.POST['name_task']
            comment = request.POST['comment']
            creator = request.user

            if request.POST['board_name']:
                board_id = models.Board_db.objects.get(name=request.POST['board_name'])
            else:
                board_id = None
            if request.POST['username']:
                user_id = models.Custom_user.objects.get(username=request.POST['username'])
                user_task_id = models.User_task_db(user_id=user_id)
                user_task_id.save()
            else:
                user_task_id = None

            task_status = models.Task_status_db.objects.get(id=3)

            models.Task_db(name=name, comment=comment, creator=creator, board_id=board_id, user_task_id=user_task_id, task_status_id=task_status).save()

        boards = models.Board_db.objects.filter(project_id=request.user.project_active)
        context = {'boards':boards}
        return render(request, 'noiro/task.html', context=context)
    else:
        return redirect('login')

def show_task(request, shou_task_id):
    if request.user.is_authenticated:
        task = models.Task_db.objects.get(id=shou_task_id)
        context={'task':task}
        return render(request, 'noiro/show_task.html', context=context)
    else:
        return redirect('login')


def display_user_tasks(request):
    if request.user.is_authenticated:
        group_id = models.User_groups_db.objects.get(user_id=request.user.id).group_id
        print(group_id)
        # group = models.Groups_db.objects.get()
        # task_group = models.Task_db.objects.filter()
        # task_user =
        return render(request, 'noiro/display_user_tasks.html')
    else:
        return redirect('login')


