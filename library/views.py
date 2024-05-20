from django.http import Http404, JsonResponse
from library.forms import LoanBookForm
from django.shortcuts import redirect, render,HttpResponse
from .models import *
from .forms import LoanBookForm
from .forms import UploadFileForm
from django.contrib.auth import authenticate, login, logout
from . import forms, models
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.files.storage import FileSystemStorage
import pandas as pd
from django.http import HttpResponse
import openpyxl
from openpyxl.styles import Font
from openpyxl.worksheet.datavalidation import DataValidation
from django.shortcuts import render, redirect

def index(request):
    return render(request, "index.html")

# Error
def error_unauthorized(request):
    return render(request, "error_unauthorized.html")

# Book
# @login_required(login_url = '/admin_login')
def view_books(request, categoryId=None):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')
    
    if categoryId:
        books = Book.objects.filter(category=categoryId)
    else:
        books = Book.objects.all()
    categories = Category.objects.all()
    return render(request, "view_books.html", {'books':books, 'categories':categories})

# @login_required(login_url = '/admin_login')
def add_book(request):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')
    
    if request.method == "POST":
        name = request.POST['name']
        author = request.POST['author']
        category = Category.objects.filter(id=request.POST['category'])[0]
        quantity = request.POST['quantity']
        books = Book.objects.create(name=name, author=author, category=category, quantity=quantity)
        books.save()
        alert = True
        return render(request, "add_book.html", {'alert':alert})
    categories = Category.objects.all()
    return render(request, "add_book.html", {'categories':categories})

def check_book_id(request, id):
    data = {
        'is_taken': Book.objects.filter(id=id).exists()
    }
    return JsonResponse(data)

def delete_book(request, id):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')
    
    books = Book.objects.filter(id=id)
    books.delete()
    return render(request, 'view_books.html')

def edit_book(request, id):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')
    
    book = Book.objects.get(id=id)
    if request.method == "POST":
        name = request.POST['name']
        author = request.POST['author']
        category = Category.objects.filter(id=request.POST['category'])[0]
        quantity = request.POST['quantity']
        book.name = name
        book.author = author
        book.category = category
        book.quantity = quantity
        book.save()
        alert = True
        return render(request, "edit_book.html", {'alert':alert, 'book':book})
    categories = Category.objects.all()
    return render(request, "edit_book.html", {'book':book, 'categories':categories})

# Category
def view_categories(request):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')
    
    categories = Category.objects.annotate(quantity=Count('book'))
    return render(request, "view_categories.html", {'categories': categories})

def add_category(request):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')
    
    if request.method == "POST":
        name = request.POST['name']
        category = Category.objects.create(name=name)
        category.save()
        alert = True
        return render(request, "add_category.html", {'alert':alert})
    return render(request, "add_category.html")

def delete_category(request, id):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')
    
    books = Book.objects.filter(category=id)
    books.delete()
    category = Category.objects.filter(id=id)
    category.delete()
    return render(request, "/view_categories")

def edit_category(request, id):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')
    
    category = Category.objects.get(id=id)
    if request.method == "POST":
        name = request.POST['name']
        category.name = name
        category.save()
        alert = True
        return render(request, "edit_category.html", {'alert':alert, 'category':category})
    return render(request, "edit_category.html", {'category':category})

def check_category_name(request, name):
    data = {
        'is_taken': Category.objects.filter(name=name).exists()
    }
    return JsonResponse(data)

# Student
# @login_required(login_url = '/admin_login')
def view_students(request, classId=None):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')
    
    if classId:
        students = Student.objects.filter(studentClass=classId)
    else:
        students = Student.objects.all()
    classes = StudentClass.objects.all()
    return render(request, "view_students.html", {'students':students, 'classes':classes})

def check_student_id(request, id):
    data = {
        'is_taken': Student.objects.filter(id=id).exists()
    }
    return JsonResponse(data)

def upload_file_student(request):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')
    
    if request.method == 'POST' and request.FILES['file']:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_path = fs.path(filename)
            
            try:
                data = pd.read_excel(file_path)
                for index, row in data.iterrows():
                    student, created = Student.objects.update_or_create(
                        id=row['id'],
                        defaults={
                            'name': row['name'],
                            'studentClass': StudentClass.objects.get(name=row['class']),
                        }
                    )
                    account, created = Account.objects.update_or_create(
                        username=row['username'],
                        defaults={
                            'password': row['password'],
                            'is_student': True,
                        }
                    )
                alert = "File imported successfully"
            except Exception as e:
                alert = f"Error processing file: {e}"

            return render(request, "/view_students")
    else:
        form = UploadFileForm()
    return render(request, "/view_students")

def download_sample_student(request):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')
    
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Data"

    columns = ["id", "name", "class", "username", "password"]
    for col_num, column_title in enumerate(columns, 1):
        cell = sheet.cell(row=1, column=col_num)
        cell.value = column_title
        cell.font = Font(bold=True)

    classes = StudentClass.objects.all()
    class_names = [cls.name for cls in classes]
    class_names_str = ','.join(class_names)

    dv = DataValidation(type="list", formula1=f'"{class_names_str}"', allow_blank=True)
    sheet.add_data_validation(dv)

    for row in range(2, 999):  # Áp dụng từ hàng 2 đến hàng 101 (hoặc số hàng bạn muốn)
        dv.add(sheet.cell(row=row, column=3))

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=sample_student.xlsx'

    workbook.save(response)
    return response
    
def delete_student(request, id):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')
    
    students = Student.objects.filter(id=id)
    students.delete()
    return render(request, "/view_students")

#Loan
def view_loan_history(request, studentId=None):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')
    
    if studentId:
        loans = Loan.objects.filter(student=Student.objects.get(id=studentId))
    else:
        loans = Loan.objects.all()
    return render(request, "view_loan_history.html", {'loanList':loans})

def add_loan(request):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')
    
    if request.method == "POST":
        receivedBookIds = request.POST.get('bookIds')
        bookIds = receivedBookIds.split(',')
        print(bookIds);
        for bookId in bookIds:
            book = Book.objects.get(id=bookId)
            student = Student.objects.get(id=request.POST['studentId'])
            due_date = request.POST['dueDate']
            borrow_date = datetime.now().strftime("%Y-%m-%d");
            loan = Loan.objects.create(book=book, student=student, borrow_date=borrow_date, return_date=None, due_date=due_date)
            loan.save()
        alert = True
        return render(request, "add_loan.html", {'alert':alert})
    books = Book.objects.all()
    students = Student.objects.all()
    return render(request, "add_loan.html", {'books':books, 'students':students})

def return_loan(request, id):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')

    loan = Loan.objects.get(id=id)
    loan.return_date = datetime.now().strftime("%Y-%m-%d")
    loan.save()
    return redirect('view_loan_history')

# Faculty
def view_faculties(request):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')
    
    faculties = Faculty.objects.all().annotate(quantity=Count('studentclass'))
    return render(request, "view_faculties.html", {'faculties':faculties})

def upload_file_faculty(request):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')
    
    if request.method == 'POST' and request.FILES['file']:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_path = fs.path(filename)
            
            try:
                data = pd.read_excel(file_path)
                for index, row in data.iterrows():
                    faculty, created = Faculty.objects.update_or_create(
                        id=row['id'],
                        defaults={'name': row['name']}
                    )
                message = "File imported successfully"
            except Exception as e:
                message = f"Error processing file: {e}"
            print(message)
            return redirect("/view_faculties")
    else:
        form = UploadFileForm()
    return redirect("/view_faculties")

def download_sample_faculty(request):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')
    
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Data"
    
    columns = ["id", "name"]
    for col_num, column_title in enumerate(columns, 1):
        cell = sheet.cell(row=1, column=col_num)
        cell.value = column_title
        cell.font = Font(bold=True)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=sample_faculty.xlsx'

    workbook.save(response)
    return response

# Class
def view_classes(request, facultyId=None):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')
    
    if facultyId:
        classes = StudentClass.objects.filter(faculty=facultyId).annotate(quantity=Count('student'))
    else:
        classes = StudentClass.objects.all().annotate(quantity=Count('student'))
    faculties = Faculty.objects.all()
    return render(request, "view_classes.html", {'classes':classes, 'faculties':faculties})

def upload_file_class(request):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')
    
    if request.method == 'POST' and request.FILES['file']:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_path = fs.path(filename)
            
            try:
                data = pd.read_excel(file_path)
                print(data)
                for index, row in data.iterrows():
                    new_class, created = StudentClass.objects.update_or_create(
                        name=row['name'],
                        defaults={'faculty': Faculty.objects.get(name=row['faculty'])}
                    )
                    
                message = "File imported successfully"
            except Exception as e:
                message = f"Error processing file: {e}"
            print(message)
            return render(request, "/view_classes")
    else:
        form = UploadFileForm()
    return render(request, "/view_classes")

def download_sample_class(request):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('error_unauthorized')
    
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Data"
    
    columns = ["name", "faculty"]
    for col_num, column_title in enumerate(columns, 1):
        cell = sheet.cell(row=1, column=col_num)
        cell.value = column_title
        cell.font = Font(bold=True)

    faculties = Faculty.objects.all()
    faculty_names = [faculty.name for faculty in faculties]

    faculty_names_str = ','.join(faculty_names)
    dv = DataValidation(type="list", formula1=f'"{faculty_names_str}"', allow_blank=True)
    sheet.add_data_validation(dv)

    for row in range(2, 999):
        dv.add(sheet.cell(row=row, column=3))

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=sample_class.xlsx'

    workbook.save(response)
    return response

# Create your views here.
def home(request):
    return render(request, 'library/index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            account = Account.objects.get(username=username)
            if account.password == password:
                request.session['account'] = account.username
                request.session['is_student'] = account.is_student
                if (account.is_student):
                    return redirect('student_view_books')
                else:
                    return redirect('view_books')
            else:
                error_message = 'Tài khoản hoặc mật khẩu không đúng'
                return render(request, 'library/login.html', {'error_message': error_message})
        except Account.DoesNotExist:
            error_message = 'Tài khoản hoặc mật khẩu không đúng'
            return render(request, 'library/login.html', {'error_message': error_message})
    else:
        return render(request, 'library/login.html')

def logout(request):
    if 'account' in request.session:
        del request.session['account']
        if 'is_student' in request.session:
            del request.session['is_student']
    
    return redirect('login')

def student_loan_history(request):
    if 'account' not in request.session:
        return redirect('login')
    
    student_id = request.session['account']
    loan_list = Loan.objects.filter(student__id=student_id).prefetch_related('student', 'book')


    return render(request, 'student_view_loan.html', {'loan_list': loan_list, 'today': date.today()})


def student_view_books(request, categoryId=None):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == False:
        return redirect('error_unauthorized')
    
    if categoryId:
        books = Book.objects.filter(category=categoryId)
    else:
        books = Book.objects.all()
    categories = Category.objects.all()

    return render(request, "student_view_books.html", {'books':books, 'categories':categories})

def student_view_categories(request):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == False:
        return redirect('error_unauthorized')
    
    categories = Category.objects.annotate(quantity=Count('book'))
    return render(request, "student_view_categories.html", {'categories': categories})

def student_change_password(request):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == False:
        return redirect('error_unauthorized')
    
    if request.method == "POST":
        old_password = request.POST['oldPassword']
        new_password = request.POST['newPassword']
        confirm_password = request.POST['confirmPassword']
        username = request.session['account']
        account = Account.objects.get(username=username)
        if account.password == old_password:
            if new_password == confirm_password:
                account.password = new_password
                account.save()
                alert = True
                return render(request, "student_change_password.html", {'alert':alert, 'account':account})
            else:
                error_message = "Mật khẩu mới không khớp"
                return render(request, "student_change_password.html", {'error_message':error_message, 'account':account})
        else:
            error_message = "Mật khẩu cũ không đúng"
            return render(request, "student_change_password.html", {'error_message':error_message, 'account':account})

    username = request.session['account']
    account = Account.objects.get(username=username)
    return render(request, "student_change_password.html", {'account':account})

def change_password(request):
    if 'account' not in request.session:
        return redirect('login')
    elif 'is_student' in request.session and request.session['is_student'] == True:
        return redirect('student_change_password')
    
    if request.method == "POST":
        old_password = request.POST['oldPassword']
        new_password = request.POST['newPassword']
        confirm_password = request.POST['confirmPassword']
        username = request.session['account']
        account = Account.objects.get(username=username)
        if account.password == old_password:
            if new_password == confirm_password:
                account.password = new_password
                account.save()
                alert = True
                return render(request, "change_password.html", {'alert':alert, 'account':account})
            else:
                error_message = "Mật khẩu mới không khớp"
                return render(request, "change_password.html", {'error_message':error_message, 'account':account})
        else:
            error_message = "Mật khẩu cũ không đúng"
            return render(request, "change_password.html", {'error_message':error_message, 'account':account})

    username = request.session['account']
    account = Account.objects.get(username=username)
    return render(request, "change_password.html", {'account':account})
    
