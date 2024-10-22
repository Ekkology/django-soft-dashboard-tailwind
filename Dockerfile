FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY . .

# running migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# collect static files
# RUN python manage.py collectstatic --noinput

#EXPOSE 8000

# gunicorn
#CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
