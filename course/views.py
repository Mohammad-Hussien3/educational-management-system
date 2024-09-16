from django.http import JsonResponse
from .models import Course
from rest_framework import status
from rest_framework.views import APIView
from .serializer import CourseSerializer
import json
from register.models import Student, Doctor
from exam.serializer import ExamSerializer

# Create your views here.

def check_keys(expected_keys, received_keys):
    return received_keys == expected_keys


def error_keys(expected_keys, received_keys):
    return JsonResponse(
                {'error': 'Invalid keys in the request data.', 'expected': list(expected_keys), 'received': list(received_keys)},
                status=status.HTTP_400_BAD_REQUEST
            )


class GetMyCourses(APIView):

    def get(self, request, id):
        json_courses = []
        if Student.objects.filter(user__id=id):
            student = Student.objects.get(user__id=id)
            for course in student.courses.all():
                json_courses.append(CourseSerializer(course).data)
            return JsonResponse(json_courses, safe=False, status=status.HTTP_200_OK)

        doctor = Doctor.objects.get(user__id=id)
        for course in doctor.courses.all():
            json_courses.append(CourseSerializer(course).data)
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
            error_keys(self.expected_keys, received_keys)
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
            error_keys(self.expected_keys, received_keys)
        newExam = ExamSerializer(data=data)
        if newExam.is_valid():
            newExam.save()
            course = Course.objects.get(id=courseId)
            course.contents.append([{'isExam':True}, newExam.data])
            course.save()
            jsonCourse = CourseSerializer(course)
            return JsonResponse(jsonCourse.data, status=status.HTTP_200_OK)
        
        return JsonResponse({'error':newExam.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class AddLecture(APIView):

    expected_keys = {'lecture'}

    def put(self, request, courseId):
        data = json.loads(request.body.decode('utf-8'))
        received_keys = set(data.keys())
        if not check_keys(self.expected_keys, received_keys):
            error_keys(self.expected_keys, received_keys)
        session = data.get('lecture')
        course = Course.objects.get(id=courseId)
        course.contents.append([{'isExam':False}, {'lecture':session}])
        course.save()
        jsonCourse = CourseSerializer(course)
        return JsonResponse(jsonCourse.data, status=status.HTTP_200_OK)
    

class GetPage(APIView):

    def get(self, request, courseId, studentId, pageIndex):
        course = Course.objects.get(id=courseId)
        pageNumber = course.latestPage[0][str(studentId)]
        if pageIndex > len(course.contents):
            return JsonResponse([{'isExam':False}, {'lecture':'finish'}], status=status.HTTP_200_OK)
        elif pageIndex > pageNumber:
            pageNumber = pageIndex
            course.latestPage[0][str(studentId)] = pageNumber
            course.save()
        elif pageIndex != 0:
            pageNumber = pageIndex
        jsonData = course.contents[pageNumber - 1].copy()
        jsonData[0]['pageIndex'] = pageNumber
        jsonData[0]['id'] = course.id
        jsonData[0]['courseName'] = course.courseName
        return JsonResponse(jsonData, safe=False, status=status.HTTP_200_OK)
    

class GetCourses(APIView):
    
    def get(self, request, studentId):
        allCourses = Course.objects.all()
        jsonCourses = []
        myCourse = Student.objects.get(user__id=studentId).courses.all()
        myCourse = [course.id for course in myCourse]
        print(myCourse)
        print(allCourses)
        for course in allCourses:
            if not course.id in myCourse:
                jsonCourses.append(CourseSerializer(course).data)
        return JsonResponse(jsonCourses, safe=False, status=status.HTTP_200_OK)
    

class CourseRegister(APIView):

    def put(self, request, courseId, studentId):
        doctor = Course.objects.get(id=courseId).doctor
        doctor.courseRequest.append({'courseId':courseId, 'studentId':studentId})
        doctor.save()
        return JsonResponse({'message':'success'}, status=status.HTTP_200_OK)


class GetAllRegisterRequests(APIView):

    def get(self, requests, doctorId):
        jsonRequests = Doctor.objects.get(user__id=doctorId).courseRequest
        return JsonResponse(jsonRequests, safe=False, status=status.HTTP_200_OK)
    

class AcceptRegisterRequest(APIView):

    def put(self, request, courseId, studentId):
        course = Course.objects.get(id=courseId)
        doctor = course.doctor
        doctor.courseRequest.remove({'courseId':courseId, 'studentId':studentId})
        doctor.save()
        course.registeredStudents.add(Student.objects.get(user__id=studentId))
        course.latestPage[0][str(studentId)] = 1
        course.save()
        return JsonResponse({'message':'success'}, status=status.HTTP_200_OK)