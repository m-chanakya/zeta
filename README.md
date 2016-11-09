# zeta

## How do I get set up? ##

**Install the requirements:**

1. virtualenv --no-site-packages --distribute venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. sudo apt-get install rabbitmq-server

**Entering the virtual environment**

1. source venv/bin/activate

**Create/Sync the database:**

1. ./manage.py makemigrations 
2. ./manage.py migrate

**Starting rabbit-mq server**

1. sudo rabbitmq-server

**Starting celery worker**

1. celery -A zeta worker -B -l info

**Starting the server:**

1. ./manage.py runserver [host:port]

**Exiting the virtual environment**

1. deactivate
