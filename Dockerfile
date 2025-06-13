FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && apt-get install -y \
    build-essential libgl1-mesa-glx libgl1 libglib2.0-0 ffmpeg pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR app/
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --without dev
RUN poetry run pip uninstall ffmpeg ffmpeg-python -y
RUN poetry run pip install ffmpeg-python

CMD ["poetry", "run", "python", "dvr/app.py"]
