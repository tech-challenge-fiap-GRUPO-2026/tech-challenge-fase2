#!/bin/sh

if [ -z "$1" ]; then

    docker compose run --rm llm

    docker compose down

else

    export OPENAI_API_KEY="$1"

    docker compose run --rm llm python -m src.llm --mode vrp --output report --deliveries-file data/brazil_capitals_sample.csv --generations "80" --population-size "80" --provider openai

    docker compose down

fi

