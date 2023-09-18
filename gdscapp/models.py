from django.db import models

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics', default='pics/user.png')
    email = models.EmailField(default='test@gmail.com')
    desc = models.TextField()
    linkedin = models.URLField(default='https://linkedin.com')
    github = models.URLField(default='https://github.com')
    domain = models.TextField(max_length=40, default='lead')
    tech = models.BooleanField(default=False)
    management = models.BooleanField(default=False)