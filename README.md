# demo backend

## Setup env (windoes)
- virtualenv venv -p python.exe
- .\venv\Scripts\activate
- pip install -r requirements.txt

## Initialize DB from scratch
    - remove local db fro  app/main/db
    - run `yarn db_init` to initialize db with migrations
    - run `yarn db_migrate -- -m "initial migration"` to create migration with db scheme
    - run `yarn db_upgrade` to apply changes from migration to db

## make new migration
    - yarn db_migrate -- -m "migration-description"

## style checking

`flake8 app/main --ignore=E501`
`pycodestyle app/main --ignore=E501`
`pylint app/main --disable=R0903,W0703,W0613,R0913,E0401,R0801,R0914,R0915`

## reminders
    - build image localy
    docker build --no-cache --progress=plain -t my-image .

## run
    yarn start

## unit tests
    yarn test