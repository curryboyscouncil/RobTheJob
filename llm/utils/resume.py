from jinja2 import Environment, FileSystemLoader
import os
import subprocess
import json
from website.models import Resume
from server import settings

def generate_resume(resume_id):

    resume_obj = Resume.objects.get(pk=resume_id)

    env = Environment(
        block_start_string='~<',
        block_end_string='>~',
        variable_start_string='<<',
        variable_end_string='>>',
        comment_start_string='<#',
        comment_end_string='#>',
        trim_blocks=True,
        lstrip_blocks=True,
        loader=FileSystemLoader(searchpath="./"),
    )

    resume = json.loads(resume_obj.resume_text)

    template = env.get_template("resume_template.latex")
    rendered_resume = template.render(resume)
    rendered_resume = rendered_resume.replace("%", "\%")
    filen = resume['name']
    
    output_folder = "media"
    output_filename = f"{filen}_resume.tex"
    directory = os.path.join(settings.BASE_DIR, output_folder)

    if not os.path.exists():
        os.makedirs(directory)

    output_path = os.path.join(directory, output_filename)
    with open(output_path, "w+") as fout:
        fout.write(rendered_resume)
    
    try:
        subprocess.run(["pdflatex", f"{filen}_resume.tex"],cwd="./media")
        return output_path.replace(".tex", ".pdf")
    except Exception as e:
        print(e)
        return output_path