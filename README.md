40-Points
=========

40 Points Card Game

## Development Environment

Powered by:

1. [Python](http://www.python.org/)
2. [MySQL](http://www.mysql.com/)

Recommended tools:

1. [virtualenv](https://python-guide.readthedocs.org/en/latest/dev/virtualenvs/#virtualenv)

### Local Setup

The following assumes you have all of the recommended tools listed above installed.

#### 1. Clone the project:

    $ git clone https://github.com/melvindu/40-Points.git fortypoints
    $ cd fortypoints

#### 2. Create and initialize virtualenv for the project:

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

#### 3. Start the server:
    
    $ python run.py

### Generating the sphinx docs

    $ sphinx-apidoc -o docs <module> -f
    $ cd docs
    $ make html
