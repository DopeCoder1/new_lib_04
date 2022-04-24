from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView

from .models import User
from DiDiStore import settings
from .forms import RegistrationForm, LoginForm, UserForm, OrderCreateForm, RegistrationForm2, StudentUserForm, \
    StudentExtraForm, ThesisForm, TeacherUserForm, TeacherExtraForm, BookForm, CategoryForm, AuthorForm, \
    ThesisCategoryForm, ArticleForm, ArticleCategoryForm, AdminUserForm, AdminExtraForm, AdminUserForm2, OrderItemForm, \
    OrderCreateForm2
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Book, Category
from .cart import Cart

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()
def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def afterlogin_view(request):
    if is_student(request.user):
        accountapproval=StudentProfile.objects.all().filter(user_id=request.user.id)
        if accountapproval:
            return redirect('student_home')
    elif is_teacher(request.user):
        accountapproval =TeacherProfile.objects.all().filter(user_id=request.user.id)
        if accountapproval:
            return redirect('teacher_home')
    elif is_admin(request.user):
        return redirect('admin_home')

#students


@login_required(login_url="login")
@user_passes_test(is_student)
def student_index(request):
    article = Article.objects.all()
    books = Book.objects.all()
    cats = Category.objects.all()
    thesis_cats = TheSisCategory.objects.all()
    thesis = TheSis.objects.all()
    article_cats = ArticleCategory.objects.all()

    context = {
        "article":article,
        "books":books,
        "cats":cats,
        "thesis_cats":thesis_cats,
        "the_sis":thesis,
        "article_cats":article_cats,
    }
    return render(request,"DiDiStoreApp/student_index.html",context)

@login_required(login_url='login')
@user_passes_test(is_student)
def student_cart_detailss(request):
    cart = Cart(request)
    context = {
        "cart": cart,
    }
    return render(request, 'DiDiStoreApp/student_desired.html', context)

@login_required(login_url='login')
@user_passes_test(is_student)
def student_cart_add(request, bookid):
    cart = Cart(request)
    book = get_object_or_404(Book,id=bookid)
    cart.add(book=book)
    return redirect('student_cart_detail')

@login_required(login_url='login')
@user_passes_test(is_student)
def student_cart_update(request, bookid, quantity):
    cart = Cart(request)
    book = get_object_or_404(Book, id=bookid)
    cart.update(book=book, quantity=quantity)
    price = (quantity)
    return render(request, 'cart/price.html', {"price": price})

@login_required(login_url='login')
@user_passes_test(is_student)
def student_cart_remove(request, bookid):
    cart = Cart(request)
    book = get_object_or_404(Book, id=bookid)
    cart.remove(book)
    return redirect('student_cart_detail')


@user_passes_test(is_student)
def searches(request):
    search_post = request.GET.get("search")
    if search_post:
        books = Book.objects.filter(Q(name__icontains=search_post))
        thesis = TheSis.objects.filter(Q(name__icontains=search_post))
        article = Article.objects.filter(Q(name__icontains=search_post))
    return render(request,"DiDiStoreApp/student_index.html",{"article":article,"books":books,"thesis":thesis})



@user_passes_test(is_teacher)
def teacher_searches(request):
    search_post = request.GET.get("search")
    if search_post:
        books = Book.objects.filter(Q(name__icontains=search_post))
        thesis = TheSis.objects.filter(Q(name__icontains=search_post))
        article = Article.objects.filter(Q(name__icontains=search_post))

    cats = Category.objects.all()
    the_cats = TheSisCategory.objects.all()
    article_cats = ArticleCategory.objects.all()
    context = {
        "cats":cats,
        "the_cats":the_cats,
        "article_cats":article_cats,
        "article":article,
        "books":books,
        "thesis":thesis
    }
    return render(request,"DiDiStoreApp/teacher_index.html",context)




@user_passes_test(is_admin)
def admin_searches(request):
    search_post = request.GET.get("search")
    if search_post:
        books = Book.objects.filter(Q(name__icontains=search_post))
        thesis = TheSis.objects.filter(Q(name__icontains=search_post))
        article = Article.objects.filter(Q(name__icontains=search_post))

    cats = Category.objects.all()
    the_cats = TheSisCategory.objects.all()
    article_cats = ArticleCategory.objects.all()
    context = {
        "cats":cats,
        "the_cats":the_cats,
        "article_cats":article_cats,
        "article":article,
        "books":books,
        "thesis":thesis
    }
    return render(request,"DiDiStoreApp/admin_index.html",context)

@login_required(login_url='login')
@user_passes_test(is_student)
def student_cart_details(request):
    cart = Cart(request)
    context = {
        "cart": cart,
    }
    return render(request, 'DiDiStoreApp/student_desired.html', context)


@login_required(login_url="login")
@user_passes_test(is_teacher)
def student_create_thesis(request):
    form = ThesisForm()
    if request.method == "POST":
        form = ThesisForm(request.POST,request.FILES)
        if form.is_valid():
            f=form.save(commit=False)
            f.student = request.user
            f.save()
        return redirect("student_home")
    return render(request,"DiDiStoreApp/student_create_thesis.html",{"form":form})

@user_passes_test(is_student)
def student_userpage(request):
    thesis = TheSis.objects.filter(student_id=request.user.id)
    profile = StudentProfile.objects.get(user_id=request.user.id)
    myorder = Order.objects.filter(customer_id=request.user.id).order_by('-created')
    order_item = OrderItem.objects.filter(order__customer_id=request.user.id)
    context = {
        "thesis":thesis,
        "profile":profile,
        "myorder":myorder,
        "order_item":order_item,
    }
    return render(request,"DiDiStoreApp/student_account.html",context)


@login_required(login_url="login")
@user_passes_test(is_student)
def student_order_create(request):
    cart = Cart(request)
    if request.user.is_authenticated:
        customer = get_object_or_404(User, id=request.user.id)
        profiles = StudentProfile.objects.get(user_id=request.user.id)
        form = OrderCreateForm2(request.POST or None, initial={"name": customer.first_name+" "+customer.last_name, "email": customer.email,"address":profiles.address})
        if request.method == 'POST':
            if form.is_valid():
                order = form.save(commit=False)
                order.customer = User.objects.get(id=request.user.id)
                order.payable = cart.get_total_price()
                order.totalbook = len(cart)  # len(cart.cart) // number of individual book
                order.save()
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        book=item['book'],
                        quantity=item['quantity']
                    )
                cart.clear()
                return render(request, 'DiDiStoreApp/student_success.html', {'order': order})
            else:
                messages.error(request, "Fill out your information correctly.")

        if len(cart) > 0:
            return render(request, 'DiDiStoreApp/order.html', {"form": form})
        else:
            return redirect('home')
    else:
        return redirect('home')

@user_passes_test(is_student)
def student_order_list(request):
    myorder = Order.objects.filter(customer_id=request.user.id).order_by('-created')
    return render(request, 'DiDiStoreApp/student_order_list.html', {"myorder": myorder})


#Base function



def index(request):
    if is_student(request.user):
        return redirect("student_home")
    elif is_teacher(request.user):
        return redirect("teacher_home")
    elif is_admin(request.user):
        return redirect("admin_home")

    article_cats = ArticleCategory.objects.all()
    article = Article.objects.all()
    books = Book.objects.all()
    cats = Category.objects.all()
    thesis_cats = TheSisCategory.objects.all()
    thesis = TheSis.objects.all()
    context = {"article_cats": article_cats, "books": books, "article": article, "cats": cats,
               "thesis_cats": thesis_cats, "thesis": thesis}

    return render(request, "DiDiStoreApp/index.html", context)


def category_book(request, id):
    books = Book.objects.filter(category_id=id)
    article_cats = ArticleCategory.objects.all()
    cats = Category.objects.all()
    thesis_cats = TheSisCategory.objects.all()

    context = {
        "thesis_cats":thesis_cats,
        "article_cats":article_cats,
        "books": books,
        "cats": cats,
    }
    return render(request, "DiDiStoreApp/index.html", context)


def category_article(request, id):
    article_cats = ArticleCategory.objects.all()
    cats = Category.objects.all()
    thesis_cats = TheSisCategory.objects.all()
    article = Article.objects.filter(category_id=id)
    context = {
        "thesis_cats":thesis_cats,
        "article_cats":article_cats,
        "cats": cats,
        "article":article,
    }
    return render(request, "DiDiStoreApp/index.html", context)



def category_thesis(request, id):
    article_cats = ArticleCategory.objects.all()
    cats = Category.objects.all()
    thesis_cats = TheSisCategory.objects.all()
    thesis = TheSis.objects.filter(category_id=id)
    context = {
        "thesis":thesis,
        "thesis_cats":thesis_cats,
        "article_cats":article_cats,
        "cats": cats,
    }
    return render(request, "DiDiStoreApp/index.html", context)

def show_thesis(request,id):
    thesis = get_object_or_404(TheSis,id=id)
    context = {
        "thesis": thesis,
    }
    return render(request, "DiDiStoreApp/thesisdetail.html", context)




@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_show_book(request, bookid):
    bookss = get_object_or_404(Book, id=bookid)
    context = {
        "bookss": bookss,
    }
    return render(request, "DiDiStoreApp/det.html", context)

def show_book(request, bookid):
    bookss = get_object_or_404(Book, id=bookid)
    context = {
        "bookss": bookss,
    }
    return render(request, "DiDiStoreApp/det.html", context)




@user_passes_test(is_student)
def student_show_category_book(request, id):
    books = Book.objects.filter(category_id=id)
    article_cats = ArticleCategory.objects.all()
    cats = Category.objects.all()
    thesis_cats = TheSisCategory.objects.all()

    context = {
        "thesis_cats":thesis_cats,
        "article_cats":article_cats,
        "books": books,
        "cats": cats,
    }
    return render(request, "DiDiStoreApp/student_index.html", context)


@user_passes_test(is_student)
def student_show_category_thesis(request, id):
    thesis = TheSis.objects.filter(category_id=id)
    article_cats = ArticleCategory.objects.all()
    cats = Category.objects.all()
    thesis_cats = TheSisCategory.objects.all()

    context = {
        "thesis_cats": thesis_cats,
        "article_cats": article_cats,
        "thesis": thesis,
        "cats": cats,
    }
    return render(request, "DiDiStoreApp/student_index.html", context)


@user_passes_test(is_student)
def student_show_category_article(request, id):
    article = Article.objects.filter(category_id=id)
    article_cats = ArticleCategory.objects.all()
    cats = Category.objects.all()
    thesis_cats = TheSisCategory.objects.all()

    context = {
        "article": article,
        "article_cats": article_cats,
        "cats": cats,
        "thesis_cats": thesis_cats,
    }

    return render(request, "DiDiStoreApp/student_index.html", context)

def signout(request):
    logout(request)
    return redirect('home')


def LogoutUser(request):
    logout(request)
    redirect("home")



def all_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                print("ye")
                login(request,user)
                return redirect("afterlogin")
    return render(request,"DiDiStoreApp/login.html",{"form":form})


class SearchResultsView(ListView):
    model = Book
    template_name = 'DiDiStoreApp/search.html'

    def get_queryset(self):  # новый
        books = Book.objects.filter(Q(name="Наруто"))
        return books

def student_registration(request):
    form1 = StudentUserForm()
    form2 = StudentExtraForm()
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = StudentUserForm(request.POST)
        form2 = StudentExtraForm(request.POST,request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            f2.save()
            my_teacher_group = Group.objects.get_or_create(name='STUDENT')
            my_teacher_group[0].user_set.add(user)
            return redirect('login')
    return render(request,"DiDiStoreApp/student_register.html",context=mydict)


def teacher_registration(request):
    form1 = TeacherUserForm()
    form2 = TeacherExtraForm()
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = TeacherUserForm(request.POST)
        form2 = TeacherExtraForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            f2.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
            return redirect('login')
    return render(request, "DiDiStoreApp/teacher_register.html", context=mydict)


@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    article_cats = ArticleCategory.objects.all()
    article = Article.objects.all()
    books = Book.objects.all()
    cats = Category.objects.all()
    the_cats = TheSisCategory.objects.all()
    thesis = TheSis.objects.all()
    context = {"article_cats":article_cats,"books": books,"article":article, "cats": cats, "the_cats": the_cats, "thesis": thesis}
    return render(request, "DiDiStoreApp/teacher_index.html",context)


@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_showstudent(request):
    students = StudentProfile.objects.all()
    context = {
        "students":students
    }
    return render(request,"DiDiStoreApp/teacher_studlist.html",context)

@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_searchstudent(request):
    query = request.GET.get("search")
    if query:
        students=StudentProfile.objects.filter(Q(user__first_name__icontains=query)|Q(user__last_name__icontains=query))
    else:
        students=StudentProfile.objects.all()
    context={
        "students":students
    }
    return render(request,"DiDiStoreApp/teacher_student_list.html",context)

@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_addbook(request):
    form = BookForm()
    if request.method == "POST":
        form = BookForm(request.POST,request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.teacher = request.user
            f.save()
        return redirect("teacher_home")
    context = {
        "form":form,
    }
    return render(request,"DiDiStoreApp/teacher_book.html",context)

@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_add_author(request):
    form = AuthorForm()
    if request.method == "POST":
        form = AuthorForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("teacher_addbook")
    context = {
        "form":form,
    }
    return render(request,"DiDiStoreApp/teacher_book_author.html", context)



@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_add_category_book(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("teacher_addbook")
    context = {
        "form":form,
    }
    return render(request,"DiDiStoreApp/teacher_book_category.html", context)



def detail(request,id):
    book = get_object_or_404(Book,id=id)
    context = {
        "book":book
    }
    return render(request, 'DiDiStoreApp/detail.html', context)

def detail_thesis(request,id):
    book = get_object_or_404(TheSis,id=id)
    context = {
        "book":book
    }
    return render(request, 'DiDiStoreApp/detail.html', context)


def detail_article(request,id):
    book = get_object_or_404(Article,id=id)
    context = {
        "book":book
    }
    return render(request, 'DiDiStoreApp/detail.html', context)

@user_passes_test(is_teacher)
def teacher_cart_details(request):
    cart = Cart(request)
    context = {
        "cart": cart,
    }
    return render(request, 'DiDiStoreApp/teacher_desired.html', context)


@login_required(login_url='login')
@user_passes_test(is_teacher)
def teacher_cart_add(request, bookid):
    cart = Cart(request)
    book = get_object_or_404(Book,id=bookid)
    cart.add(book=book)
    return redirect('teacher_card_detail')

@login_required(login_url='login')
@user_passes_test(is_teacher)
def teacher_cart_update(request, bookid, quantity):
    cart = Cart(request)
    book = get_object_or_404(Book, id=bookid)
    cart.update(book=book, quantity=quantity)
    price = (quantity)
    return render(request, 'cart/price.html', {"price": price})

@login_required(login_url='login')
@user_passes_test(is_teacher)
def teacher_cart_remove(request, bookid):
    cart = Cart(request)
    book = get_object_or_404(Book, id=bookid)
    cart.remove(book)
    return redirect('teacher_card_detail')





@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_order_create(request):
    cart = Cart(request)
    if request.user.is_authenticated:
        customer = get_object_or_404(User, id=request.user.id)
        profiles = TeacherProfile.objects.get(user_id=request.user.id)
        form = OrderCreateForm2(request.POST or None, initial={"name": customer.first_name+" "+customer.last_name, "email": customer.email,"address":profiles.address})
        if request.method == 'POST':
            if form.is_valid():
                order = form.save(commit=False)
                order.customer = User.objects.get(id=request.user.id)
                order.payable = cart.get_total_price()
                order.totalbook = len(cart)  # len(cart.cart) // number of individual book
                order.save()
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        book=item['book'],
                        quantity=item['quantity']
                    )
                cart.clear()
                return render(request, 'DiDiStoreApp/teacher_success.html', {'order': order})
            else:
                messages.error(request, "Fill out your information correctly.")

        if len(cart) > 0:
            return render(request, 'DiDiStoreApp/order.html', {"form": form})
        else:
            return redirect('teacher_home')
    else:
        return redirect('teacher_home')

@user_passes_test(is_teacher)
def teacher_order_list(request):
    myorder = Order.objects.filter(customer_id=request.user.id).order_by('-created')
    return render(request, 'DiDiStoreApp/student_order_list.html', {"myorder": myorder})


@user_passes_test(is_teacher)
def teacher_show_category(request, id):
    cats = Category.objects.all()
    the_cats = TheSisCategory.objects.all()
    article_cats = ArticleCategory.objects.all()
    books = Book.objects.filter(category_id=id)

    context = {
        "cats":cats,
        "the_cats":the_cats,
        "article_cats":article_cats,
        "books": books,

    }
    return render(request, "DiDiStoreApp/teacher_index.html", context)

@user_passes_test(is_teacher)
def teacher_show_category_article(request, id):
    cats = Category.objects.all()
    the_cats = TheSisCategory.objects.all()
    article_cats = ArticleCategory.objects.all()
    article = Article.objects.filter(category_id=id)
    context = {
        "cats": cats,
        "the_cats": the_cats,
        "article_cats": article_cats,
        "article": article,
    }
    return render(request, "DiDiStoreApp/teacher_index.html", context)


@user_passes_test(is_teacher)
def teacher_show_category_thesis(request, id):
    cats = Category.objects.all()
    the_cats = TheSisCategory.objects.all()
    article_cats = ArticleCategory.objects.all()
    thesis = TheSis.objects.filter(category_id=id)
    context = {
        "cats": cats,
        "the_cats": the_cats,
        "article_cats": article_cats,
        "thesis": thesis,
    }
    return render(request, "DiDiStoreApp/teacher_index.html", context)

@user_passes_test(is_student)
def student_detail_book(request,id):
    thesis = get_object_or_404(Book,id=id)
    context = {
        "thesis":thesis,
    }
    return render(request,"DiDiStoreApp/student_book_det.html",context)


def teacher_detail_book(request,id):
    book = get_object_or_404(Book,id=id)
    context = {
        "book":book,
    }
    return render(request,"DiDiStoreApp/teacher_book_det.html",context)


def teacher_show_thesis(request,id):
    thesis = get_object_or_404(TheSis,id=id)
    context = {
        "thesis": thesis,
    }
    return render(request, "DiDiStoreApp/thesisdetail.html", context)


@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_userpage(request):
    article = Article.objects.filter(teacher_id=request.user.id)
    book = Book.objects.filter(teacher_id=request.user.id)
    thesis = TheSis.objects.filter(student_id=request.user.id)
    profile = TeacherProfile.objects.get(user_id=request.user.id)
    myorder = Order.objects.filter(customer_id=request.user.id).order_by('-created')
    order_item = OrderItem.objects.filter(order__customer_id=request.user.id)
    context = {
        "article":article,
        "book":book,
        "thesis": thesis,
        "profile": profile,
        "myorder": myorder,
        "order_item": order_item,
    }
    return render(request, "DiDiStoreApp/teacher_account.html", context)


@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_thesis_create(request):
    form = ThesisForm()
    if request.method == "POST":
        form = ThesisForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.student = request.user
            f.save()
        return redirect("teacher_home")
    return render(request, "DiDiStoreApp/teacher_thesis_create.html", {"form": form})


@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_thesis_category(request):
    form = ThesisCategoryForm()
    if request.method == "POST":
        form = ThesisCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("teacher_thesis_create")
    return render(request,"DiDiStoreApp/teacher_thesis_category.html",{"form":form})




@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_article_create(request):
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.teacher = request.user
            f.save()
        return redirect("teacher_home")
    return render(request, "DiDiStoreApp/teacher_article_create.html", {"form": form})


@login_required(login_url="login")
@user_passes_test(is_teacher)
def teacher_article_category(request):
    form = ArticleCategoryForm()
    if request.method == "POST":
        form = ArticleCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("teacher_article_create")
    return render(request,"DiDiStoreApp/teacher_article_category.html",{"form":form})


@user_passes_test(is_student)
def student_detail_thesis(request,id):
    thesis = get_object_or_404(TheSis,id=id)
    context = {
        "thesis": thesis,
    }
    return render(request, "DiDiStoreApp/student_thesis_det.html", context)

@user_passes_test(is_teacher)
def teacher_detail_thesis(request,id):
    thesis = get_object_or_404(TheSis,id=id)
    context = {
        "thesis": thesis,
    }
    return render(request, "DiDiStoreApp/teacher_thesis_detail.html", context)

@user_passes_test(is_student)
def student_detail_article(request,id):
    thesis = get_object_or_404(Article,id=id)
    context = {
        "thesis": thesis,
    }
    return render(request, "DiDiStoreApp/student_article_det.html", context)

@user_passes_test(is_teacher)
def teacher_detail_article(request,id):
    thesis = get_object_or_404(Article,id=id)
    context = {
        "thesis": thesis,
    }
    return render(request, "DiDiStoreApp/teacher_article_detail.html", context)



#admin
@user_passes_test(is_admin)
def admin_report_all_orderItem(request):
    order_order_item_book = OrderItem.objects.all().count()
    order_item = OrderItem.objects.all()
    count_order_item = OrderItem.objects.all().count()
    count_order_item_status = OrderItem.objects.all().count()
    context={
        "order_order_item_book":order_order_item_book,
        "order_item":order_item ,
        "count_order_item":count_order_item,
        "count_order_item_status":count_order_item_status,
    }
    return render(request,"DiDiStoreApp/admin_orderItem_report.html",context)


@user_passes_test(is_admin)
def admin_report_orderItem(request):
    order_order_item_book = OrderItem.objects.filter(order__customer_id=request.user.id).count()
    order_item = OrderItem.objects.filter(order__customer_id=request.user.id)
    count_order_item = OrderItem.objects.filter(order__customer_id=request.user.id).count()
    count_order_item_status = OrderItem.objects.filter(order__customer_id=request.user.id,order__status=True).count()
    context={
        "order_order_item_book":order_order_item_book,
        "order_item":order_item ,
        "count_order_item":count_order_item,
        "count_order_item_status":count_order_item_status,
    }
    return render(request,"DiDiStoreApp/admin_orderItem_report.html",context)


@user_passes_test(is_admin)
def admin_report_article(request):
    article = Article.objects.filter(teacher_id=request.user.id)
    context={
        "article":article ,
    }
    return render(request,"DiDiStoreApp/admin_report_article.html",context)


@user_passes_test(is_admin)
def admin_report_article_all(request):
    article = Article.objects.all()
    context={
        "article":article ,
    }
    return render(request,"DiDiStoreApp/admin_report_article.html",context)


@user_passes_test(is_admin)
def admin_report_thesis_all(request):
    thesis = TheSis.objects.all()
    context={
        "thesis":thesis ,
    }
    return render(request,"DiDiStoreApp/admin_thesis_report.html",context)

@user_passes_test(is_admin)
def admin_report_thesis(request):
    thesis = TheSis.objects.filter(student_id=request.user.id)
    context={
        "thesis":thesis ,
    }
    return render(request,"DiDiStoreApp/admin_thesis_report.html",context)

@user_passes_test(is_admin)
def admin_report_all_book(request):
    count_order_item = Book.objects.all().count()
    books = Book.objects.all()
    context = {
        "count_order_item": count_order_item,
        "books": books,
    }
    return render(request, "DiDiStoreApp/admin_book_report.html", context)
@user_passes_test(is_admin)
def admin_report_book(request):
    count_order_item = Book.objects.filter(teacher_id=request.user.id).count()
    books = Book.objects.filter(teacher_id=request.user.id)
    context={
        "count_order_item":count_order_item,
        "books":books,
    }
    return render(request,"DiDiStoreApp/admin_book_report.html",context)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_article_category(request):
    form = ArticleCategoryForm()
    if request.method == "POST":
        form = ArticleCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_article_create")
    return render(request,"DiDiStoreApp/admin_article_category.html",{"form":form})

@user_passes_test(is_admin)
def admin_show_teacher(request):
    pass

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_article_create(request):
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.teacher = request.user
            f.save()
        return redirect("admin_home")
    return render(request, "DiDiStoreApp/admin_article_create.html", {"form": form})


@user_passes_test(is_admin)
def admin_order_list(request):
    myorder = Order.objects.filter(customer_id=request.user.id).order_by('-created')
    return render(request, 'DiDiStoreApp/admin_order_list.html', {"myorder": myorder})



@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_order_create(request):
    cart = Cart(request)
    if request.user.is_authenticated:
        customer = get_object_or_404(User, id=request.user.id)
        form = OrderCreateForm2(request.POST or None, initial={"name": customer.first_name+" "+customer.last_name, "email": customer.email})
        if request.method == 'POST':
            if form.is_valid():
                order = form.save(commit=False)
                order.customer = User.objects.get(id=request.user.id)
                order.payable = cart.get_total_price()
                order.totalbook = len(cart)  # len(cart.cart) // number of individual book
                order.save()
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        book=item['book'],
                        quantity=item['quantity']
                    )
                cart.clear()
                return render(request, 'DiDiStoreApp/admin_success.html', {'order': order})
            else:
                messages.error(request, "Fill out your information correctly.")

        if len(cart) > 0:
            return render(request, 'DiDiStoreApp/order.html', {"form": form})
        else:
            return redirect('admin_home')
    else:
        return redirect('admin_home')



@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_cart_remove(request, bookid):
    cart = Cart(request)
    book = get_object_or_404(Book, id=bookid)
    cart.remove(book)
    return redirect("admin_card_detail")


@user_passes_test(is_admin)
def admin_cart_details(request):
    cart = Cart(request)
    context = {
        "cart": cart,
    }
    return render(request, 'DiDiStoreApp/admin_desired.html', context)

@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_cart_add(request, bookid):
    cart = Cart(request)
    book = get_object_or_404(Book,id=bookid)
    cart.add(book=book)
    return redirect('admin_card_detail')

@user_passes_test(is_admin)
def admin_edit_profile(request):
    if request.method == "POST":
        user_form = AdminUserForm2(request.POST,instance=request.user)
        profile_form = AdminExtraForm(request.POST,request.FILES,instance=request.user.adminprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect("admin_userpage")
    else:
        user_form = AdminUserForm2()
        profile_form = AdminExtraForm()

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'DiDiStoreApp/Student_details.html',context)


@user_passes_test(is_admin)
def admin_create_other(request):
    form1 = StudentUserForm()
    form2 = StudentExtraForm()
    if request.method == "POST":
        form1 = StudentUserForm(request.POST)
        form2 = StudentExtraForm(request.POST,request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            user2 = form2.save(commit=False)
            user2.user = user
            user2.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
            return redirect("admin_showstudent")
    context = {
        "form1":form1,
        "form2":form2,
    }
    return render(request,"DiDiStoreApp/admin_add_student.html",context)

@user_passes_test(is_admin)
def admin_create_other_teachers(request):
    form1 = TeacherUserForm()
    form2 = TeacherExtraForm()
    if request.method == "POST":
        form1 = TeacherUserForm(request.POST)
        form2 = TeacherExtraForm(request.POST,request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            user2 = form2.save(commit=False)
            user2.user = user
            user2.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
            return redirect("admin_show_teacher")
    context = {
        "form1":form1,
        "form2":form2,
    }
    return render(request,"DiDiStoreApp/admin_add_teachers.html",context)

@user_passes_test(is_admin)
def admin_del_other(request,id):
    try:
        u = StudentProfile.objects.get(user_id=id)
        u2 = User.objects.get(id=id)
        u.delete()
        u2.delete()
        return redirect("admin_showstudent")
    except StudentProfile.DoesNotExist:
        messages.error(request,"Student Doesent not exist")
    return render(request,"DiDiStoreApp/admin_studlist.html",{"u":u})



def admin_registration(request):
    form1 = AdminUserForm()
    form2 = AdminExtraForm()
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = AdminUserForm(request.POST)
        form2 = AdminExtraForm(request.POST,request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            f2.save()
            my_student_group = Group.objects.get_or_create(name='ADMIN')
            my_student_group[0].user_set.add(user)
            return redirect('login')
    return render(request,"DiDiStoreApp/admin_register.html",context=mydict)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_dashboard(request):
    article_cats = ArticleCategory.objects.all()
    article = Article.objects.all()
    books = Book.objects.all()
    cats = Category.objects.all()
    thesis_cats = TheSisCategory.objects.all()
    thesis = TheSis.objects.all()
    context = {"article_cats":article_cats,"books": books,"article":article, "cats": cats, "thesis_cats": thesis_cats, "thesis": thesis}
    return render(request, "DiDiStoreApp/admin_index.html",context)


@user_passes_test(is_admin)
def admin_show_category_book(request, id):
    books = Book.objects.filter(category_id=id)
    article_cats = ArticleCategory.objects.all()
    cats = Category.objects.all()
    thesis_cats = TheSisCategory.objects.all()

    context = {
        "thesis_cats":thesis_cats,
        "article_cats":article_cats,
        "books": books,
        "cats": cats,
    }
    return render(request, "DiDiStoreApp/admin_index.html", context)

@user_passes_test(is_admin)
def admin_show_category_article(request, id):
    article = Article.objects.filter(category_id=id)
    article_cats = ArticleCategory.objects.all()
    cats = Category.objects.all()
    thesis_cats = TheSisCategory.objects.all()
    context = {
        "article": article,
        "article_cats": article_cats,
        "cats": cats,
        "thesis_cats": thesis_cats,
    }

    return render(request, "DiDiStoreApp/admin_index.html", context)

@user_passes_test(is_admin)
def admin_show_category_thesis(request, id):
    thesis = TheSis.objects.filter(category_id=id)
    article_cats = ArticleCategory.objects.all()
    cats = Category.objects.all()
    thesis_cats = TheSisCategory.objects.all()

    context = {
        "thesis_cats": thesis_cats,
        "article_cats": article_cats,
        "thesis": thesis,
        "cats": cats,
    }
    return render(request, "DiDiStoreApp/admin_index.html", context)


@user_passes_test(is_admin)
def admin_detail_article(request,id):
    thesis = get_object_or_404(Article,id=id)
    context = {
        "thesis": thesis,
    }
    return render(request, "DiDiStoreApp/admin_article_det.html", context)


@user_passes_test(is_admin)
def admin_detail_thesis(request,id):
    thesis = get_object_or_404(TheSis,id=id)
    context = {
        "thesis": thesis,
    }
    return render(request, "DiDiStoreApp/admin_detail_thesis.html", context)

@user_passes_test(is_admin)
def admin_detail_book(request,id):
    book = get_object_or_404(Book,id=id)
    context = {
        "book":book,
    }
    return render(request,"DiDiStoreApp/admin_detail_book.html",context)


@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_add_category_book(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_addbook")
    context = {
        "form":form,
    }
    return render(request,"DiDiStoreApp/admin_add_category_book.html", context)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_addbook(request):
    form = BookForm()
    if request.method == "POST":
        form = BookForm(request.POST,request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.teacher = request.user
            f.save()
        return redirect("admin_home")
    context = {
        "form":form,
    }
    return render(request,"DiDiStoreApp/admin_addbook.html",context)


@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_userpage(request):
    article = Article.objects.filter(teacher_id=request.user.id)
    book = Book.objects.filter(teacher_id=request.user.id)
    thesis = TheSis.objects.filter(student_id=request.user.id)
    profile = AdminProfile.objects.get(user_id=request.user.id)
    myorder = Order.objects.filter(customer_id=request.user.id).order_by('-created')
    order_item = OrderItem.objects.filter(order__customer_id=request.user.id)
    context = {
        "article":article,
        "book":book,
        "thesis": thesis,
        "profile": profile,
        "myorder": myorder,
        "order_item": order_item,
    }
    return render(request, "DiDiStoreApp/admin_account.html", context)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_add_author(request):
    form = AuthorForm()
    if request.method == "POST":
        form = AuthorForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_addbook")
    context = {
        "form":form,
    }
    return render(request,"DiDiStoreApp/admin_add_author.html", context)



@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_thesis_create(request):
    form = ThesisForm()
    if request.method == "POST":
        form = ThesisForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.student = request.user
            f.save()
        return redirect("admin_home")
    return render(request, "DiDiStoreApp/admin_thesis_create.html", {"form": form})


@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_thesis_category(request):
    form = ThesisCategoryForm()
    if request.method == "POST":
        form = ThesisCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_thesis_create")
    return render(request,"DiDiStoreApp/admin_thesis_category.html",{"form":form})


@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_showstudent(request):
    students = StudentProfile.objects.all()
    context = {
        "students":students
    }
    return render(request,"DiDiStoreApp/admin_studlist.html",context)

@login_required(login_url="login")
@user_passes_test(is_admin)
def admin_showteacher(request):
    students = TeacherProfile.objects.filter()
    context = {
        "students":students
    }
    return render(request,"DiDiStoreApp/admin_teacher_list.html",context)





@user_passes_test(is_teacher)
def teacher_report_book(request):
    count_order_item = Book.objects.filter(teacher_id=request.user.id).count()
    books = Book.objects.filter(teacher_id=request.user.id)
    context={
        "count_order_item":count_order_item,
        "books":books,
    }
    return render(request,"DiDiStoreApp/teacher_book_report.html",context)



@user_passes_test(is_teacher)
def teacher_report_thesis(request):
    thesis = TheSis.objects.filter(student_id=request.user.id)
    context={
        "thesis":thesis ,
    }
    return render(request,"DiDiStoreApp/teacher_thesis_report.html",context)

@user_passes_test(is_teacher)
def teacher_report_article(request):
    article = Article.objects.filter(teacher_id=request.user.id)
    context={
        "article":article ,
    }
    return render(request,"DiDiStoreApp/teacher_article_report.html",context)

@user_passes_test(is_teacher)
def teacher_report_orderItem(request):
    order_order_item_book = OrderItem.objects.filter(order__customer_id=request.user.id).count()
    order_item = OrderItem.objects.filter(order__customer_id=request.user.id)
    count_order_item = OrderItem.objects.filter(order__customer_id=request.user.id).count()
    count_order_item_status = OrderItem.objects.filter(order__customer_id=request.user.id,order__status=True).count()
    context={
        "order_order_item_book":order_order_item_book,
        "order_item":order_item ,
        "count_order_item":count_order_item,
        "count_order_item_status":count_order_item_status,
    }
    return render(request,"DiDiStoreApp/teacher_orderItem_report.html",context)



@user_passes_test(is_admin)
def admin_del_other_teachers(request,id):
    try:
        u = TeacherProfile.objects.get(user_id=id)
        u2 =User.objects.get(id=id)
        u.delete()
        u2.delete()
        return redirect("admin_show_teacher")
    except StudentProfile.DoesNotExist:
        messages.error(request,"Student Doesent not exist")
    return render(request,"DiDiStoreApp/admin_teacher_list.html",{"u":u})


def admin_order_lists(request):
    orders = Order.objects.all()
    orders_count = Order.objects.all().count()
    order_item = OrderItem.objects.all()
    context = {
        "order_item":order_item,
        "orders":orders,
        "orders_count":orders_count
    }
    return render(request,"DiDiStoreApp/admin_confirmed_order.html",context)

@user_passes_test(is_admin)
def admin_create_order_edit(request,id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Order, id=id)

    # pass the object as instance in form
    form = OrderCreateForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return redirect("admin_order_lists")

    # add form dictionary to context
    context["form"] = form

    return render(request, "DiDiStoreApp/admin_confirmed_edit.html", context)
