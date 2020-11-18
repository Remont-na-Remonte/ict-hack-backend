# ICT Hackathon Project

## Running locally

Initially, install **pipenv** via _brew_ or _pip_.

Then, set up the Postgres database with the data provided in _.env.example_.

Next, enter the pipenv shell and install the reqired dependencies
```
$ pipenv shell
(ict-hack-backend) $ pipenv install
```

When the above-written instructions are done, you can configure and run the server itself
```
(ict-hack-backend) $ python manage.py migrate
(ict-hack-backend) $ python manage.py createsuperuser
(ict-hack-backend) $ python manage.py runserver
```

Now you can access the server at _localhost:8000_ by default

## Populating the DB

To populate the DB with the initial objects run the following command:
```
(ict-hack-backend) $ python manage.py populate_objects
```

## Running the telegram bot

To run the bot execute the following command:
```
(ict-hack-backend) $ python manage.py runbot
```
