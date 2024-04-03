# syntax=docker/dockerfile:1

FROM ubuntu:22.04

COPY . /code
CMD /code/script.sh

# When running in the hackathon evaluation script, `ls -d /code/tests/data/*.csv`
# will be used to append all test cubes available in the `tests/data` directory
# so if you have more than one cube there, be sure your workflow can cope with that
