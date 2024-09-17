from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from .models import Exam
from .serializer import ExamSerializer
import json
from register.models import Doctor, Student
from course.models import Course

# Create your views here.

def check_keys(expected_keys, received_keys):
    return received_keys == expected_keys


def error_keys(expected_keys, received_keys):
    return JsonResponse(
                {'error': 'Invalid keys in the request data.', 'expected': list(expected_keys), 'received': list(received_keys)},
                status=status.HTTP_400_BAD_REQUEST
            )
    

class SolveExam(APIView):
    
    expected_keys = {'studentId', 'answers'}

    def post(self, request, courseId, examId):
        data = json.loads(request.body.decode('utf-8'))
        received_keys = set(data.keys())
        if not check_keys(self.expected_keys, received_keys):
            error_keys(self.expected_keys, received_keys)

        exam = Exam.objects.get(id=examId)
        doctorId = exam.doctorId
        studentId = data['studentId']

        result = 0
        for i in range(0, len(exam.answers)):
            if exam.answers[i] == data['answers'][i]:
                result += exam.degrees[i]
        doctor = Doctor.objects.get(user__id=doctorId)
        doctor.degrees.append({'studentId':studentId, 'examId':examId, 'result':result, 'courseName':Course.objects.get(id=courseId).courseName})
        doctor.save()
        return JsonResponse({'success':'success'}, status=status.HTTP_200_OK)


class GetDoctorList(APIView):

    def get(self, request, pk):
        doctor = Doctor.objects.get(user__id=pk)
        return JsonResponse(doctor.degrees, safe=False)
    

class CorrectExam(APIView):

    expected_keys = {'doctorId', 'examId', 'studentId'}

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        received_keys = set(data.keys())
        if not check_keys(self.expected_keys, received_keys):
            error_keys(self.expected_keys, received_keys)
        doctorId = data['doctorId']
        examId = data['examId']
        studentID = data['studentId']
        doctor = Doctor.objects.get(user__id=doctorId)
        student = Student.objects.get(user__id=studentID)
        idx = 0
        for element in doctor.degrees:
            studentId = element['studentId']
            result = element['result']
            courseName = element['courseName']
            if studentId == studentID:
                student.degrees.append({'examId':examId, 'studentId':studentId, 'result':result, 'courseName':courseName})
                student.save()
                doctor.degrees.pop(idx)
                doctor.save()
                break
            idx += 1

        return JsonResponse(doctor.degrees, safe=False)
    

class GetStudentList(APIView):

    def get(self, request, pk):
        student = Student.objects.get(user__id=pk)
        return JsonResponse(student.degrees, safe=False)
        