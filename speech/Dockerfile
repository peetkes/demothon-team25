FROM python:3.13.3
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libasound2 \
    pulseaudio \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/* \

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "speech.py"]