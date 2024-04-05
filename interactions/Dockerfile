# docker build -t ixro .
# docker run -it ixro /bin/bash
FROM python:3.11-slim

RUN mkdir /data /code
COPY data/interactions_globi_vitis_vinifera.csv /data
COPY ixro /code/ixro
COPY pyproject.toml /code
RUN cd /code && python -m pip install .

# Required environment variables
ENV GBIF_EMAIL=
ENV GBIF_USER=
ENV GBIF_PWD=

CMD ["python", "/code/ixro/__init__.py"]
