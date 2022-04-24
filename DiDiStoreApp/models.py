from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


TYPE_CHOICES = (
    ("Книга","Книга"),
    ("Дипломная работа","Дипломная работа"),
    ("Статья","Статья")
)

class AdminProfile(models.Model):
    photo = models.ImageField(upload_to="users/%Y/%m/%d/",  verbose_name="Фото")
    user = models.OneToOneField(User,on_delete=models.CASCADE,  verbose_name="Пользыватель")

    def __str__(self):
        return self.user.username

class TeacherProfile(models.Model):
    photo = models.ImageField(upload_to="users/%Y/%m/%d/",  verbose_name="Фото")
    user = models.OneToOneField(User,on_delete=models.CASCADE,  verbose_name="Пользыватель")
    address = models.CharField(max_length=255, verbose_name="Адрес")

    def __str__(self):
        return self.user.username

class StudentProfile(models.Model):
    photo = models.ImageField(upload_to="users/%Y/%m/%d/",  verbose_name="Фото")
    user = models.OneToOneField(User,on_delete=models.CASCADE,  verbose_name="Пользыватель")
    address = models.CharField(max_length=255, verbose_name="Адрес")

    def __str__(self):
        return self.user.username



class Book(models.Model):
    teacher = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    author = models.ForeignKey("Author", on_delete=models.CASCADE, verbose_name="Автор",blank=True,null=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField(max_length=100, verbose_name="Название")
    file = models.FileField(upload_to="files/%Y/%m/%d/",verbose_name="Книга")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="Последний изм.")
    desc = models.TextField(verbose_name="Описание")
    type = models.CharField(max_length=255,verbose_name="Тип",choices=TYPE_CHOICES,default="Книга")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"



class TheSisCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")

    def __str__(self):
        return self.name



class TheSis(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Название")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    category = models.ForeignKey(TheSisCategory, on_delete=models.CASCADE, verbose_name="Категория")
    file = models.FileField(upload_to="files/%Y/%m/%d/",verbose_name="Дипломная")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="Последний изм.")
    desc = models.TextField(verbose_name="Описание")
    type = models.CharField(max_length=255,verbose_name="Тип",choices=TYPE_CHOICES,default="Дипломная работа")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Дипломная"
        verbose_name_plural = "Дипломные"



class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    desc = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to="author_photos/%Y/%m/%d/", verbose_name="Фото")

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"




class Order(models.Model):
    customer = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=16)
    address = models.CharField(max_length=150)
    account_no = models.CharField(max_length = 20)
    transaction_id = models.IntegerField()
    totalbook = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField("Статус",default=False)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


class ArticleCategory(models.Model):
    name = models.CharField(max_length=255,verbose_name="Категория")

    def __str__(self):
        return self.name

class Article(models.Model):
    teacher = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    name = models.CharField(max_length=100, verbose_name="Название")
    category = models.ForeignKey(ArticleCategory,verbose_name="Категория",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="Последний изм.")
    desc = models.TextField(verbose_name="Описание")
    type = models.CharField(max_length=255,verbose_name="Тип",choices=TYPE_CHOICES,default="Cтатья")

    def __str__(self):
        return self.name
