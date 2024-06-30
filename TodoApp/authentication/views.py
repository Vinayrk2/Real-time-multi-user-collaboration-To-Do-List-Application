from django.shortcuts import render, HttpResponsePermanentRedirect, HttpResponse
from appModels.models import User


# Create your views here.
def login(request):

    if request.session.get('username') != None:
        return HttpResponsePermanentRedirect('/')

    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = User.getUser(email, password)
            if user : 
                request.session['username'] = user.username
                # request.session['user_id'] = user.id
                request.session['email'] = user.email
                return HttpResponsePermanentRedirect('/todo/')
            else : 
                return HttpResponse('Invalid password')
        except:
            return HttpResponse('Invalid username or password')
    return render(request, 'login.html')

def signup(request):


    if request.session.get('username'):
        return HttpResponsePermanentRedirect('/')

    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            
            user = User()
            user.username = username
            user.password = password
            user.email = email
            user.save()
            return HttpResponsePermanentRedirect('/auth/login')

        except Exception as e:
            return HttpResponse(e)

    return render(request,'signup.html')

def logout(request):
    request.session.flush()
    return HttpResponsePermanentRedirect('/auth/login')
