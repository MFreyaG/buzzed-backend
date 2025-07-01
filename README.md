### Remember activating the venv
#### Create a new one
`python3 -m venv venv`
#### Activate current one
`source venv/bin/activate`

### 1. Install project dependencies
`pip install -r requirements.txt`

### 2. Create and load Django migrations
`python3 manage.py migrate`

`python3 manage.py makemigrations`

### 4. Create Django superuser
`python3 manage.py createsuperuser`

### 5. Run server
`python3 manage.py runserver`

### 6. Run tests
`python3 manage.py test path.to.test`