# Service Log API

## Introduction
To record a ticket from customer service.

### Workflow
1. Open ticket by create a new ticket by enter customer information, machine/device/equipment information, issue topic and detail.
2. Record service/work process detail from the created ticket.
3. Close ticket after everything is done.


## Tech stack
- Python
- Sqlite3
- Database first: SqlAlchemy https://www.sqlalchemy.org
- FastAPI
- Uvicon - web server for python

## Setup project
### Generate requirements.txt
- bash: `pip3 install pipreqs`
- Run in current directory
  - bash: `python3 -m  pipreqs.pipreqs .`
### Setup database
- Create database. 
  - bash: `python3 -m database.db`
- Seed default data.
  - bash: `python3 -m database.seed_default_data`

## Run API
- bash: `uvicorn main:app --reload`
- Access API Docs: url: `http://127.0.0.1:8000/docs`