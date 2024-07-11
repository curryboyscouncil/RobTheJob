from jinja2 import Environment, FileSystemLoader
import os
import subprocess

def generate_resume(resume):
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
    template = env.get_template("resume_template.latex")
    rendered_resume = template.render(resume)
    rendered_resume = rendered_resume.replace("%", "\%")
    print("Type of the resume")
    print(type(rendered_resume))
    filen = resume['name']
    
    output_folder = "media"
    output_filename = f"{filen}_resume.tex"
    output_path = os.path.join(output_folder, output_filename)
    with open(output_path, "w") as fout:
        fout.write(rendered_resume)
    # subprocess.run(["pdflatex", f"{filen}_resume.tex"],cwd="./output")
    return output_path