FROM python:3.12
EXPOSE 5000
WORKDIR /cogmood_backend
COPY requirements.txt .
RUN pip install -r requirements.txt &&\
    playwright install && \
    playwright install-deps
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]