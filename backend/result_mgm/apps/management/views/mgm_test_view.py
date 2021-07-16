import csv
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from ..models.mgm_test import MgmTest
from result_mgm.apps.management.serializers.mgm_test import MgmTestSerializer
# Create your views here.
from result_mgm.apps.authentication.models.users import User
from result_mgm.apps.authentication.serializers.users import RegistrationUserSerializer
from rest_framework.decorators import action
import io
from result_mgm.apps.management.serializers.mgm_test_participant import MgmTestParticipantSerializer, MgmTestParticipant


class MgmTestAPI(ModelViewSet):

    lookup_field = 'id'
    queryset = MgmTest.objects.all()
    serializer_class = MgmTestSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        if request.user and request.user.is_superuser:
            return Response({'status': True, 'output': MgmTestSerializer(MgmTest.objects.all(),many=True).data}, status=status.HTTP_200_OK)
        elif request.user and request.user.is_teacher:
            return Response({'status': True, 'output': MgmTestSerializer(MgmTest.objects.filter(subject_id__assigned_teacher__id=request.user.id),many=True).data}, status=status.HTTP_200_OK)
        return Response({'status': False, 'output': 'Please provide valid user information to access data.'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, id=None):
        try:
            if request.user and request.user.is_superuser:
                return Response({'status': True, 'output': MgmTestSerializer(MgmTest.objects.get(id=id),many=False).data}, status=status.HTTP_200_OK)
            elif request.user and request.user.is_teacher:
                test_obj = MgmTest.objects.get(id=id, subject_id__assigned_teacher__id=request.user.id)
                test_info = MgmTestSerializer(test_obj,many=False).data
                test_info['test_participants'] = MgmTestParticipantSerializer(test_obj.test_participant_ids, many=True).data

                return Response({'status': True, 'output': test_info}, status=status.HTTP_200_OK)
            return Response({'status': False, 'output': 'Please provide valid user information to access data.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({'status': False, 'output': 'No Valid test information found'}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, id=None):
        try:
            if request.user and request.user.is_teacher:
                test_obj = MgmTest.objects.get(id=id, subject_id__assigned_teacher__id=request.user.id)
                if test_obj.test_participant_ids.count > 0 :
                    test_obj.is_archived = True
                    test_obj.save()
                    return Response({'status': True, 'output': "Test archived Successfully"}, status=status.HTTP_200_OK)
                test_obj.delete()
                return Response({'status': True, 'output': "Test deleted Successfully"}, status=status.HTTP_200_OK)
            return Response({'status': False, 'output': 'Please provide valid user information to access data.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({'status': False, 'output': 'No Valid test information found'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, id):
        try:
            if request.user and request.user.is_superuser:
                test = request.data.get('test', {})
                get_staff = MgmTest.objects.get(id=id)
                serializer = self.serializer_class(get_staff, data=test, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'result': 'success',
                        "output": serializer.data
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'result': 'error',
                        'output': {},
                        'message': serializer.errors,

                    }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            return Response({'status': False, 'output': 'No Valid User information found'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        try:
            if request.user and request.user.is_teacher:
                test = request.data.get('test', {})
                serializer = self.serializer_class(data=test)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'result': 'success',
                        "output": serializer.data
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'result': 'error',
                        'output': {},
                        'message': serializer.errors,

                    }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            return Response({'status': False, 'output': 'No Valid User information found'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'],
                detail=True,
                url_path='available-pupil',
                url_name='test-available-pupil')
    def available_pupil(self, request, id):
        try:
            if request.user and request.user.is_teacher:
                get_test = MgmTest.objects.get(id=id, is_archived=False)
                pupil_info = User.objects.filter(is_student=True).exclude(id__in=get_test.test_participant_ids.values_list('pupil_id', flat=True))
                return Response({
                    'result': 'success',
                    "output": RegistrationUserSerializer(pupil_info, many=True).data
                }, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'status': False, 'output': 'No Valid Class information found'}, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['PUT'],
            detail=True,
            url_path='result-upload',
            url_name='result-upload')
    def upload_result(self, request, id):
        try:
            if request.user and request.user.is_teacher:
                file = request.FILES.get('file_upload')
                data_set = file.read().decode('utf-8')
                io_string = io.StringIO(data_set)
                next(io_string)
                for column in csv.reader(io_string, delimiter = ',' , quotechar="|"):
                    participant_dict = {}
                    participant_dict['pupil_id'] = int(column[0])
                    participant_dict['test_id'] = id
                    participant_dict['grade'] = float(column[1])
                    existing_result = MgmTestParticipant.objects.filter(pupil_id=participant_dict['pupil_id'],test_id=participant_dict['test_id'])
                    existing_result.delete()
                    final_info = MgmTestParticipantSerializer(data=participant_dict)
                    if final_info.is_valid():
                        final_info.save()
                return Response({
                    'result': 'success',
                    "output": "success"
                }, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'status': False, 'output': 'Invalid File Submitted'}, status=status.HTTP_400_BAD_REQUEST)

