from django.shortcuts import render, redirect
from library.models import Account

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
                return redirect('home')
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