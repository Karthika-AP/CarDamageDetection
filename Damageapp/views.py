# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST
from requests.auth import HTTPBasicAuth
from django.utils.datastructures import MultiValueDictKeyError
from urllib.error import HTTPError
from django.db import IntegrityError
from requests import ConnectionError
from rest_framework.views import APIView
from pathlib import Path
import os
import glob
import ntpath
import shutil, errno
import re
import yaml
import xml.etree.cElementTree as ET
import os
import secrets
import shutil
import string

from .scripts import Damage


#@ensure_csrf_cookie
@csrf_exempt
@require_POST
def front(request):
  try:
    if request.method=='POST':
          json_data=json.loads(request.body)
          folderpath=json_data["folderpath"]
          print(folderpath)
          filename=json_data["filename"]
          print(filename)
          view=json_data["view"]
          print(view)
          
    if(view=='Front'):
      
      result=[]
      front_result=[]
      f_result=[]
      
      boolean_is_car, prediction_car = Damage.predict_car(view)
      if boolean_is_car:        
        boolean_is_front, prediction_front = Damage.predict_front()
        if boolean_is_front:
          boolean_hood_engine, prediction_hood = Damage.predict_hood()
          boolean_bumper_front, prediction_bumper = Damage.predict_bumper()
          boolean_windshield_frontglass, prediction_windshield = Damage.predict_windshield()
          f_result.append(dict(is_hood=boolean_hood_engine, prediction_hood=prediction_hood, is_bumper=boolean_bumper_front, prediction_bumper=prediction_bumper, is_frontglass=boolean_windshield_frontglass, prediction_windshield=prediction_windshield))
        front_result.append(dict(damaged=boolean_is_front, front_prediction=prediction_front, types=f_result))
      result.append(dict(image=filename, is_car=boolean_is_car, is_prediction=prediction_car, is_front=front_result))
      print(result)

      response = JsonResponse(result, safe=False)
      response["Access-Control-Allow-Origin"] = "*"
      response["Access-Control-Allow-Credentials"] = "true"
      response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
      response["Access-Control-Max-Age"] = "3600"
      response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
      return response
    
  except HTTPError:
        context = {
            "message": "Error Revisit the code"
        }
        response = JsonResponse(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
        return response

@ensure_csrf_cookie
@csrf_exempt
@require_POST
def rear(request):
  try:
    if request.method=='POST':
          json_data=json.loads(request.body)
          folderpath=json_data["folderpath"]
          print(folderpath)
          filename=json_data["filename"]
          print(filename)
          view=json_data["view"]
          print(view)
          
    if(view=='Rear'):
      
      result=[]
      rear_result=[]
      r_result=[]
      
      boolean_is_car, prediction_car = Damage.predict_car(view)
      if boolean_is_car:        
        boolean_is_rear, prediction_rear = Damage.predict_rear()
        if boolean_is_rear:
          boolean_boot_storage, prediction_storage = Damage.predict_boot()
          boolean_bumper_rear, prediction_rear = Damage.predict_bumper_rear()
          boolean_windshield_rearglass,  prediction_rearglass = Damage.predict_windshield_rear()
          r_result.append(dict(is_boot=boolean_boot_storage, prediction_storage=prediction_storage, is_bumper=boolean_bumper_rear, prediction_rear=prediction_rear, is_rearglass=boolean_windshield_rearglass, prediction_rearglass=prediction_rearglass))
        rear_result.append(dict(damaged=boolean_is_rear, prediction_rear=prediction_rear, types=r_result))
      result.append(dict(image=filename, is_car=boolean_is_car, is_prediction=prediction_car, is_rear=rear_result))
      print(result)

      response = JsonResponse(result, safe=False)
      response["Access-Control-Allow-Origin"] = "*"
      response["Access-Control-Allow-Credentials"] = "true"
      response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
      response["Access-Control-Max-Age"] = "3600"
      response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
      return response
    
  except HTTPError:
        context = {
            "message": "Error Revisit the code"
        }
        response = JsonResponse(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
        return response

@ensure_csrf_cookie
@csrf_exempt
@require_POST
def left(request):
  try:
    if request.method=='POST':
          json_data=json.loads(request.body)
          folderpath=json_data["folderpath"]
          print(folderpath)
          filename=json_data["filename"]
          print(filename)
          view=json_data["view"]
          print(view)
          
    if(view=='Left'):
      
      result=[]
      left_result=[]
      l_result=[]
      
      boolean_is_car, prediction_car = Damage.predict_car(view)
      if boolean_is_car:        
        boolean_is_left, prediction_left = Damage.predict_side_left()
        if boolean_is_left:
          boolean_window_left, prediction_window = Damage.predict_window_left()
          boolean_door_left, prediction_door = Damage.predict_door_left()
          l_result.append(dict(is_window=boolean_window_left, prediction_window=prediction_window, is_door=boolean_door_left, prediction_door=prediction_door))
        left_result.append(dict(damaged=boolean_is_left, prediction_left=prediction_left, types=l_result))
      result.append(dict(image=filename, is_car=boolean_is_car, is_prediction=prediction_car, is_left=left_result))
      print(result)

      response = JsonResponse(result, safe=False)
      response["Access-Control-Allow-Origin"] = "*"
      response["Access-Control-Allow-Credentials"] = "true"
      response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
      response["Access-Control-Max-Age"] = "3600"
      response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
      return response
    
  except HTTPError:
        context = {
            "message": "Error Revisit the code"
        }
        response = JsonResponse(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
        return response

@ensure_csrf_cookie
@csrf_exempt
@require_POST
def right(request):
  try:
    if request.method=='POST':
          json_data=json.loads(request.body)
          folderpath=json_data["folderpath"]
          print(folderpath)
          filename=json_data["filename"]
          print(filename)
          view=json_data["view"]
          print(view)
          
    if(view=='Right'):
      
      result=[]
      right_result=[]
      ri_result=[]
      
      boolean_is_car, prediction_car = Damage.predict_car(view)
      if boolean_is_car:        
        boolean_is_right, prediction_right = Damage.predict_side_right()
        if boolean_is_right:
          boolean_window_right, prediction_window = Damage.predict_window_right()
          boolean_door_right, prediction_door = Damage.predict_door_right()
          ri_result.append(dict(is_window=boolean_window_right, prediction_window=prediction_window, is_door=boolean_door_right, prediction_door=prediction_door))
        right_result.append(dict(damaged=boolean_is_right, prediction_right=prediction_right, types=ri_result))
      result.append(dict(image=filename, is_car=boolean_is_car, is_prediction=prediction_car, is_right=right_result))
      print(result)

      response = JsonResponse(result, safe=False)
      response["Access-Control-Allow-Origin"] = "*"
      response["Access-Control-Allow-Credentials"] = "true"
      response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
      response["Access-Control-Max-Age"] = "3600"
      response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
      return response
    
  except HTTPError:
        context = {
            "message": "Error Revisit the code"
        }
        response = JsonResponse(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
        return response


      
