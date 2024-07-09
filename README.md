# RobTheJob

## What the heck is it?

Builds a CV using Llama 3 70B LLM, generates a `yaml` file for CV details, combines the details with the JD a produces a tailored CV with the LaTeX template and exports it into a PDF which is 99% parseable.

## Ok, but how do I run it myself?

- Clone this repo.
- Create a python virtual environment, and install dependencies in `requirements.txt`.

```bash
pip install -r requirements.txt
```

- Make a file called `.env` in the root dir and add in required API keys and secret keys. Follow the JSON structure given in `.env.example`. (psst, you will get the API keys from [groq](https://groq.com/)!)
<!-- - Run database migrations and create a superuser.

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
``` -->

- Now run the server

```bash
python manage.py runserver
```

Your server should be running on port 8000. Visit [localhost:8000](http://localhost:8000/) on your system to see it in its glory.

## I like this, can I make contributions?

Sure mate, go ahead. Fork this repo and create a PR with your changes!