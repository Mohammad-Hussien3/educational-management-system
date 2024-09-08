from django.http import JsonResponse
from .models import Course
from rest_framework import status
from rest_framework.views import APIView
from .serializer import CourseSerializer
import json
from register.models import Doctor

# Create your views here.

def check_keys(expected_keys, received_keys):
    return received_keys == expected_keys


class GetAllCourses(APIView):

    def get(self, request, pk):
        courses = Course.objects.all()
        myCourses = []
        doctor = Doctor.objects.get(user__id=pk)
        myCourses = [course for course in doctor.courses.all()]
        newCourses = [{'id':CourseSerializer(course).data['id'], 'courseName':CourseSerializer(course).data['courseName']}
                       for course in courses if myCourses.count(course) == 0]
            
        return JsonResponse(newCourses, safe=False, status=status.HTTP_200_OK)
    

class GetMyCourses(APIView):

    def get(self, request, pk):
        doctor = Doctor.objects.get(user__id=pk)
        json_courses = [{'id':CourseSerializer(course).data['id'], 'courseName':CourseSerializer(course).data['courseName']}
                        for course in doctor.courses.all()]
        return JsonResponse(json_courses, safe=False, status=status.HTTP_200_OK)


class AddCourse(APIView):

    expected_keys = {'courseId'}

    def post(self, request, doctorId):
        data = json.loads(request.body.decode('utf-8'))
        received_keys = set(data.keys())
        if not check_keys(self.expected_keys, received_keys):
            return JsonResponse(
                {'error': 'Invalid keys in the request data.', 'expected': list(self.expected_keys), 'received': list(received_keys)},
                status=status.HTTP_400_BAD_REQUEST
            )
        courseId = data.get('courseId')
        doctor = Doctor.objects.get(user__id=doctorId)
        doctor.courses.add(Course.objects.get(id=courseId))
        return JsonResponse({'message':'success'}, status=status.HTTP_200_OK)
