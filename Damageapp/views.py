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

from .scripts.CarDamage import *
from .scripts import CarDamageEdited
from .scripts.extras import handle_uploaded_file


@ensure_csrf_cookie
@csrf_exempt
@require_POST
def prediction(request):
  try:
    if request.method == 'POST':            
            file_front = request.FILES['accident_front']
            print(file_front)
            print("hey")
            print(type(file_front))
            file_rear = request.FILES['accident_rear']
            print(file_rear)
            file_left = request.FILES['accident_left']
            print(file_left)
            file_right = request.FILES['accident_right']
            print(file_right)
            
            al = string.ascii_letters + string.digits
            k = 8
            
            accident_front = "".join(secrets.SystemRandom().choices(al, k=k)) + file_front.name
            accident_rear = "".join(secrets.SystemRandom().choices(al, k=k)) + file_rear.name
            accident_left = "".join(secrets.SystemRandom().choices(al, k=k)) + file_left.name
            accident_right = "".join(secrets.SystemRandom().choices(al, k=k)) + file_right.name

            print(accident_front)
            print(type(accident_front))
            print(accident_rear)
            print(accident_left)
            print(accident_right)

            handle_uploaded_file(file_front, "front", accident_front)
            handle_uploaded_file(file_rear, "rear", accident_rear)
            handle_uploaded_file(file_left, "left", accident_left)
            handle_uploaded_file(file_right, "right", accident_right)

            boolean_is_car = False
            boolean_is_car = is_car()
            if not boolean_is_car:
                print("Not a CAR - ######## Upload Image of a car")
                context = {
                    "message": "Please upload Images of a Car"
                  }
                response = JsonResponse(context, safe=False)
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Credentials"] = "true"
                response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
                response["Access-Control-Max-Age"] = "3600"
                response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
                return response
            else:
                boolean_hood_engine,boolean_bumper_front,boolean_bumper_rear,boolean_windshield_frontglass,boolean_windshield_rearglass=(False for i in range(5))
                boolean_boot_storage,boolean_window_left,boolean_window_right,boolean_door_left,boolean_door_right=(False for i in range(5))
                
                if is_front():
                    boolean_hood_engine = is_hood()
                    boolean_bumper_front = is_bumper()
                    boolean_windshield_frontglass = is_windshield()
                if is_side('left'):
                    boolean_window_left = is_window('left')
                    boolean_door_left = is_door('left')
                if is_side('right'):
                    boolean_window_right = is_window('right')
                    boolean_door_right = is_door('right')
                if is_rear():
                    boolean_boot_storage = is_boot()
                    boolean_bumper_rear = is_bumper_rear()
                    boolean_windshield_rearglass = is_windshield_rear()

                
                    
                if any([boolean_hood_engine,boolean_bumper_front,boolean_windshield_frontglass,boolean_window_left,boolean_door_left,
                        boolean_window_right,boolean_door_right,boolean_boot_storage,boolean_bumper_rear,boolean_windshield_rearglass]):
                  print("Damage")
                  print(boolean_hood_engine,boolean_bumper_front,boolean_windshield_frontglass,boolean_window_left,boolean_door_left,
                        boolean_window_right,boolean_door_right,boolean_boot_storage,boolean_bumper_rear,boolean_windshield_rearglass)

                  result=[]
                  
                  ka = []
                  ka.append(str(boolean_hood_engine))
                  ka.append(str(boolean_bumper_front))
                  ka.append(str(boolean_windshield_frontglass))
                  ka.append(str(boolean_window_left))
                  ka.append(str(boolean_door_left))
                  ka.append(str(boolean_window_right))
                  ka.append(str(boolean_door_right))
                  ka.append(str(boolean_boot_storage))
                  ka.append(str(boolean_bumper_rear))
                  ka.append(str(boolean_windshield_rearglass))
                  result.append(ka)

                  FinalResult=[]
                  for a,b,c,d,e,f,g,h,i,j in result:
                      FinalResult.append(dict(boolean_hood_engine=a, boolean_bumper_front=b, boolean_windshield_frontglass=c,
                                              boolean_window_left=d, boolean_door_left=e, boolean_window_right=f, boolean_door_right=g, boolean_boot_storage=h,
                                              boolean_bumper_rear=i, boolean_windshield_rearglass=j))    

                  response = JsonResponse(FinalResult, safe=False)
                  response["Access-Control-Allow-Origin"] = "*"
                  response["Access-Control-Allow-Credentials"] = "true"
                  response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
                  response["Access-Control-Max-Age"] = "3600"
                  response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
                  return response
                    
                else:
                  print("No Damage")

                  context = {
                    "message": "Hurray!!! Your Car has No Damage"
                  }
                  response = JsonResponse(context, safe=False)
                  response["Access-Control-Allow-Origin"] = "*"
                  response["Access-Control-Allow-Credentials"] = "true"
                  response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
                  response["Access-Control-Max-Age"] = "3600"
                  response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
                  return response

  except HTTPError:
                context = {
                    "message": "Internal Server Error 500. Please check with Tools Team"
                }
                response = JsonResponse(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Credentials"] = "true"
                response["Access-Control-Allow-Methods"] = "POST, GET, PUT, OPTIONS, DELETE"
                response["Access-Control-Max-Age"] = "3600"
                response["Access-Control-Allow-Headers"] = "X-Remote-User,X-Impersonate-User,X-Requested-With, Content-Type, Authorization, Origin, Accept, Access-Control-Request-Method, Access-Control-Request-Headers"
                return response


@ensure_csrf_cookie
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
      
      boolean_is_car = CarDamageEdited.is_car(view)
      if boolean_is_car:        
        boolean_is_front = CarDamageEdited.is_front()
        if boolean_is_front:
          boolean_hood_engine = CarDamageEdited.is_hood()
          boolean_bumper_front = CarDamageEdited.is_bumper()
          boolean_windshield_frontglass = CarDamageEdited.is_windshield()
          f_result.append(dict(is_hood=boolean_hood_engine, is_bumper=boolean_bumper_front, is_frontglass=boolean_windshield_frontglass))
        front_result.append(dict(damaged=boolean_is_front, types=f_result))
      result.append(dict(image=filename, is_car=boolean_is_car, is_front=front_result))
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
      
      boolean_is_car = CarDamageEdited.is_car(view)
      if boolean_is_car:        
        boolean_is_rear = CarDamageEdited.is_rear()
        if boolean_is_rear:
          boolean_boot_storage = CarDamageEdited.is_boot()
          boolean_bumper_rear = CarDamageEdited.is_bumper_rear()
          boolean_windshield_rearglass = CarDamageEdited.is_windshield_rear()
          r_result.append(dict(is_boot=boolean_boot_storage, is_bumper=boolean_bumper_rear, is_rearglass=boolean_windshield_rearglass))
        rear_result.append(dict(damaged=boolean_is_rear, types=r_result))
      result.append(dict(image=filename, is_car=boolean_is_car, is_rear=rear_result))
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
      
      boolean_is_car = CarDamageEdited.is_car(view)
      if boolean_is_car:        
        boolean_is_left = CarDamageEdited.is_side_left()
        if boolean_is_left:
          boolean_window_left = CarDamageEdited.is_window_left()
          boolean_door_left = CarDamageEdited.is_door_left()
          l_result.append(dict(is_window=boolean_window_left, is_door=boolean_door_left))
        left_result.append(dict(damaged=boolean_is_left, types=l_result))
      result.append(dict(image=filename, is_car=boolean_is_car, is_left=left_result))
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
      
      boolean_is_car = CarDamageEdited.is_car(view)
      if boolean_is_car:        
        boolean_is_right = CarDamageEdited.is_side_right()
        if boolean_is_right:
          boolean_window_right = CarDamageEdited.is_window_right()
          boolean_door_right = CarDamageEdited.is_door_right()
          ri_result.append(dict(is_window=boolean_window_right, is_door=boolean_door_right))
        right_result.append(dict(damaged=boolean_is_right, types=ri_result))
      result.append(dict(image=filename, is_car=boolean_is_car, is_right=right_result))
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


      
