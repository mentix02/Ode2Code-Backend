# Contributing to Ode2Code

Thank you for deciding to contribute to this open source project.

## Table of Contents

+ [Introduction](#introduction)
    + [Tech Stack](#tech-stack)
       + [Requirements](#requirements)
    + [Frontend Repo](#frontend-repo)
+ [Installing Ode2Code](#installing-ode2code)
+ [Style Guide](#style-guide)
+ [Requests](#requests)
    + [Bug Reports](#bug-reports)
    + [Feature Requests](#feature-requests)

## Introduction

Ode2Code is, at it's core, an API service that's built with Django. It's more or less inspired by Instagram's tech stack - Django on the server side and React for the frontend. For Ode2Code, the backend is just an API that serves JSON content and manages the database. In addition to Django, it relies heavily on [django-rest-framework](https://www.django-rest-framework.org/). In fact, the entire API authentication system is derived from [django-rest-framework's authtoken](https://www.django-rest-framework.org/api-guide/authentication/) module. Refer the [requirements.txt](https://github.com/mentix02/Ode2Code-Backend/blob/master/requirements.txt) file to see a whole list of packages used. 

### Requirements

Ode2Code was built using Python 3.6 on a machine running Ubuntu 18.04 LTS (with a decent internet connection). So make sure you have all of those three things before [running it locally](#installing-ode2code).

### Tech Stack
Ode2Code uses [Gunicorn](https://gunicorn.org/) for its production server. For the frontend, we use the [React.js](https://reactjs.org) JavaScript framework. The frontend can be found [here](https://github.com/mentix02/Ode2Code-Frontend).

### Frontend Repo
As mentioned, the frontend is React project that lives as a seperate project. At the time of writing this, the two projects haven't been merged yet. The current workflow is running the test server on port 8000 and the frontend on the React development server (more on this later). There is little to no documentation save the auto-generated README by create-react-app for the frontend and thus it might be a tad harder to contribute over there. But if you still want to look at the source - [Ode2Code-Frontend](https://github.com/mentix02/Ode2Code-Frontend).

## Installing Ode2Code

Read the guide over at [docs/README.md](docs/README.md).

## Style Guide

I have seen a lot of big open source projects stress over maintaining a consistent code standard and have also seen a ton of debate over formatters and that's why, at least for now, I don't have a particular style guide save the (more of less, *official*) one from Kennith Reitz - [pep8](https://pep8.org/).

If you're writing code using an IDE like PyCharm, don't change the default settings for code formatting and you'll be good to go since it already enforces pep8. Try to document ever new `class` that you define with a docstring like so - 

```python
class ClassName(SuperClassName):
    """
    ClassName is a dummy class meant
    to showcase how one should document
    his / her code when writing them
    for Ode2Code.
    """
    
    def __init__(self, name):
        """
        Take a parameter name of
        type string. If it's not
        string, ValueError is raised.
        """
        if type(name) != str:
            raise ValueError('Please provide a string for the name.')
        self.name = name

    def say_hello(self):
        """
        Also document the methods
        defined inside the class
        """
        print(f'Hello, {self.name}')

    @staticmethod
    def do_nothing():
        """
        If a class method doesn't
        refer "self" explicitly, you
        need to make it a static
        method by adding the '@staticmethod'
        decorator and not having a 'self'
        parameter inside of the parenthesis.
        """
        print('I do nothing!')
```

Now as mentioned in [requirements](#requirements), Ode2Code can only be developed with Python 3.6+ as it uses features such as format strings and type hinting in some areas where data type safety is critical or when functions return complex dictionaries or lists - and thus type hinting just makes managing them a tad easier. Type hinting isn't adopted as much as I'd like and [mypy](http://mypy-lang.org/) won't even succeed on more than a few files when tested with but this is just as a disclaimer - type hinting is NOT discouraged, rather it can be appreciated as long as it's not **overkill**. There's no metric to measure how much checking should be done but that will be covered in testing.

## Requests

There's a reason why I made Ode2Code open source. Well, three reasons actually - 1. because I have been using open source tools for as long as I can remember and until I'm working at a private company and don't have to worry about money, all the software that I'll author will be published on GitHub. 2. I am extremely lazy at coming up with ideas to implement to make software better so I hope to rely on the users of the software that I write for ways to improve. And 3. I don't have money to make private repos even if I wanted to.

### Bug Reports

If you encounter any bugs, please follow the [template format here](docs/bug_report_template.md) and [submit the report here](https://github.com/mentix02/Ode2Code-Backend/issues/new).

### Feature Requests

Follow the same instructions for making a feature request as filing a bug report but start the title with "Feature Request" (without the quotes). No particular template to be followed.
