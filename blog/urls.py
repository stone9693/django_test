
from django.urls import re_path,include
from rest_framework.urlpatterns import  format_suffix_patterns
from blog import views
from rest_framework.authtoken import views as tkviews

urlpatterns=[
    re_path(r'^articles/$',views.ArticleList.as_view()),
    re_path(r'^articles/(?P<pk>[0-9]+)$',views.ArticleDetail.as_view()),
    re_path(r'^users/$',views.UserList.as_view()),
    re_path(r'^profiles/$',views.ProfileList.as_view()),
    re_path(r'api-auth/',include('rest_framework.urls')),
    re_path(r'^api-token-auth/',views.CustomAuthToken.as_view()),
]

urlpatterns=format_suffix_patterns(urlpatterns)
