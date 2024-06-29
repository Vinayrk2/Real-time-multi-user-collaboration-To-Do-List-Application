from django.shortcuts import render, HttpResponse
from appModels.models import User, Group

# Create your views here.
def home(request):
    if "username" in request.session:
        user = User.getUserByUsername(request.session['username'])
        groups = Group.getGroupsByUser(user.id)
        print(groups)
        return render(request, "home.html", {"groups":groups})
    return render(request, "home.html")

def create_group(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        if name != "" and description != "":
            user = User.getUserByUsername(request.session['username'])
            group = Group(name=name, description=description)
            group.owner = user
            group.members.add(user)
            group.save()
            return HttpResponse("Group created successfully.")
    return HttpResponse("There is an error in creating the group, please try again later.")

def join_group(request,id):
    if request.method == "GET":
        group_id = request.POST.get("id")
        try:
            if group_id != "":
                user = User.getUserByUsername(request.session['username'])
                group = Group.objects.get(id=group_id)
                group.members.add(user)
                group.save()
                return HttpResponse("You have joined the group successfully.")
        except Exception as e:
            return HttpResponse("It Seems you have already joined the group")
    return HttpResponse("There is an error in joining the group, please try again later.")

def group_page(request,id):
    group = Group.objects.get(id=id)
    return render(request, "group.html", {"group":group})