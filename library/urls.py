from django.urls import path
from . import views

urlpatterns = [
    path('error_404/', views.error_404, name='error_404'),
    path('error_500/', views.error_500, name='error_500'),

    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('student_view_loan/', views.student_loan_history, name='student_view_loan'),
    path("student_view_categories/", views.student_view_categories, name="student_view_categories"),
    path('student_view_books/', views.student_view_books, name='student_view_books'),
    path('student_view_books/<int:categoryId>/', views.student_view_books, name='student_view_books'),
    path('student_change_password/', views.student_change_password, name='student_change_password'),

    path("", views.index, name="index"),
    path("add_book/", views.add_book, name="add_book"),
    path("add_loan/", views.add_loan, name="add_loan"),
    path("view_books/", views.view_books, name="view_books"),
    path('view_books/<int:categoryId>/', views.view_books, name='view_books'),
    path("delete_book/<int:id>/", views.delete_book, name="delete_book"),
    path("edit_book/<int:id>/", views.edit_book, name="edit_book"),

    path("add_category/", views.add_category, name="add_category"),
    path("view_categories/", views.view_categories, name="view_categories"),
    path("delete_category/<int:id>/", views.delete_category, name="delete_category"),
    path("edit_category/<int:id>/", views.edit_category, name="edit_category"),
    path("check_category_name/<str:name>/", views.check_category_name, name="check_category_name"),

    path("view_students/", views.view_students, name="view_students"),
    path("view_students/<int:classId>/", views.view_students, name="view_students"),
    path("upload_file_student/", views.upload_file_student, name="upload_file_student"),
    path("download_sample_student/", views.download_sample_student, name="download_sample_student"),
    path("check_student_id/<int:id>/", views.check_student_id, name="check_student_id"),

    path("view_faculties/", views.view_faculties, name="view_faculties"),
    path("upload_file_faculty/", views.upload_file_faculty, name="upload_file_faculty"),
    path("download_sample_faculty/", views.download_sample_faculty, name="download_sample_faculty"),

    path("view_classes/", views.view_classes, name="view_classes"),
    path("view_classes/<int:facultyId>/", views.view_classes, name="view_classes"),
    path("upload_file_class/", views.upload_file_class, name="upload_file_class"),
    path("download_sample_class/", views.download_sample_class, name="download_sample_class"),

    path("view_loan_history/", views.view_loan_history, name="view_loan_history"),
    path("view_loan_history/<int:studentId>/", views.view_loan_history, name="view_loan_history"),
    path("add_loan/", views.add_loan, name="add_loan"),
    path("detail_loan/<int:id>", views.detail_loan, name="detail_loan"),
    path("return_loan/<int:id>", views.return_loan, name="return_loan"),
    path("renew_loan/<int:id>", views.renew_loan, name="renew_loan"),
    path("delete_loan/<int:id>", views.delete_loan, name="delete_loan"),

    path("delete_student/<int:id>/", views.delete_student, name="delete_student"),
    path('change_password/', views.change_password, name='change_password'),

    path('admin_view_accounts/', views.admin_view_accounts, name='admin_view_accounts'),
    path("admin_upload_file_account/", views.admin_upload_file_account, name="admin_upload_file_account"),
    path("admin_download_sample_account/", views.admin_download_sample_account, name="admin_download_sample_account"),
    path('admin_reset_password_account/<int:id>', views.admin_reset_password_account, name='admin_reset_password_account'),
    path('admin_delete_account/<int:id>', views.admin_delete_account, name='admin_delete_account'),

    path('admin_view_loan_history/', views.admin_view_loan_history, name='admin_view_loan_history'),
    path('admin_view_logs/', views.admin_view_logs, name='admin_view_logs'),
    
    path('admin_change_password/', views.admin_change_password, name='admin_change_password'),

    path('resetRole/', views.resetRole, name='resetRole'),
]