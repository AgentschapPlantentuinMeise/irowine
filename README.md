

## References

- https://github.com/AgentschapPlantentuinMeise/intercubos
- https://github.com/AgentschapPlantentuinMeise/intercubos/blob/main/intercubos/occurrences.py

## Building the interaction cubes for Vitis vinifera

    cd interactions
    docker build -t ixro .
    docker run -v $RESULTS_FOLDER_PATH:/results \
      -e GBIF_USER=$GBIF_USER -e GBIF_PWD=$GBIF_PWD ixro
