from django.db import models

# Create your models here.
class USER_DATA(models.Model):
    user_id=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
class COMMENT_USER(models.Model):
    comment_id=models.CharField(max_length=20)
    user_id=models.CharField(max_length=20)
    admin_id=models.CharField(max_length=20)
class USER_ISSUES(models.Model):
    issue_id=models.CharField(max_length=20)
    user_id=models.CharField(max_length=20)
class TITLE_BODY(models.Model):
    title=models.CharField(max_length=50)
    body=models.CharField(max_length=10000)
    issue_id=models.CharField(max_length=20)
    user_id=models.CharField(max_length=20)