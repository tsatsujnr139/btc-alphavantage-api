# BTC API

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Pre-requisites

1. Docker - (Instructions on how to install can be found [here](https://docs.docker.com/install/) 
2. Docker-Compose (Instructions on how to install can be found [here](https://docs.docker.com/compose/install/)


### Get Up and running

Once the prerequisites are met, The following steps can be used to get the application up and running. All commands are run from the root directory of the project

1. Build the docker image using

```
docker-compose build
```

2. Run the application using (This step also all run all upgrade operations on the database using the most recent migration file)

```
docker-compose up
```

3. Run the tests

```
docker-compose run web sh -c "python manage.py test"
```

4. View available API's. The API's that require authentication require the header Authorization: Token "tokenfromcreatetokenapi"

```
docker-compose run web sh -c "python manage.py show_urls". 
```

5. You can access the available api's after starting up the application using the base URL
```
http://localhost:8000/
```

## Authors

- **Tsatsu Adogla-Bessa Jnr**

