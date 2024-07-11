from groq import Groq
import yaml
import os
import json

def llama_call(data, jd, verbose=False):
    experience_details = {}
    ct=0
    yaml_data = yaml.safe_load(data)
    try:
        if 'experience' in yaml_data:
            for entry in yaml_data["experience"]:
                experience_details[entry["company"]] = entry["details"]

        if 'leadership' in yaml_data:
            for entry in yaml_data['leadership']:
                experience_details[entry["organization"]] = entry["details"]
                
        client = Groq(api_key=os.getenv('GROQ_API_KEY')) 
        jd_string = "Job Description:\n" + jd
        resume_details = json.dumps(experience_details, indent=2)
        prompt_message = f'''Objective: Generate resume content tailored for job description.
Input Specifications:
- Job Description: Detailed description including required skills and responsibilities.
- Candidate's Basic Experience: Provided as JSON-formatted resume details.

Output Specifications:
- Resume Details: Generate 3-4 tailored bullet points per past role, emphasizing responsibilities and achievements relevant to the job description.
- Skills Section: Identify and list critical technical and soft skills from the job description that align with the candidate's capabilities.

Instructions:
Match Experiences : Align bullet points with the job's required skills and responsibilities, using action verbs and quantitative achievements where possible.
Prioritize Relevant Skills: Extract essential skills from the job description, ensuring they are directly applicable to the position.
Output Format : Ensure JSON output is structured, with clear sections for resume details and skills, categorized under Technical and Soft. 
Keys should be "ResumeDetails", "Skills" accordingly. Do not use any other names.'''

        messages = [
            {"role": "system", "content": prompt_message},
            {"role": "user", "content": f"Job Description:\n{jd}\n\nCandidate's Basic Experience:\n{resume_details}"}
        ]
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages= messages,
            temperature=0.85,
            max_tokens=1830,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
            stop=None,
        )
        gen_text = completion.choices[0].message
        json_content = json.loads(gen_text.content)  # Assuming that the output is in JSON string format
        if verbose:
            print('groq response: ', json_content)
        if "experience" in yaml_data:
            for section in yaml_data["experience"]:
                company = section['company']
                
                if company in json_content["ResumeDetails"]:
                    details = json_content["ResumeDetails"]  # Corrected key access
                    if company in details:  # Check if company exists before accessing details
                        
                        section["details"]=details[company]

			
        if "leadership" in yaml_data:
            for section in yaml_data["leadership"]:
                    org = section['organization']
                    if org in json_content["ResumeDetails"]:
                            detail = json_content['ResumeDetails'][org]
                            if detail and len(detail)>0:
                                section["details"] = detail
                                
                                
			
        if "skills" in yaml_data:
          if isinstance(yaml_data, dict):
            yaml_data["skills"] = json_content["Skills"].copy()  # Replace skills with a copy
            ct=1
          else:
            print("Error: resume_details is not a dictionary. Cannot assign skills.")
        else:
              yaml_data["skills"] = json_content["Skills"].copy()
              
              
   
    except Exception as e:
        print("An error occurred: ", e)

    return yaml_data, ct