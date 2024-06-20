# E-commerce

An implementation of small set of APIs for an e-commerce.


## ✋ Before you start

This project uses the following tools:

- [python](https://www.python.org/) as runtime
- [virtualenv](https://docs.python.org/3/library/venv.html) way to run your python environment
- [django](https://www.djangoproject.com) as web framework
- [postgres] (https://www.postgresql.org) as database for the application
- [psycopg2](https://pypi.org/project/psycopg2/) as library to communicate to Postgres
- [rest_framework](https://pypi.org/project/djangorestframework/) as framework to build API on top of Django

## 📑 Getting started

The project has been tested on Mac only.

1. ensure you have `python` [installed](https://www.python.org/downloads/) on your computer.

2. clone this repository and `cd` into it.

3. run `pip install -r requirements.txt` to install the correct dependencies.

4. add your postgres env vars in `settings.py`.

5. run `python manage.py migrate` to run migrations on database.

6. run `python manage.py createsuperuser` to create a valid user.

7. run `python manage.py runserver` to start the development server.

8. send a POST request to ` http://127.0.0.1:8000/auth/` with the valid user credentials as body, to get a valid token.
```
{
	"username": "michelecapra",
	"password": "password"
}
```

8. start navigating API adding `Authorization` header with value `Token your-token`.

9. if you want you can create some data through [admin](http://127.0.0.1:8000/admin).

## 🏗️ Project Structure

The project is organized into two main apps:

1. `ecommerce`: the core application that contains models, test and settings for the django app.
2. `ecommerce_api`: the set of apis and serializers, built using Django REST framework .

## 🚢 Deployment

For this application and especially if you are a small team, I suggest to deploy this application on a Paas. This way you'll maximize on your dev team to focus on product development and leave most for the infra work to the Pass service. 

We could use Heorku for this work. In that case, we should:
* create a new application in heroku.
* create a Procfile to tell Heroku how to start our django application and push it to our repo.
* link the application to our public repo in git and force a deploy.
* enable Automated Certification Management to force https for all connections.
* then we would be able to reach it at a specific address that you can get from the settings tab.

Alternatively we could use AWS to retain more control (and more work) over our infra. Still in that case, I would suggest to add a Dockerfile to containerize the application. Then we should use ECS on Fargate to deploy our application. I choose again Fargate instead of EC2 to minimize the devops work from the team.

Basically we should:
* push the image to the ECR registry.
* create an ECS application on Fargate that uses our image.
* then I would set the minimum set of instance that you want always active and set also the tracking policy to scale them when you have peak traffic.
* in front of all of this I would put and Elastic Load Balancer to redirect traffic to the different instances.
