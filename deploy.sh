#!/bin/bash
set -exu

#Install Venv and make sure linting is clean
pipenv install --dev
pipenv run flake8 src/

# Get SSO token before running AWS Commands
aws sso login

sam build
sam local invoke --event local/json/local-event.json

## Inspect local invoke and make sure the lambda passed.
echo
read -p "Continue Script? [N]" -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

# Deploy if y/Y is entered
sam deploy --guided