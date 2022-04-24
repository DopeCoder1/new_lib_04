from django.contrib import admin
from .models import *


# Register your models here.
class AdminCat(admin.ModelAdmin):
    list_display = ['name',]

class AdminAuthor(admin.ModelAdmin):
    list_display = ['name',]



class AdminBook(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ["name",]



admin.site.register(Author, AdminAuthor)
admin.site.register(Book, AdminBook)
admin.site.register(Category, AdminCat)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(TheSis)
admin.site.register(TheSisCategory)
admin.site.register(Article)
admin.site.register(ArticleCategory)
admin.site.register(AdminProfile)
