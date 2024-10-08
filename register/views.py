from django.http import JsonResponse
from rest_framework.views import APIView
from .models import User, Doctor, Student, Admin
from rest_framework import status
from .serializer import UserSerializer
import json

# Create your views here.

def check_keys(expected_keys, received_keys):
    return received_keys == expected_keys
    

def error_keys(expected_keys, received_keys):
    return JsonResponse(
                {'error': 'Invalid keys in the request data.', 'expected': list(expected_keys), 'received': list(received_keys)},
                status=status.HTTP_400_BAD_REQUEST
            )


class Register(APIView):

    expected_keys_post = {'firstName', 'lastName', 'Email', 'Password'}
    expected_keys_put = {'id', 'Type'}

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        received_keys = set(data.keys())
        if not check_keys(self.expected_keys_post, received_keys):
            error_keys(self.expected_keys_post, received_keys)
        new_user = UserSerializer(data=data)
        if new_user.is_valid():
            new_user.save()
            data['id'] = new_user.data.get('id')
            return JsonResponse(data)
        return JsonResponse({'error':new_user.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = json.loads(request.body.decode('utf-8'))
        received_keys = set(data.keys())
        if not check_keys(self.expected_keys_put, received_keys):
            error_keys(self.expected_keys_put, received_keys)
        Type = data.get('Type')
        Id = data.get('id')
        user = User.objects.get(id=Id)
        user.Type = Type
        user.save()
        json_user = UserSerializer(user)
        if Type == "admin":
            user.isAdmin = True
            user.save()
            admin = Admin(user=user)
            admin.save()
            return JsonResponse(json_user.data)
        admin = Admin.objects.all().first()
        admin.requests.append(json_user.data)
        admin.save()
        return JsonResponse(json_user.data)


class LogIn(APIView):

    expected_keys = {'Email', 'Password'}
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        received_keys = set(data.keys())
        if not check_keys(self.expected_keys, received_keys):
            error_keys(self.expected_keys, received_keys)
        password = data.get('Password')
        email = data.get('Email')
        if User.objects.filter(Email=email, Password=password).exists():
            user = User.objects.get(Email=email, Password=password)
            json_user = UserSerializer(user)
            if user.isAdmin == True:
                return JsonResponse(json_user.data, status=status.HTTP_200_OK)
            if user.verify == False:
                return JsonResponse({'message':'wait until the admin check your acount'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            return JsonResponse(json_user.data)

        return JsonResponse({'message':'person is not exist'}, status=status.HTTP_400_BAD_REQUEST)
    

class GetRequests(APIView):
    def get(self, request):
        admin = Admin.objects.all().first()
        return JsonResponse(admin.requests, safe=False, status=status.HTTP_200_OK)
    

class ReplyUser(APIView):
    
    def put(self, request, pk, state):
        user = User.objects.get(id=pk)
        Type = user.Type
        if state == 1:
            user.verify = True
            user.save()
            if Type == 'doctor':
                doctor = Doctor(user=user)
                doctor.save()
            else:
                student = Student(user=user)
                student.save()
        else:
            user.delete()

        admin = Admin.objects.all().first()
        admin.requests = [element for element in admin.requests if element['id'] != pk]
        admin.save()
        return JsonResponse({'message':'success'}, status=status.HTTP_200_OK)


class GetAllUsers(APIView):

    def get(self, request):
        users = User.objects.all()
        json_users = [UserSerializer(user).data for user in users if user.verify == True]
        return JsonResponse(json_users, safe=False, status=status.HTTP_200_OK)
    

class GetProfile(APIView):
    
    def get(self, request, id):
        user = User.objects.get(id=id)
        return JsonResponse(UserSerializer(user).data, status=status.HTTP_200_OK)

class EditFirstName(APIView):

    expected_keys = {'firstName'}

    def put(self, request, id):
        data = json.loads(request.body.decode('utf-8'))
        received_keys = set(data.keys())
        if not check_keys(self.expected_keys, received_keys):
            error_keys(self.expected_keys, received_keys)

        user = User.objects.get(id=id)
        firstName = data.get('firstName')
        user.firstName = firstName
        user.save()
        return JsonResponse(UserSerializer(user).data, status=status.HTTP_200_OK)
    

class EditLastName(APIView):

    expected_keys = {'lastName'}

    def put(self, request, id):
        data = json.loads(request.body.decode('utf-8'))
        received_keys = set(data.keys())
        if not check_keys(self.expected_keys, received_keys):
            error_keys(self.expected_keys, received_keys)
        
        lastName = data.get('lastName')
        user = User.objects.get(id=id)
        user.lastName = lastName
        user.save()
        return JsonResponse(UserSerializer(user).data, status=status.HTTP_200_OK)
    

class EditPassword(APIView):

    expected_keys = {'Password'}

    def put(self, request, id):
        data = json.loads(request.body.decode('utf-8'))
        received_keys = set(data.keys())
        if not check_keys(self.expected_keys, received_keys):
            error_keys(self.expected_keys, received_keys)

        password = data.get('Password')
        user = User.objects.get(id=id)
        user.Password = password
        user.save()
        return JsonResponse(UserSerializer(user).data, status=status.HTTP_200_OK)
    

class LogOut(APIView):

    def delete(self, request, id):
        user = User.objects.get(id=id)
        user.delete()
        return JsonResponse({'message':'success'}, status=status.HTTP_200_OK)