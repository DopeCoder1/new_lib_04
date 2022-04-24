from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import Textarea


from .models import Order, StudentProfile, TeacherProfile, TheSis, TheSisCategory, Book, Category, Author, Article, \
    ArticleCategory, AdminProfile, OrderItem


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"placeholder":"Логин"}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={"placeholder":"Пароль"}))

class TeacherExtraForm(forms.ModelForm):
    photo = forms.ImageField(max_length=50, widget=forms.FileInput(attrs={"placeholder":"Фото"}))
    address = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"placeholder":"Адрес"}))

    class Meta:
        model = TeacherProfile
        fields = ["photo","address"]

class StudentExtraForm(forms.ModelForm):
    photo = forms.ImageField(max_length=50, widget=forms.FileInput(attrs={"placeholder":"Фото"}))
    address = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"placeholder":"Адрес"}))

    class Meta:
        model = StudentProfile
        fields = ["photo","address"]

TYPE_CHOICES = (
    ("Книга","Книга"),
    ("Дипломная работа","Дипломная работа"),
    ("Статья","Статья")
)
class BookForm(forms.ModelForm):
    type = forms.ChoiceField(choices=TYPE_CHOICES,widget=forms.RadioSelect())
    class Meta:
        model = Book
        fields = ["name","photo","author","category","file","desc","type"]

class ThesisForm(forms.ModelForm):
    class Meta:
        model = TheSis
        fields = ["name","photo","desc","file","category"]

    # def __init__(self, road_choices=None, *args, **kwargs):
    #     super(ThesisForm, self).__init__(*args, **kwargs)
    #     if road_choices:
    #         self.fields['category'].choices = road_choices

class TeacherUserForm(forms.ModelForm):
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={"placeholder": "Имя"}))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={"placeholder": "Фамилия"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"placeholder": "Почта"}))
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={"placeholder": "Логин"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}))

    class Meta:
        model = User
        fields=['first_name','last_name',"email",'username','password']


class StudentUserForm(forms.ModelForm):
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={"placeholder": "Имя"}))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={"placeholder": "Фамилия"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"placeholder": "Почта"}))
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={"placeholder": "Логин"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}))

    class Meta:
        model = User
        fields=['first_name','last_name',"email",'username','password']


class RegistrationForm2(UserCreationForm):
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={"placeholder":"Имя"}))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={"placeholder":"Фамилия"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"placeholder":"Почта"}))
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={"placeholder":"Логин"}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"placeholder":"Пароль"}))
    password2 = forms.CharField(label="Подтверждение Пароля", widget=forms.PasswordInput(attrs={"placeholder":"Подтверждение Пароля"}))

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
        ]

    def save(self, commit=True):
        user = super(RegistrationForm2, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class RegistrationForm(UserCreationForm):
    name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={"required class":"registration_inputs","id":"name"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"required class":"registration_inputs","id":"email"}))
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={"required class":"registration_inputs","id":"surname"}))
    password1 = forms.CharField(label="Пароль 1", widget=forms.PasswordInput(attrs={"required class":"registration_inputs","id":"pass"}))
    password2 = forms.CharField(label="Пароль 2", widget=forms.PasswordInput(attrs={"required class":"registration_inputs","id":"conf_pass"}))

    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'username',
            'password1',
            'password2',
        ]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user






class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username","first_name","last_name","email")


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'phone', 'address', 'account_no', 'transaction_id','status']

class OrderCreateForm2(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'phone', 'address', 'account_no', 'transaction_id',]

class ThesisCategoryForm(forms.ModelForm):
    class Meta:
        model = TheSisCategory
        fields = "__all__"



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = "__all__"


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["photo","name","category","desc","type"]

class ArticleCategoryForm(forms.ModelForm):
    class Meta:
        model = ArticleCategory
        fields ="__all__"

class AdminUserForm(forms.ModelForm):
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={"placeholder": "Имя"}))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={"placeholder": "Фамилия"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"placeholder": "Почта"}))
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={"placeholder": "Логин"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}))

    class Meta:
        model = User
        fields=['first_name','last_name',"email",'username','password']

class AdminUserForm2(forms.ModelForm):
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={"placeholder": "Имя"}))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={"placeholder": "Фамилия"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"placeholder": "Почта"}))


    class Meta:
        model = User
        fields=['first_name','last_name',"email"]

class AdminExtraForm(forms.ModelForm):
    photo = forms.ImageField(max_length=50, widget=forms.FileInput(attrs={"placeholder":"Фото"}))

    class Meta:
        model = AdminProfile
        fields = ["photo"]