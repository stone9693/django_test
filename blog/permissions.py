
from rest_framework import permissions
from blog.models import ArticleUser
class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        article_user_queryset=ArticleUser.objects.filter(article_id=obj.id)
        article_user_list=[info.user_id for info in article_user_queryset]
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.id in article_user_list