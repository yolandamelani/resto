from django.contrib import admin
from .models import User, TableResto, MenuResto, Category, StatusModel

admin.site.register(User)
admin.site.register(TableResto)
admin.site.register(MenuResto)
admin.site.register(Category)
admin.site.register(StatusModel)