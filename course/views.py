from django.http import JsonResponse
from .models import Course
from rest_framework import status
from rest_framework.views import APIView
from .serializer import CourseSerializer
import json
from register.models import Student, Doctor
from exam.models import Exam
from exam.serializer import ExamSerializer

# Create your views here.

def check_keys(expected_keys, received_keys):
    return received_keys == expected_keys


class GetMyCourses(APIView):

    def get(self, request, id):
        json_courses = []
        return JsonResponse(json_courses, safe=False, status=status.HTTP_200_OK)


class AddCourse(APIView):

    def post(self, request, studentId, courseId):
        student = Student.objects.get(user__id=studentId)
        course = Course.objects.get(id=courseId)
        course.registeredStudents.add(student)
        course.save()
        return JsonResponse({'message':'success'}, status=status.HTTP_200_OK)
    

class CreateCourse(APIView):

    expected_keys = {'courseName'}

    def post(self, request, doctorId):
        data = json.loads(request.body.decode('utf-8'))
        received_keys = set(data.keys())
        if not check_keys(self.expected_keys, received_keys):
            return JsonResponse(
                {'error': 'Invalid keys in the request data.', 'expected': list(self.expected_keys), 'received': list(received_keys)},
                status=status.HTTP_400_BAD_REQUEST
            )
        doctor = Doctor.objects.get(user__id=doctorId)
        courseName = data.get('courseName')
        newCourse = Course(doctor=doctor, courseName=courseName)
        newCourse.save()
        jsonNewCourse = CourseSerializer(newCourse)
        return JsonResponse(jsonNewCourse.data, status=status.HTTP_200_OK)
    

class AddExam(APIView):

    expected_keys = {'doctorId', 'questions', 'degrees', 'answers'}

    def put(self, request, courseId):
        data = json.loads(request.body.decode('utf-8'))
        received_keys = set(data.keys())
        if not check_keys(self.expected_keys, received_keys):
            return JsonResponse(
                {'error': 'Invalid keys in the request data.', 'expected': list(self.expected_keys), 'received': list(received_keys)},
                status=status.HTTP_400_BAD_REQUEST
            )
        newExam = ExamSerializer(data=data)
        if newExam.is_valid():
            newExam.save()
            course = Course.objects.get(id=courseId)
            course.contents.append(newExam.data)
            course.save()
            jsonCourse = CourseSerializer(course)
            return JsonResponse(jsonCourse.data, status=status.HTTP_200_OK)
        
        return JsonResponse({'error':newExam.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class AddLecture(APIView):

    expected_keys = {'session'}

    def put(self, request, courseId):
        data = json.loads(request.body.decode('utf-8'))
        received_keys = set(data.keys())
        if not check_keys(self.expected_keys, received_keys):
            return JsonResponse(
                {'error': 'Invalid keys in the request data.', 'expected': list(self.expected_keys), 'received': list(received_keys)},
                status=status.HTTP_400_BAD_REQUEST
            )
        session = data.get('session')
        course = Course.objects.get(id=courseId)
        course.contents.append(session)
        course.save()
        jsonCourse = CourseSerializer(course)
        return JsonResponse(jsonCourse.data, status=status.HTTP_200_OK)