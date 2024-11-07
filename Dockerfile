FROM python:3.12
EXPOSE 5000
WORKDIR /cogmood_backend
COPY requirements.txt .
RUN pip install -r requirements.txt &&\
    playwright install && \
    playwright install-deps
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "10", "-k", "gevent", "--max-requests", "5000", "app:app"]
