from rest_framework import serializers
from news.models import Article, Journalist
from rest_framework.serializers import ModelSerializer
from datetime import datetime
from django.utils.timesince import timesince
from datetime import date

class ArticleSerializer(ModelSerializer):

    publishedSince = serializers.SerializerMethodField()
    #author = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = "__all__"
        #fields = ["title","author","description"]
        #exclude = ["title"]
        read_only_fields = ["id","created_time","updated_time"] 

    def get_publishedSince(self, object):
        timeNow = datetime.now()
        print(f"TIME NOW = {timeNow}")
        publishedTime = object.published_date
        timeDelta = timesince(publishedTime,timeNow)
        return timeDelta
    
    def validate_published_date(self,date):
        today = date.today()
        print(f"TODAY DATE = {today}")
        if date > today:
         raise serializers.ValidationError("The date has not come yet!")
        return date
    

class JournalistSerializer(ModelSerializer):
    #articles = ArticleSerializer(read_only=True,many=True)
    articles = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="article/details"
    )
    class Meta: 
        model = Journalist
        fields = "__all__"


class ArticleSerializerDefault(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    main_text = serializers.CharField()
    published_date = serializers.DateField()
    is_active = serializers.BooleanField()
    created_date = serializers.DateTimeField(read_only=True)
    updated_date = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        return Article.objects.create(**validated_data)
    #As we know validated_data is dictonary, to extract it we used double **.
    
    def update(self, instance,validated_data):
        instance.author = validated_data.get('author',instance.author)
        instance.title = validated_data.get('title', instance.title) 
        instance.description = validated_data.get('description',instance.description)
        instance.main_text = validated_data.get('main_text', instance.main_text)
        instance.published_date = validated_data.get('published_date',instance.published_date)
        instance.is_active = validated_data.get('is_active',instance.is_active)
        instance.save()
        return instance
    
    def validate(self, data):
        if data['title'] == data['description']:
            raise serializers.ValidationError('Title and Description cannot be same.')
        return data
    
    def validate_title(self,title):
        titleLength = len(title)
        if titleLength < 8:
            raise serializers.ValidationError(f"Title must be minimum 8 characters, You wrote only {titleLength} characters.")
        return title