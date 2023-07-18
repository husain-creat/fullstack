from django.shortcuts import render,  HttpResponse,redirect
from .models import *
from django.contrib import messages
import bcrypt


def index(request):
    	return render(request,'login.html')

def register(request):
    if request.method =='POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  
            print(pw_hash)
            request.session['username'] = fname + " "+ lname
            request.session['status']="Registered"
            User.objects.create(first_name=fname, last_name=lname,email=email, password=pw_hash)
    return redirect("/")
def login(request):
    if request.method =='POST':
        errors2 = User.objects.login_validator(request.POST)
        if len(errors2) > 0:
            for key, value in errors2.items():
                messages.error(request, value)
            return redirect('/')

        users = User.objects.filter(email=request.POST['email2'])
        if users:
            logged_user = users[0]
            if bcrypt.checkpw(request.POST['password2'].encode(), logged_user.password.encode()):
                request.session['username'] = logged_user.first_name
                request.session['status']="logged in"
                request.session['user_id'] = logged_user.id
                return redirect('/book')
            print("""Wrong password""")
        return redirect("/")
def book(request):
    return render(request,'book.html')  
def book(request):
    user = User.objects.get(id = request.session['user_id'] )
    books = Book.objects.all()
    context = {
        "user": user,
        "books":books,
        "first_name":user.first_name,
        "last_name":user.last_name
    } 
    return render(request,"book.html",context)


def add_book(request):
    if request.method =='POST':
        user_id = request.session['user_id']

        title = request.POST['title']
        desc = request.POST['desc']

        errors = Book.objects.book_validation(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            Book.objects.create(title = title,
                                desc = desc,
                                uploaded_by  = User.objects.get(id = user_id))
        return redirect('/book')




def edit(request,id):
    book_id = id 
    if request.method =="POST":

        errors = Book.objects.book_validation(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            book_update = Book.objects.get(id = book_id)
            book_update.title = request.POST['title'] 
            book_update.desc = request.POST['desc']  
            book_update.save()
    return redirect('/details/'+ str(book_id)) 

def details(request,id):
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=id)
    context = {
        "user":user,
        'book':book
    }
    return render(request,'edit.html',context)
def add_to_fav(request, user_id, book_id):
    user = User.objects.get(id=user_id)
    book = Book.objects.get(id=book_id)
    book.liked_by.add(user)
    return redirect('/book')

def unfav(request, book_id, user_id):
    book = Book.objects.get(id = book_id)
    user = User.objects.get(id = user_id)
    book.liked_by.remove(user)
    return redirect('/details/'+ str(book_id)) 

    


                             


