from rest_framework import serializers
from django.contrib.auth import authenticate
from django.conf import settings
from ..models.mgm_test_participant import MgmTestParticipant
from django.utils.translation import gettext as _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from rest_framework.exceptions import NotFound


class MgmTestParticipantSerializer(serializers.ModelSerializer):
    pupil_name = serializers.SerializerMethodField()
    teacher_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    test_name = serializers.SerializerMethodField()


    def get_pupil_name(self,obj):
        return obj.pupil_id.name
    def get_teacher_name(self,obj):
        return obj.test_id.subject_id.assigned_teacher.name
    def get_subject_name(self,obj):
        return obj.test_id.subject_id.name

    def get_test_name(self,obj):
        return obj.test_id.name

    class Meta:
        model = MgmTestParticipant
        fields = ['test_id',
                  'id',
                  'pupil_id',
                  'pupil_name',
                  'teacher_name',
                  'subject_name',
                  'test_name',
                  'grade'
                  ]