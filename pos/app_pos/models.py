from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_waitress = models.BooleanField(default = False)
    is_cashier = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.username} {self.first_name} {self.last_name}'

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TableResto(models.Model):
    status_choices = (
        ('Aktif', 'Aktif'),
        ('Tidak Aktif', 'Tidak Aktif'),
    )
    status_table_choices = (
        ('Kosong', 'Kosong'),
        ('Terisi', 'Terisi'),
    )
    code = models.CharField(max_length = 20)
    name = models.CharField(max_length = 100)
    capacity = models.IntegerField(default = 0)
    table_status = models.CharField(max_length = 15, choices = status_table_choices, default = 'Kosong')
    status = models.CharField(max_length = 15, choices = status_choices, default = 'Aktif')
    user_create = models.ForeignKey(User, related_name = 'user_created_table_resto', blank = True, null = True, on_delete = models.SET_NULL)
    user_update = models.ForeignKey(User, related_name = 'user_update_table_resto', blank = True, null = True, on_delete = models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

class StatusModel(models.Model):

    status = (
        ('Aktif', 'Aktif'),
        ('Tidak Aktif', 'Tidak Aktif'),
    )
    status_name = models.CharField(max_length = 15, choices = status, default = 'Aktif')
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status_name


class MenuResto(models.Model):

    status_menu_choices = (
        ('Kosong', 'Kosong'),
        ('Ada', 'Ada'),
    )

    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_menu=models.CharField(max_length=100)
    menu_status= models.CharField(max_length = 15, choices = status_menu_choices, default = 'Kosong')
    is_available = models.BooleanField(default=True)
    status = models.ForeignKey(StatusModel, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name