# FROM alpine:3.19

# WORKDIR /usr/src/app

# COPY requirements.txt ./

# RUN apk add --update python3 py3-pip
# RUN python3 -m venv /path/to/venv

# # Activate the virtual environment
# RUN . /path/to/venv/bin/activate

# # RUN pip install -r requirements.txt
# RUN pip install pytube

# EXPOSE 5000

# CMD ["python", "skachalka4_0.py"]
# FROM python:3.11

# WORKDIR /usr/src/app

# COPY requirements.txt ./
# # RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install -r requirements.txt

# COPY . .

# CMD [ "python", "./skachalka4_0.py" ]

FROM python:3.10-slim

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install git -y
RUN pip3 install -r requirements.txt
RUN apt-get install -y ffmpeg
RUN pip3 install "git+https://github.com/openai/whisper.git" 


COPY . .

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0" ]
