from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import TeamMember
from django.contrib import messages
from django.http import HttpResponse


def index(req):
  mems = TeamMember.objects.all()
  return render(req, 'index.html', {'mems': mems})

def admindashboard(req):
  if req.user.is_authenticated:
    userfirstname = req.user.first_name
    return render(req, 'admindashboard.html', {'user_first_name': userfirstname})
  else:
    return HttpResponse("<h1>Please Authenticate to access this page!!!</h1><a href='../login'>Login Here</a>")

def addMember(request):
  if request.method == "POST":
    name = request.POST['name']
    email = request.POST['email']
    domain = request.POST['domain']
    description = request.POST['description']
    category = request.POST['category']
    if TeamMember.objects.filter(email=email).exists():
      messages.info(request, 'Email already in use')
      return redirect('admindashboard')
    mem = TeamMember()
    try:
      profile_pic = request.FILES['profile_pic']
      github = request.POST['github']
      linkedin = request.POST['linkedin']
      mem.img = profile_pic
      mem.github = github
      mem.linkedin = linkedin
    except:
      pass
    mem.name = name
    mem.email = email
    mem.domain = domain
    mem.desc = description
    if category == 'management':
      mem.tech = False
      mem.management = True
    else:
      mem.tech = True
      mem.management = False
    mem.save()
    messages.info(request, "Added Member Successfully")
    return redirect('/admindashboard')


def login(request):
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      return redirect("/admindashboard/")
    else:
      messages.info(request, "Invalid credentials")
      return redirect('login')
    
  else:
    if request.user.is_authenticated:
      return redirect('/admindashboard')
    return render(request, 'login.html')

def logout(request):
  auth.logout(request)
  return redirect("/")

def register(request):
  if request.method == "POST":
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    email = request.POST['email']

    if password1 == password2:
      if User.objects.filter(username=username).exists():
        messages.info(request, 'Username already in use')
        return redirect('register')
      elif User.objects.filter(email=email).exists():
        messages.info(request, 'Email already in use')
        return redirect('register')
      else:
        user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
        user.save()
        print("user created")
        messages.info(request, "User Registered Successfully")
        return redirect('/login')
    
    else:
      messages.info(request, 'Passwords Doesnot match')
      return redirect('register')
    
  else:
    if request.user.is_authenticated:
      return render(request, 'register.html')
    else:
      return HttpResponse("<h1>Please Authenticate to access this page!!!</h1><a href='../login'>Login Here</a>")
  

def delete(request):
  if request.method == "POST":
    email = request.POST['email']
    TeamMember.objects.filter(email=email).delete()
    messages.info(request, 'Deletetion Performed!!')
    return redirect('/')
  else:
    if request.user.is_authenticated:
      mems = TeamMember.objects.all()
      return render(request, 'delete.html', {'mems': mems})
    else:
      return HttpResponse("<h1>Please Authenticate to access this page!!!</h1><a href='../login'>Login Here</a>")
    

def members(req, id):
  mem = TeamMember.objects.get(id=id)
  return render(req, 'member.html', {'mem': mem})

def update(request):
  if request.method == "POST":
    verifymail = request.POST['verifymail']
    try:
      mem = TeamMember.objects.get(email=verifymail)
    except:
      messages.info(request, 'Email Not found')
      return redirect('update')
    else:
      try:
        name = request.POST['name']
        if name != '':
          mem.name = name
      except:
        pass

      try:
        email = request.POST['email']
        if email != '':
          mem.email = email
      except:
        pass

      try:
        domain = request.POST['domain']
        if domain != '':
          mem.domain = domain
      except:
        pass
      
      try:
        description = request.POST['description']
        if description != '':
          mem.desc = description
      except:
        pass
      
      try:
        category = request.POST['category']
        if category == 'management':
          mem.tech = False
          mem.management = True
        if category == 'tech':
          mem.tech = True
          mem.management = False
      except:
        pass

      try:
        profile_pic = request.FILES['profile_pic']
        if profile_pic != '':
          print(profile_pic)
          mem.img = profile_pic
          print(mem.img)
      except:
        pass

      try:
        github = request.POST['github']
        print(github)
        if github != '':
          mem.github = github
      except:
        pass

      try:
        linkedin = request.POST['linkedin']
        print(linkedin)
        if mem.linkedin != '':
          mem.linkedin = linkedin
      except:
        pass
      print(mem.name)
      mem.save()
      messages.info(request, "Successfully Updated!!!")
      return redirect('/')
  else:
    if request.user.is_authenticated:
      mems = TeamMember.objects.all()
      return render(request, 'update.html', {'mems': mems})
    else:
      return HttpResponse("<h1>Please Authenticate to access this page!!!</h1><a href='../login'>Login Here</a>")