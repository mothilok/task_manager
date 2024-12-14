from django.db import models
from django.contrib.auth.models import AbstractUser


class Status_db(models.Model):
    status = models.IntegerField()

    def __str__(self):
        return self.status


class Project_role_db(models.Model):
    roles = models.CharField(max_length=100)

    def __str__(self):
        return self.roles

class Custom_user(AbstractUser):
    status = models.ForeignKey(Status_db, null=True, on_delete=models.SET_NULL)
    project_active = models.ForeignKey('Project_db', null=True, on_delete=models.SET_NULL)# сессии


    def __str__(self):
        return self.username


class Project_db(models.Model):
    name = models.CharField(max_length=100)
    data_created = models.DateTimeField(auto_now_add=True)
    user_created = models.ForeignKey(Custom_user, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Project_user_db(models.Model):
    project_id = models.ForeignKey(Project_db, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Custom_user, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Project_role_db, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.project_id)


class Board_db(models.Model):
    name = models.CharField(max_length=100)
    project_id = models.ForeignKey(Project_db, on_delete=models.CASCADE)
    data_create = models.DateTimeField(auto_now_add=True)
    user_created = models.ForeignKey(Custom_user, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Board_user_db(models.Model):
    board_id = models.ForeignKey(Board_db, null=True, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Custom_user, null=True, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Project_role_db, on_delete=models.CASCADE)


class Group_db(models.Model):
    name = models.CharField(max_length=100)
    project_id = models.ForeignKey(Project_db, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class User_groups_db(models.Model):
    user_id = models.ForeignKey(Custom_user, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group_db, on_delete=models.CASCADE)


class Task_status_db(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User_task_db(models.Model):
    user_id = models.ForeignKey(Custom_user, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user_id)

class Task_db(models.Model):
    name = models.CharField(max_length=100)
    comment = models.CharField(max_length=100, null=True)
    creator = models.ForeignKey(Custom_user, null=True, on_delete=models.SET_NULL)
    board_id = models.ForeignKey(Board_db, null=True, on_delete=models.SET_NULL)
    user_task_id = models.ForeignKey(User_task_db, null=True, on_delete=models.SET_NULL)
    task_status_id = models.ForeignKey(Task_status_db, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


