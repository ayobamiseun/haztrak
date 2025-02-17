# Builder
FROM python:3.11.2-alpine3.17 as builder
LABEL maintainer="graham.david@epa.gov"
# Starting environment varibles
ENV APP_DIRECTORY=/app/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR $APP_DIRECTORY
COPY requirements.txt ./
RUN mkdir $APP_DIRECTORY/static
RUN mkdir $APP_DIRECTORY/media
# Setup virtual environment and install dependencies
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir --quiet -r requirements.txt
# Copy app into image working directory
COPY . .
ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# local
FROM builder as dev
EXPOSE 8000
RUN python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    python manage.py loaddata dev_data.yaml
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# Production
FROM builder as production
EXPOSE 8000
CMD  ./run.sh
