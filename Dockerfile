#FROM nvidia/cuda:12.1.0-devel-ubuntu22.04
#
#
#RUN apt update --assume-yes \
#    && apt install --assume-yes software-properties-common \
#    && apt list | grep python3.10 \
#    && add-apt-repository ppa:deadsnakes/ppa \
#    && apt install --assume-yes python3.10 \
#    && apt-get install -y python3-pip \
#    && rm /usr/bin/python3 && ln -s /usr/bin/python3.10 /usr/bin/python3
#
#
#
#RUN python3.10 -m pip install --upgrade pip
#CMD python3.10 --version
#
#WORKDIR /usr/src/app
#
#RUN pip3 install --no-cache-dir poetry
#
#COPY ./pyproject.toml ./poetry.lock* ./
#
#RUN poetry config virtualenvs.create false \
#    && poetry lock --no-update  \
#    && poetry install --no-dev --no-interaction --no-ansi
#
#COPY ./app ./app
#CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

FROM ubuntu:22.04


WORKDIR /usr/src/app

RUN apt update --assume-yes \
    && apt install --assume-yes software-properties-common \
    && apt list | grep python3.10 \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt install --assume-yes python3.10 \
    && apt-get install -y python3-pip \
    && rm /usr/bin/python3 && ln -s /usr/bin/python3.10 /usr/bin/python3

RUN python3.10 -m pip install --upgrade pip
CMD python3.10 --version

RUN pip3 install --no-cache-dir poetry

COPY ./pyproject.toml ./poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry lock --no-update  \
    && poetry install --no-dev --no-interaction --no-ansi

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY ./app ./app

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
