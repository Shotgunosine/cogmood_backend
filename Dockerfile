FROM python:3.12
EXPOSE 5000
WORKDIR /cogmood_backend
COPY requirements.txt .
RUN pip install -r requirements.txt &&\
    playwright install && \
    playwright install-deps
RUN apt-get install -y cmake genisoimage && \
    cd / && \
    git clone https://github.com/planetbeing/libdmg-hfsplus.git && \
    cd libdmg-hfsplus && \
    git fetch && \
    git checkout openssl-1.1 && \
    cmake . && \
    make && \
    mv dmg/dmg /usr/local/bin/ && \
    cd /
RUN curl https://sh.rustup.rs -sSf > install_rust.sh && \
    bash install_rust.sh -y && \
    . "$HOME/.cargo/env" && \
    cargo install --git https://github.com/indygreg/apple-platform-rs --branch main --bin rcodesign apple-codesign && \
    cd ../cogmood_backend

COPY . .
ENV SCRIPT_NAME="/cogmood"
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "10", "-k", "gevent", "--max-requests", "5000", "app:app"]
