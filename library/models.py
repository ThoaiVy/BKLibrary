from django.db import models

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    is_student = models.BooleanField(default=False)
    ROLE_CHOICES = [
        ('IsStudent', 'Student'),
        ('IsLibrarian', 'Librarian'),
        ('IsAdmin', 'Admin'),
    ]

    role = models.CharField(
        max_length=100,
        choices=ROLE_CHOICES,
        default='IsStudent',
    )

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

class Faculty(models.Model):
    id = models.CharField(max_length=3,primary_key=True)
    name = models.CharField(max_length=100)

class StudentClass(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)

class Student(models.Model):
    id = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=100)
    studentClass = models.ForeignKey(StudentClass, on_delete=models.SET_NULL, null=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)

class Librarian(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    
class Loan(models.Model):
    id = models.AutoField(primary_key=True)
    books = models.ManyToManyField(Book)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    borrow_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

class Log(models.Model):
    id = models.AutoField(primary_key=True)
    action = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)