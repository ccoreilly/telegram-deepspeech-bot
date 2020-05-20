FROM python:3.7.6 as base

WORKDIR /app

RUN apt-get update -qq && apt-get -y install ffmpeg libavcodec-extra

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY deepspeech-bot.py .

ENV MODEL_PATH /app/model/model.pbmm
ENV SCORER_PATH /app/model/kenlm.scorer

RUN mkdir -p tmp

CMD ["python", "deepspeech-bot.py"]