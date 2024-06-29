from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=300)
    email = models.EmailField(unique=True)
    profile = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    status = models.BooleanField(default=False)

    def save(self):
        self.password = make_password(self.password)
        return super().save()
    def check_password(self, password):
        return check_password(password, self.password)
    
    @staticmethod
    def getUser(id):
        return User.objects.filter(id=id)[0]

    @staticmethod
    def getUser(email, password):
        if User.objects.filter(email=email)[0]:
            user = User.objects.filter(email=email)[0]
            if user.check_password(password):
                return user
        return None
    
    def __str__(self):
        return self.username
    
class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)
    members = models.ManyToManyField(User, related_name='groups')

    @staticmethod
    def getGroup(id):
        return Group.objects.filter(id=id)[0]
    def __str__(self):
        return self.name
    

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='tasks', blank=True, null=True)

    @staticmethod
    def getTask(id):
        return Task.objects.filter(id=id)[0]
    @staticmethod
    def getTaskByOwner(owner):
        return Task.objects.filter(owner=owner)
    @staticmethod
    def getTaskByGroup(group):
        return Task.objects.filter(group=group)

    @staticmethod
    def getTaskByStatus(status):
        return Task.objects.filter(status=status)
    
    def __str__(self):
        return self.title

class subTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=[('progress', 'In Progress'), ('archive', 'Archieved'), ('done', 'Done')])
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subtasks', blank=True, null=True)
    priority = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    
    def __str__(self):
        return self.title
    
    @staticmethod
    def getTask(id):
        return subTask.objects.filter(id=id)[0]

    @staticmethod
    def getSubTaskByTask(task):
        return subTask.objects.filter(task=task)
    
    @staticmethod
    def getSubTaskByStatus(status):
        return subTask.objects.filter(status=status)
    
    @staticmethod
    def getSubTaskByAssignee(assignee):
        return subTask.objects.filter(assignee=assignee)
    
    @staticmethod
    def getSubTaskByPriority(priority):
        return subTask.objects.filter(priority=priority)

class Comment(models.Model):
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    subtask = models.ForeignKey(subTask, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):  
        return self.text