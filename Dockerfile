FROM python:3.12
EXPOSE 5000
WORKDIR /cogmood_backend
COPY requirements.txt .
RUN pip install -r requirements.txt &&\
    playwright install && \
    playwright install-deps && \
    apt-get install gcc g++ cmake zlib1g-dev genisoimage && \
    git clone https://github.com/hamstergene/libdmg-hfsplus.git && \
    cd libdmg-hfsplus && \
    cmake . && \
    make 
COPY . .
ENV SCRIPT_NAME="/cogmood"
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "10", "-k", "gevent", "--max-requests", "5000", "app:app"]
