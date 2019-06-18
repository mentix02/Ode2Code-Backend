# Ode2Code Documentation

## Development

The first step to get the code for Ode2Code is to clone the git repo on your machine - preferably a Linux one. Specifically [Ubuntu 18.04 LTS](https://ubuntu.com/download/desktop).

```bash
$ mkdir ode2code
$ cd ode2code/
$ git clone https://github.com/mentix02/Ode2Code-Backend backend
$ cd backend/
```

To setup your local development server on your machine, all you need to do is install [MySQL](https://www.mysql.com/) for the database and a [Python 3.6](https://python.org/downloads/) (or above) interpreter. 

```bash
$ sudo apt update
$ sudo apt install mysql-server mysql-client python3.6
```

The next recommended step would be to create and activate a virtual environment for your Python interpreter. Installing virtualenv using `pip` is the way to go (make sure you're in the backend directory) - 

```bash
$ pip install --upgrade pip virtualenv
$ virtualenv venv
$ source venv/bin/activate
```

Then just run `make` to run the `bin/install.sh` script (make sure the virtualenv is activated).

Then enter the fields that are prompted. All inputs, by the way, remain stored only on your disk. Nowhere else.
