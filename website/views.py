from django.shortcuts import render, redirect, render
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseNotFound
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
import yaml
from groq import Groq
import json
import re
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django_ratelimit.decorators import ratelimit

from llm.utils.resume import generate_resume
from llm.utils.llama import llama_call
from .serializers import ResumeSerializer
from .DTOs import ResumeDTO

# Create your views here.

cache_timeout = 60 * 60 * 15

@api_view(['GET'])
@ratelimit(key='ip', rate='100/h')
@cache_page(cache_timeout)
def api_overview(request: Request):
    api_urls = {
        'API documentation': 'GET /swagger',
    }

    return Response(api_urls)

@api_view(['POST'])
# @ratelimit(key='ip', rate='5/h')
def send_profile(request: Request):
    cv = request.data['cv_yaml']
    jd = request.data['jd']

    response, ct = llama_call(data=cv, jd=jd)

    res = {'cv': cv, 'jd': jd, 'resume_text': json.dumps(response)}
    # print(res)
    resume_serializer = ResumeSerializer(data=res)

    if resume_serializer.is_valid():
        r = resume_serializer.save()
    else:
        print(resume_serializer.errors)
        return Response("Error in saving the resume", status=status.HTTP_503_SERVICE_UNAVAILABLE)

    res['resume_text'] = response
    res['ct'] = ct,
    res['r_id'] = r.id

    return Response(res)

@api_view(['GET'])
@ratelimit(key='get:r_id', rate='50/h')
@cache_page(cache_timeout)
def download_resume(request: Request):
    resume_id = request.query_params.get("r_id")  # Example session data, replace with actual data

    if not resume_id:
        return Response("No resume data found!", status=status.HTTP_204_NO_CONTENT)
    pdf_path = generate_resume(resume_id)
    filename = (pdf_path.split("/")[-1]).split(".")[0]
    return Response({'path': f"/media/{filename}.tex"})