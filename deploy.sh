#!/bin/bash
set -exu
flake8 src/

aws sso login

sam build
sam local invoke --event local/json/local-event.json

read -p "Continue Script? [N]" -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

sam deploy --guided