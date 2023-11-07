from django.db import models
from django.utils.translation import ugettext_lazy as ugl
from django.contrib.auth import get_user_model
# Create your models here.

User=get_user_model()

class Article(models.Model):
    STATUS_CHOICES=(('p',ugl('Published')),('d',ugl('Draft')),)
    title=models.CharField(verbose_name=ugl('Title(*)'),max_length=90,db_index=True)
    body=models.TextField(verbose_name=ugl('Body'),blank=True)
    status=models.CharField(ugl('Status(*)'),max_length=1,choices=STATUS_CHOICES,default='s',null=True,blank=True)
    create_date=models.DateTimeField(verbose_name=ugl('Create Date'),auto_now_add=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering=['-create_date']
        verbose_name='Article'
        verbose_name_plural='Articles'
        db_table='blog_article_info'

class ArticleUser(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.DO_NOTHING,db_column='user_id')
    article=models.ForeignKey(to=Article,on_delete=models.DO_NOTHING,db_column='article_id')
    class Meta:
        db_table='blog_article_user'

class Profile(models.Model):
    addr=models.TextField(blank=True,null=True)
    user=models.ForeignKey(to=User,on_delete=models.DO_NOTHING,db_column='user_id')
    class Meta:
        db_table='blog_user_profile'
