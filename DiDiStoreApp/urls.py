from unicodedata import name

from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from .views import *

urlpatterns = [
    path("detail/<int:id>/",detail,name="detail"),
    path("detail_thesis/<int:id>/", detail_thesis, name="detail_thesis"),
    path("detail_article/<int:id>/", detail_article, name="detail_article"),
    path('category_book/<int:id>/', category_book, name='category_book'),
    path('category_article/<int:id>/', category_article, name='category_article'),
    path('category_thesis/<int:id>/', category_thesis, name='category_thesis'),


    path("",index,name="home"),
    path("searches/",searches,name="searches"),
    path("teacher_searches/", teacher_searches, name="teacher_searches"),

    path("student_registraion/",student_registration,name="student_registration"),
    path("studentindex/",student_index,name="student_home"),
    path("student_userpage/",student_userpage,name="student_userpages"),
    path("studenorder_create/",student_order_create,name="student_order_create"),
    path("student_order_list/",student_order_list,name="student_order_list"),
    path("student_cart_add/<int:bookid>/",student_cart_add,name="student_cart_add"),
    path("student_cart_detail/",student_cart_details,name="student_cart_detail"),
    path("student_cart_remove<int:bookid>/",student_cart_remove,name="student_cart_remove"),
    path("student_create_thesis/",student_create_thesis,name="student_create_thesis"),

    path('student_category_book/<int:id>/', student_show_category_book, name='student_show_category_book'),
    path('student_category_article/<int:id>/', student_show_category_article, name='student_show_category_article'),
    path('student_category_thesis/<int:id>/', student_show_category_thesis, name='student_show_category_thesis'),
    path("student_detail_article/<int:id>/",student_detail_article,name="student_detail_article"),
    path("student_detail_thesis/<int:id>/", student_detail_thesis, name="student_detail_thesis"),
    path("student_detail_book/<int:id>/",student_detail_book,name="student_detail_book"),

    #
    path('studentlogin', all_login,name="login"),
    path("teacher_registration/", teacher_registration, name="teacher_registration"),
    path("exit/",LogoutView.as_view(),name="exit"),
    path('afterlogin', afterlogin_view,name='afterlogin'),


    #teacher
    path("teacher_detail_article/<int:id>/",teacher_detail_article,name="teacher_detail_article"),
    path("teacher_detail_thesis/<int:id>/", teacher_detail_thesis, name="teacher_detail_thesis"),
    path("teacher_detail_book/<int:id>/",teacher_detail_book,name="teacher_detail_book"),
    path("teacher_show_category/<int:id>/",teacher_show_category,name="teacher_show_category"),

    path("teacher_bookcategory/",teacher_add_category_book,name="teacher_category"),
    path("teacher_addbook/",teacher_addbook,name="teacher_addbook"),
    path("teacher_home/",teacher_dashboard,name="teacher_home"),
    path("teacher_userpage/",teacher_userpage,name="teacher_userpage"),
    path("teacher_book_author/",teacher_add_author,name="teacher_addauthor"),
    path("teacher_thesis_create/",teacher_thesis_create,name="teacher_thesis_create"),
    path("teacher_thesis_category/",teacher_thesis_category,name="teacher_thesis_category"),
    path("teacher_showstudent/",teacher_showstudent,name="teacher_showstudent"),
    path("teacher_show_category_thesis/<int:id>/",teacher_show_category_thesis,name="teacher_show_category_thesis"),
    path("teacher_show_category_article/<int:id>/",teacher_show_category_article,name="teacher_show_category_article"),

    path("teacher_cart_add/<int:bookid>/", teacher_cart_add, name="teacher_cart_add"),
    path("teacher_card_detail",teacher_cart_details,name="teacher_card_detail"),
    path("teacher_cart_remove<int:bookid>/", teacher_cart_remove, name="teacher_cart_remove"),
    path("teacher_order_create/",teacher_order_create,name="teacher_order_create"),
    path("teache_order_list/",teacher_order_list,name="teacher_order_list"),
    path("teacher_article/",teacher_article_create,name="teacher_article_create"),
    path("teacher_article_cat/",teacher_article_category,name="teacher_article_category"),

    path("teacher_report_book/",teacher_report_book,name="teacher_report_book"),
    path("teacher_report_thesis/", teacher_report_thesis, name="teacher_report_thesis"),
    path("teacher_report_article/", teacher_report_article, name="teacher_report_article"),
    path("teacher_report_order/", teacher_report_orderItem, name="teacher_report_order"),

    #admin
    path("admin_report_all_article/", admin_report_article_all, name="admin_report_all_article"),
    path("admin_report_all_order/", admin_report_all_orderItem, name="admin_report_all_order"),
    path("admin_report_all_book/", admin_report_all_book, name="admin_report_all_book"),
    path("admin_report_all_thesis/", admin_report_thesis_all, name="admin_report_all_thesis"),

    path("admin_report_book/",admin_report_book,name="admin_report_book"),
    path("admin_report_thesis/", admin_report_thesis, name="admin_report_thesis"),
    path("admin_report_article/", admin_report_article, name="admin_report_article"),
    path("admin_report_order/", admin_report_orderItem, name="admin_report_order"),

    path("admin_cart_add/<int:bookid>/", admin_cart_add, name="admin_cart_add"),
    path("admin_card_detail", admin_cart_details, name="admin_card_detail"),
    path("admin_cart_remove<int:bookid>/", admin_cart_remove, name="admin_cart_remove"),
    path("admin_order_create/", admin_order_create, name="admin_order_create"),
    path("admin_order_list/", admin_order_list, name="admin_order_list"),

    path("admin_article/", admin_article_create, name="admin_article_create"),
    path("admin_article_cat/", admin_article_category, name="admin_article_category"),

    path('admin_category_book/<int:id>/', admin_show_category_book, name='admin_show_category_book'),
    path('admin_category_article/<int:id>/', admin_show_category_article, name='admin_show_category_article'),
    path('admin_category_thesis/<int:id>/', admin_show_category_thesis, name='admin_show_category_thesis'),
    path("admin_detail_article/<int:id>/",admin_detail_article,name="admin_detail_article"),
    path("admin_detail_thesis/<int:id>/", admin_detail_thesis, name="admin_detail_thesis"),
    path("admin_detail_book/<int:id>/",admin_detail_book,name="admin_detail_book"),
    path("admin_regis/", admin_registration, name="admin_registration"),

    path("admin_bookcategory/", admin_add_category_book, name="admin_category"),
    path("admin_addbook/", admin_addbook, name="admin_addbook"),
    path("admin_home/", admin_dashboard, name="admin_home"),
    path("admin_userpage/", admin_userpage, name="admin_userpage"),
    path("admin_book_author/", admin_add_author, name="admin_addauthor"),
    path("admin_thesis_create/", admin_thesis_create, name="admin_thesis_create"),
    path("admin_thesis_category/", admin_thesis_category, name="admin_thesis_category"),
    path("admin_showstudent/", admin_showstudent, name="admin_showstudent"),
    path("admin_show_category_thesis/<int:id>/", admin_show_category_thesis, name="admin_show_category_thesis"),
    path("admin_show_category_article/<int:id>/", admin_show_category_article,name="admin_show_category_article"),
    path("admin_searches/",admin_searches,name="admin_searches"),
    path("admin_show_teacher/",admin_showteacher,name="admin_show_teacher"),
    path("admin_edit_profile/",admin_edit_profile,name="admin_edit_profile"),
    path("admin_del_other/<int:id>/",admin_del_other,name="admin_del_other"),
    path("admin_del_other_teachers/<int:id>/", admin_del_other_teachers, name="admin_del_other_teachers"),
    path("admin_add_other/", admin_create_other, name="admin_create_other"),
    path("admin_add_other_teachers/", admin_create_other_teachers, name="admin_create_other_teachers"),
    path("admin_order_lists",admin_order_lists,name="admin_order_lists"),
    path("admin_create_order_edit/<int:id>/",admin_create_order_edit,name="admin_create_order_edit"),
]
