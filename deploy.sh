#!/bin/sh
poetry export -f requirements.txt --output requirements.txt --without-hashes
poetry run chalice deploy --profile $profile
rm requirements.txt
