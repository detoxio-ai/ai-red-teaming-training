# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11.11-bookworm

# create a user called sia
RUN useradd -m dtx

# set work directory
WORKDIR /home/dtx/app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1


# install dependencies
RUN apt-get update && apt-get install -y curl

# switch to user dtx
USER dtx

RUN curl -sSL https://install.python-poetry.org | python3 -

# add poetry to PATH
ENV PATH="/home/dtx/.local/bin:$PATH"

# copy the poetry lock file and pyproject.toml
COPY --chown=dtx:dtx pyproject.toml poetry.lock README.md  ./

# # install project dependencies
RUN poetry install --no-root

# # copy project
COPY --chown=dtx:dtx . .

# # expose the application port
EXPOSE 8001

# # define the command to run the application
CMD ["poetry", "run", "python", "main.py"]


