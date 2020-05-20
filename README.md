# DeepSpeech inference Telegram bot

A simple telegram bot that will convert a voice note to text using a [DeepSpeech](https://github.com/mozilla/DeepSpeech) model. Created to quickly test my [DeepSpeech Catalan model](https://github.com/ccoreilly/deepspeech-catala).

## Configuration

The following environment variables allow configuring the bot:

| Variable         | Description                      | Default                |
| ---------------- | -------------------------------- | ---------------------- |
| `TELEGRAM_TOKEN` | The unique token of your bot     | None                   |
| `MODEL_PATH`     | The path to the DeepSpeech model | `./model/model.pbmm`   |
| `SCORER_PATH`    | The path to the KenLM scorer     | `./model/kenlm.scorer` |

## Usage

Install the requirements

```
$ pip install -r requirements.txt
```

and start the bot

```
$ python deepspeech-bot.py
```

## Usage with Docker

Build the docker image

```
$ docker build -f Dockerfile -t deepspeech-bot .
```

Run the docker image. You can specify a volume and environment variables (please refer to the docker run [documentation](https://docs.docker.com/engine/reference/commandline/run/)):

```
$ docker run -v /path/to/my/model:/app/model -e TELEGRAM_TOKEN deepspeech-bot
```