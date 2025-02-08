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
            curent_project = models.Project_db(name=name, user_created=request.user)
            curent_project.save()
            role = models.Project_role_db.objects.get(id=1)
            models.Project_user_db(project_id=curent_project, user_id=request.user, role_id=role).save()

            context = {'successfully':'successfully'}
            return render(request, 'noiro/project.html',context=context)

    else:
        return redirect('login')
    return render(request, 'noiro/project.html')


def delite_project(request):
    return HttpResponse('<h1>twerydgkhu</h1>')


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
                if request.POST['mod'] == 'select_project':
                    models.Custom_user.objects.filter(username=request.user).update(project_active=None)
                    return redirect('select_project')


                elif request.POST['mod'] == 'group':
                    context = {'select': 'group'}

                elif request.POST['mod'] == 'create_group':
                    return redirect('group')
                elif request.POST['mod'] == 'add_user_group':
                    return redirect('user_group')
                elif request.POST['mod'] == 'display_groups':
                    return redirect('display_groups')
                elif request.POST['mod'] == 'delite_group':
                    return redirect('delite_group')


                elif request.POST['mod'] == 'board':
                    context = {'select': 'board'}

                elif request.POST['mod'] == 'create_board':
                    return redirect('board')
                elif request.POST['mod'] == 'add_board_user':
                    return redirect('board_user')
                elif request.POST['mod'] == 'display_boards':
                    return redirect('display_boards')


                elif request.POST['mod'] == 'task':
                    context={'select':'task'}

                elif request.POST['mod'] == 'create_task':
                    return redirect('task')
                elif request.POST['mod'] == 'display_tasks':
                    return redirect('display_tasks')


                context['curent_project'] = request.user.project_active
                return render(request, 'noiro/manage_projects.html', context=context)


        curent_project = request.user.project_active
        data = {'curent_project':curent_project}
        return render(request, 'noiro/manage_projects.html', context=data)
    else:
        return redirect('login')


def select_project(request):
    if request.user.is_authenticated:
        if request.POST:
            models.Custom_user.objects.filter(id=request.user.id).update(project_active=request.POST['curent_project'])
            return redirect('manage_projects')
        else:

            projects_user = models.Project_user_db.objects.filter(user_id=request.user.id)
            context = {
                'projects_user':projects_user
            }
            return render(request, 'noiro/select_project.html', context=context)
    else:
        return redirect('login')

def group(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            if request.POST:
                models.Group_db(name=request.POST['name_group'],
                                project_id=request.user.project_active).save()

                return render(request, 'noiro/group.html')
        else:
            return redirect('login')
        return render(request, 'noiro/group.html')
    else:
        return redirect('login')


def display_groups(request):
    if request.user.is_authenticated:
        if request.POST:
            id_group = request.POST['group']
            return show_group(request, show_group_id=id_group)
        else:
            project_role = models.Project_user_db.objects.get(project_id=request.user.project_active,
                                                              user_id=request.user).role_id
            if project_role.roles == 'creator' or project_role.roles == 'super_admin':
                groups = models.Group_db.objects.filter(project_id=request.user.project_active)
                context = {'groups': groups}

            else:
                user_groups = models.User_groups_db.objects.filter(user_id=request.user,
                                                              project_id=request.user.project_active).values_list('group_id', flat=True)
                group_list = []
                for group in user_groups:
                    groups = models.Group_db.objects.get(id=group)
                    group_list.append(groups)
                context = {'groups':group_list}

            return render(request, 'noiro/display_groups.html', context=context)

    else:
        return redirect('login')

# все пошло по пизде уже давно
def show_group(request, show_group_id):
    if request.user.is_authenticated:
        if request.POST:
            print('IN POSRT')
        group = models.Group_db.objects.get(id=show_group_id)
        users = models.User_groups_db.objects.filter(group_id=group, project_id=request.user.project_active)
        context = {"group":group, 'users':users}
        return render(request, 'noiro/show_group.html', context=context)
    else:
        return redirect('login')


def user_group(request):
    if request.user.is_authenticated:
        if request.POST:
            group_id = models.Group_db.objects.get(name=request.POST['group_name'],
                                                   project_id=request.user.project_active)
            user_id = models.Custom_user.objects.get(username=request.POST['username'])
            check_user_db = models.User_groups_db.objects.filter(user_id=user_id,
                                                                 group_id=group_id,
                                                                 project_id=request.user.project_active)
            # проверка записи в User_groups
            if not check_user_db:
                models.User_groups_db(user_id=user_id,
                                      group_id=group_id,
                                      project_id=request.user.project_active).save()
                role_id = models.Project_role_db.objects.get(id=4)
                ceheck_proj_user = models.Project_user_db.objects.filter(project_id=request.user.project_active,
                                                                         user_id=user_id)
                # проверка есть ли запись в project_user
                if not ceheck_proj_user:
                    models.Project_user_db(project_id=request.user.project_active,
                                           user_id=user_id,
                                           role_id=role_id).save()

        all_group = models.Group_db.objects.filter(project_id=request.user.project_active)
        context = {'all_group':all_group}

        return render(request, 'noiro/user_group.html', context=context)
    else:
        return redirect('login')


def delite_group(request, group_id):
    print('awdwdwadwadwdwadawdwadwadwadwadwaaadawdwaddaw')
    return HttpResponse('<h1>awddaadwdawdawdwda</h1>')

def board(request):
    if request.user.is_authenticated:
        if request.POST:

            check_board = models.Board_db.objects.filter(name=request.POST['name'],
                                                         project_id=request.user.project_active)
            if not check_board:

                name = request.POST['name']
                project_id = request.user.project_active
                user_created = request.user

                models.Board_db(name=name,
                                project_id=project_id,
                                user_created=user_created).save()
        return render(request, 'noiro/board.html')
    else:
        return redirect('login')

def board_user(request):
    if request.user.is_authenticated:
        if request.POST:
            # сделать проверку есть авторизованы ли юзеры
            board_id = models.Board_db.objects.get(name=request.POST['board_name'])
            role_id = models.Project_role_db.objects.get(roles=request.POST['role'])
            # НЕ РАБОТАЕТ
            if request.POST['group_name'] == '':
                group_name = False
            else:
                group_name = request.POST['group_name']
            # проверка есть ли группа в посте
            if request.POST['username'] and not group_name:
                user_id = models.Custom_user.objects.get(username=request.POST['username'])
                project_id = request.user.project_active
                check_user_board = models.Board_user_db.objects.filter(board_id=board_id,
                                                                       user_id=user_id,
                                                                       project_id=project_id
                                                                       )
                if not check_user_board.exists():

                    models.Board_user_db(board_id=board_id,
                                         user_id=user_id,
                                         role_id=role_id,
                                         project_id=project_id).save()
                    ceheck_proj_user = models.Project_user_db.objects.filter(project_id=request.user.project_active,
                                                                             user_id=user_id)
                    if not ceheck_proj_user.exists():
                        models.Project_user_db(project_id=request.user.project_active,
                                               user_id=user_id,
                                               role_id=role_id,).save()

            elif not request.POST['username'] and group_name:
                group_id = models.Group_db.objects.get(project_id=request.user.project_active,
                                                       name=request.POST['group_name']).id

                users_group = models.User_groups_db.objects.filter(group_id=group_id)
                users_board = models.Board_user_db.objects.filter(board_id=board_id,
                                                                  project_id=request.user.project_active)

                users_group_only_user_id = users_group.values_list('user_id', flat=True)
                users_board_only_user_id = users_board.values_list('user_id', flat=True)

                new_users = users_group_only_user_id.difference(users_board_only_user_id)

                if new_users.exists():
                    for user in new_users:
                        instance_user = models.Custom_user.objects.get(id=user)
                        models.Board_user_db(board_id=board_id,
                                             user_id=instance_user,
                                             role_id=role_id,
                                             project_id=request.user.project_active).save()

        boards = models.Board_db.objects.filter(project_id=request.user.project_active)
        roles = models.Project_role_db.objects.order_by('-id')
        groups = models.Group_db.objects.filter(project_id=request.user.project_active)

        context = {
            'boards':boards,
            'roles':roles,
            'groups':groups
        }
        return render(request, 'noiro/board_user.html', context=context)
    else:
        return redirect('login')


def display_boards(request):
    if request.user.is_authenticated:
        if request.POST:
            id_board = request.POST['board']
            return show_board(request, board_id=id_board)
        else:
            project_role = models.Project_user_db.objects.get(project_id=request.user.project_active,
                                                              user_id=request.user).role_id
            if project_role.roles == 'creator' or project_role.roles == 'super_admin':
                boards = models.Board_db.objects.filter(project_id=request.user.project_active)
                context = {'boards': boards}
            else:
                user_boards = models.Board_user_db.objects.filter(user_id=request.user,
                                                             project_id=request.user.project_active).values_list('board_id', flat=True)
                board_list = []
                for board in user_boards:
                    boards = models.Board_db.objects.get(id=board, project_id=request.user.project_active)
                    board_list.append(boards)
                print(board_list)
                context = {'boards':board_list}

            return render(request, 'noiro/display_boards.html', context=context)
    else:
        return redirect('login')


def show_board(request, board_id):
    if request.user.is_authenticated:
        board = models.Board_db.objects.get(id=board_id, project_id=request.user.project_active)
        users = models.Board_user_db.objects.filter(board_id=board_id, project_id=request.user.project_active)
        context = {'board':board, 'users':users}
        return render(request, 'noiro/show_board.html', context=context)
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
            else:
                user_id = None

            task_status = models.Task_status_db.objects.get(id=3)

            check_task = models.Task_db.objects.filter(name=name,
                               comment=comment,
                               creator=creator,
                               board_id=board_id,
                               task_status_id=task_status)

            if not check_task:
                task = models.Task_db(name=name,
                               comment=comment,
                               creator=creator,
                               board_id=board_id,
                               task_status_id=task_status,
                               project_id=request.user.project_active)
                task.save()

                if user_id:
                    models.User_task_db(user_id=user_id, task_id=task, project_id=request.user.project_active).save()

                    ceheck_proj_user = models.Project_user_db.objects.filter(project_id=request.user.project_active,
                                                                             user_id=user_id)
                    if not ceheck_proj_user.exists():
                        role_id = models.Project_role_db.objects.get(id=4)
                        models.Project_user_db(project_id=request.user.project_active,
                                               user_id=user_id,
                                               role_id=role_id).save()


        boards = models.Board_db.objects.filter(project_id=request.user.project_active)
        context = {'boards':boards}
        return render(request, 'noiro/task.html', context=context)
    else:
        return redirect('login')


def display_tasks(request):
    if request.user.is_authenticated:
        if request.POST:
            print(request.POST)
            if 'task' in request.POST:
                return show_task(request, show_task_id=request.POST['task'])
            else:
                task = models.User_task_db.objects.get(id=request.POST['task_user']).task_id.id

                return show_task(request, show_task_id=task)

        else:
            project_role = models.Project_user_db.objects.get(project_id=request.user.project_active,
                                                              user_id=request.user).role_id
            if project_role.roles == 'creator' or project_role.roles == 'super_admin':
                tasks = models.Task_db.objects.filter(project_id=request.user.project_active)
                context = {'tasks':tasks}
                return render(request, 'noiro/display_tasks.html', context=context)
            else:
                boards_id = models.Board_user_db.objects.filter(user_id=request.user,
                                                                project_id=request.user.project_active).values_list('board_id', flat=True)
                tasks_user = models.User_task_db.objects.filter(project_id=request.user.project_active,
                                                                user_id=request.user)
                print(boards_id)
                if boards_id.exists():
                    print(boards_id.exists())
                    tasks = []
                    for board_id in boards_id:
                        print(board_id)
                        try:
                            task = models.Task_db.objects.get(board_id=board_id,
                                                              project_id=request.user.project_active)
                            tasks.append(task)
                        except:
                            pass

                if boards_id.exists() and not tasks_user.exists():
                    context = {'tasks':tasks}
                    return render(request, 'noiro/display_tasks.html', context=context)

                elif tasks_user.exists() and not boards_id.exists():
                    context = {'tasks_user':tasks_user}
                    return render(request, 'noiro/display_tasks.html', context=context)

                elif tasks_user.exists() and boards_id.exists():
                    context = {'tasks':tasks, 'tasks_user': tasks_user}
                    return render(request, 'noiro/display_tasks.html', context=context)

                else:
                    return render(request, 'noiro/display_tasks.html')

    else:
        return redirect('login')


def show_task(request, show_task_id):
    if request.user.is_authenticated:
        task = models.Task_db.objects.get(id=show_task_id)
        context={'task':task}
        return render(request, 'noiro/show_task.html', context=context)
    else:
        return redirect('login')
