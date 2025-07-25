To run:

Create a venv:
`python -m venv .venv`

Activate venv
`source .venv/bin/activate`

Install Dependencies
`pip install -r requirements.txt`

Run Server
`uvicorn main:app --reload`

Now see docs
`http://127.0.0.1:8000/api/v1/docs#/`