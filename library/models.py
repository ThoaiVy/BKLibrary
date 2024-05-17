from django.db import models

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    is_student = models.BooleanField(default=False)

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
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    borrow_date = models.DateField()
    return_date = models.DateField()
    due_date = models.DateField()