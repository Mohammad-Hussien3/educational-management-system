from django.http import JsonResponse
from rest_framework import status
from .models import Article
from rest_framework.views import APIView
from .serializer import ArticleSerializer
import json
from register.models import User

# Create your views here.

def check_keys(expected_keys, received_keys):
    return received_keys == expected_keys


class GetArticles(APIView):

    def get(self, request):
        articles = Article.objects.all()
        json_articles = [ArticleSerializer(article).data for article in articles]
        return JsonResponse(json_articles, safe=False, status=status.HTTP_200_OK)
    

class AddArticle(APIView):

    expected_keys = {'doctorId', 'title', 'subject'}

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        received_keys = set(data.keys())
        if not check_keys(self.expected_keys, received_keys):
            return JsonResponse(
                {'error': 'Invalid keys in the request data.', 'expected': list(self.expected_keys), 'received': list(received_keys)},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_article = ArticleSerializer(data=data)
        if new_article.is_valid():
            new_article.save()
        doctorId = data.get('doctorId')
        doctor = User.objects.get(id=doctorId)
        data['id'] = new_article.data.get('id')
        data['name'] = doctor.firstName + ' ' + doctor.lastName
        data['email'] = doctor.Email
        return JsonResponse(data, status=status.HTTP_200_OK)
