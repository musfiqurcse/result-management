from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
# from .models.
# Create your views here.


# class UserAPI(ModelViewSet):
#     """
#            Users API endpoint
#            Users List : /api/users/datatable
#            Users List in Scheduler: /api/users/scheduler
#            Users List for all : /api/users/generic
#     """
#     lookup_field = 'id'
#     queryset = Bookings.objects.all()
#     serializer_class = BookingSerializer
#     permission_classes = (CustomSystemSettingUserPermissionCheck,)
#     permission_code = 'booking_list_'
