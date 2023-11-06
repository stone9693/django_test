from django.contrib import admin

from blog.models import Article,ArticleUser
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','status','create_date')
    list_filter = ('status',)
    list_per_page = 10

class ArticleUserAdmin(admin.ModelAdmin):
    list_display = ('article_id','user_id')
    list_per_page = 10

admin.site.register(Article,ArticleAdmin)
admin.site.register(ArticleUser,ArticleUserAdmin)