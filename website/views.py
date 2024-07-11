from django.shortcuts import render, redirect, render
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseNotFound
import yaml
from groq import Groq
import json
import re

from llm.utils.resume import generate_resume
from llm.utils.llama import llama_call

# Create your views here.

def home_page(request):
    if request.method == 'POST':
        yaml_data = request.POST.get('yaml_data')
        # Instead of storing in session, pass directly to process_data
        return redirect('process_data', yaml_data=yaml_data)

    return render(request, 'website/index.html', {})

def download_yaml(request):
    yaml_data = request.form['yaml_data']
    response = HttpResponse(yaml_data, mimetype='text/yaml')
    response.headers['Content-Disposition'] = 'attachment; filename="submitted_data.yaml"'
    return response

def process_data(request):
    if request.method == 'POST':
        jd = request.form['jd']
        yaml_data = request.form['yaml_data']
        # Pass JD and YAML data to final_page via URL parameters or by posting directly to the endpoint handling final_page
        return redirect('final_page', jd=jd, yaml_data=yaml_data)

    # Check if YAML data exists in request arguments and display form for entering JD
    yaml_data = request.args.get('yaml_data', '')
    if yaml_data == '':
        # If no YAML data is available, redirect to start to ensure flow integrity
        return redirect('index')

    # Render a form that includes the YAML data as a hidden field
    return render(request, 'website/process_data.html', dict(yaml_data))

def final_page(request):
    # Extract data from query parameters instead of the session
    yaml_data = request.args.get('yaml_data', '')
    jd = request.args.get('jd', '')

    # Simulate a function call that processes this data
    response, ct = llama_call(data=yaml_data, jd=jd)

    request.session["LLM"]=response

    context = {'yaml_data': yaml_data, 'jd':jd,'ct':ct}

    return render(request, 'website/final_page.html', context)

def download_resume(request):
    resume_data = request.session.get("LLM")  # Example session data, replace with actual data
    if not resume_data:
        return HttpResponseNotFound("No resume data found!")
    pdf_path = generate_resume(resume_data)
    filename = (pdf_path.split("/")[-1]).split(".")[0]
    response = HttpResponse(open(f"output/{filename}.pdf"), content_type="application/json")
    response['Content-Disposition'] = 'attachment; filename="downloaded_file.json"'
    return response