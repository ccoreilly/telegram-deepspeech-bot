#!/usr/bin/env python

import os, sys, logging

import scipy.io.wavfile as wav

from deepspeech import Model
from pydub import AudioSegment
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger("DeepspeechBot")

TOKEN = os.environ.get("TELEGRAM_TOKEN")
BASE_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
AUDIO_FILE_PATH = BASE_PATH + "/tmp/{}_{}.{}"
MODEL_PATH = os.environ.get("MODEL_PATH", BASE_PATH + "/model/model.pbmm")
SCORER_PATH = os.environ.get("SCORER_PATH", BASE_PATH + "/model/kenlm.scorer")

ds = Model(MODEL_PATH)
ds.enableExternalScorer(SCORER_PATH)


def start(update, context):
    update.message.reply_text(
        "Hola\! Sóc un bot creat per a provar les capacitats de reconeixement automàtic de la parla "
        "del motor DeepSpeech de Mozilla amb les dades de CommonVoice\. Envia'm un missatge de veu i "
        "el transcriuré\. Pots trobar més informació sobre el model català [aquí](https://github.com/ccoreilly/deepspeech-catala)\.",
        parse_mode="MarkdownV2",
    )


def info(update, context):
    update.message.reply_text("Envia'm un missatge de veu i el transcriuré")


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def voice(update, context):
    message = update.message

    if message.voice.duration > 10:
        update.message.reply_text(
            "Em sap greu però per ara els missatges vocals estan limitats a deu segons."
        )
        return

    ogg_file_path = AUDIO_FILE_PATH.format(message.chat_id, message.message_id, "ogg")
    new_file = message.voice.bot.get_file(message.voice.file_id)
    new_file.download(ogg_file_path)

    wav_file_path = AUDIO_FILE_PATH.format(message.chat_id, message.message_id, "wav")
    AudioSegment.from_ogg(ogg_file_path).export(
        wav_file_path, format="wav", parameters=["-ar", "16000", "-ac", "1"]
    )

    fs, audio = wav.read(wav_file_path)
    text = ds.stt(audio)

    update.message.reply_text(text)

    os.remove(ogg_file_path)
    os.remove(wav_file_path)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, info))
    dp.add_handler(MessageHandler(Filters.voice, voice))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
