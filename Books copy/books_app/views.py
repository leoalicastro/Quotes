from django.shortcuts import render, redirect
from .models import User, Quote
import bcrypt
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashedpassword = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(hashedpassword)
        new_user = User.objects.create(
            fname = request.POST['fname'],
            lname = request.POST['lname'],
            email = request.POST['email'],
            password = hashedpassword
        )
    request.session['user_id'] = new_user.id
    return redirect('/home')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email = request.POST['logemail'])
        request.session['user_id'] = user.id
        return redirect('/home')

def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        "this_user": user,
        "quotes": Quote.objects.all()
    }
    return render(request, 'home.html', context)

def add_quote(request):
    uploaded_by = User.objects.get(id=request.session['user_id'])
    errors = Quote.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/home')
    else:
        new_quote = Quote.objects.create(
            author = request.POST['author'],
            quote = request.POST['quote'],
            uploaded_by = uploaded_by,
        )
    return redirect('/home')

def user(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        "quotes": Quote.objects.all(),
        "user": user,
    }
    return render(request, 'details.html', context)

def edit(request, quote_id):
    errors = Quote.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect(f'/details/{quote_id}')
    else:
        edit = Quote.objects.get(id=quote_id)
        edit.author = request.POST['author']
        edit.quote = request.POST['quote']
        edit.save()
    return redirect('/home')

def my_account(request, user_id):
    context = {
        "this_user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'my_account.html', context)

def edit_account(request, user_id):
    errors = User.objects.edit_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect(f'/my_account/{user_id}')
    else:
        
        edit = User.objects.get(id=user_id)
        edit.fname = request.POST['fname']
        edit.lname = request.POST['lname']
        edit.email = request.POST['email']
        edit.save()
    return redirect(f'/my_account/{user_id}')

def edit_quote(request, quote_id):
    context ={
        'this_quote': Quote.objects.get(id=quote_id)
    }
    return render(request, 'edit_quote.html', context)

def update_quote(request, quote_id):
    errors = Quote.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/edit/{quote_id}')
    else:
        edit = Quote.objects.get(id=quote_id)
        edit.author = request.POST['author'],
        edit.quote = request.POST['quote'],
        edit.save()
    return redirect(f'/edit/{quote_id}')

def like_quote(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    user = User.objects.get(id=request.session['user_id'])
    user.likes.add(quote)
    return redirect('/home')

def unlike_quote(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    user = User.objects.get(id=request.session['user_id'])
    user.likes.remove(quote)
    return redirect('/home')

def delete(request, quote_id):
    delete = Quote.objects.get(id=quote_id)
    delete.delete()
    return redirect('/home')

def logout(request):
    request.session.clear()
    return redirect('/')
# Create your views here.
