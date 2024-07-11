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
@ratelimit(key='ip', rate='5/h')
def send_profile(request: Request):
    cv = request.data['cv_yaml']
    jd = request.data['jd']

    response, ct = llama_call(data=cv, jd=jd)

    res = {'cv': cv, 'jd':jd,'ct':ct, 'response': response}

    return Response(res)

@api_view(['GET'])
@ratelimit(key='ip', rate='50/h')
@cache_page(cache_timeout)
def download_resume(request: Request):
    resume_data = request.query_params.get("user")  # Example session data, replace with actual data
    if not resume_data:
        return Response("No resume data found!", status=status.HTTP_204_NO_CONTENT)
    pdf_path = generate_resume(resume_data)
    filename = (pdf_path.split("/")[-1]).split(".")[0]
    return Response({'path': f"/media/{filename}.pdf"})