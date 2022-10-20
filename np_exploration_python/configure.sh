#! /bin/bash

source /root/.cache/pypoetry/virtualenvs/np-exploration-python-PSNYYbGO-py3.9/bin/activate
python np_exploration_python/configure_settings.py
poetry install --only project