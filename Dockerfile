FROM 441581275790.dkr.ecr.ap-southeast-2.amazonaws.com/np-python-development-container:latest
WORKDIR /dependencies
COPY poetry.lock pyproject.toml /dependencies/
COPY np_exploration_python/ /dependencies/np_exploration_python/
RUN bash -c "source ~/.bashrc && poetry install --no-interaction --no-ansi"

ENTRYPOINT ["/bin/bash", "-cl"]