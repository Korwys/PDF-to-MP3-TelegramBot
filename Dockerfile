FROM python:3.10.2-slim

# set work directory
WORKDIR /home

# copy project
COPY . /home
COPY pyproject.toml /home/

# env
ENV TOKEN="API_TOKEN_BOT"

# install and config poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# install dependencies
RUN poetry install

# run app
CMD ["python","main.py"]
