
from rest_framework import serializers
from blog.models import Article,ArticleUser,Profile
from django.contrib.auth import get_user_model

User=get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=('username','email')
        read_only_fields=['id',]

class ProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Profile
        fields=['id','addr','user']
        read_only_fields=['id']
    def create(self, validated_data):
        user_data=validated_data.pop('user')
        user=User.objects.create(**user_data)
        Profile.objects.create(user=user,**validated_data)
        return user


class ArticleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=ArticleUser
        fields='__all__'



class ArticleSerializer(serializers.ModelSerializer):

    cn_status=serializers.SerializerMethodField()
    # authors=serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),many=True)
    authors=serializers.SerializerMethodField(read_only=True)
    create_date=serializers.DateTimeField('%Y-%m-%d %H:%M:%S',read_only=True)
    class Meta:
        model=Article
        fields=['id','cn_status','title','body','create_date','authors','status']
        read_only_fields=['id','create_date','cn_status','authors']
    def get_cn_status(self,obj):
        if obj.status=='p':
            return '已出版'
        elif obj.status=='d':
            return '草稿'
        else:
            return ''
    def get_authors(self,obj):
        article_id_queryset=ArticleUser.objects.filter(article_id=obj.id)
        data_list=[info_dict.user_id for info_dict in article_id_queryset]
        return data_list
    def validate(self,data):
        accept_title_list=['redis','django','python','mysql']
        is_title_in=False
        is_title_name = data['title']
        for title_name in accept_title_list:
            if title_name in data['title'].lower():
                is_title_in=True

        if not is_title_in:
            raise serializers.ValidationError(f'{is_title_name} not in title')
        return data

