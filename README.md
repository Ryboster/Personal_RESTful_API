# Developer Profile API

## Purpose

The purpose of this website is to showcase my abilities as a software developer, and constitute a place of self advertisement and promotion.

## Setup

To use this app you're going to need to install required packages. Open a terminal window and type in the following commands:

```bash
$ python3 -m venv venv # Create a new virtual environment
$ source venv/bin/activate # Activate (or enter) the virtual environment
$ pip install -r requirements.txt # Download required packages from a file
```

This application takes two optional positional arguments; **PORT** and **HOST**. If not provided, it will default to hosting the server on `0.0.0.0:443`.

To launch the application, enter the following command:

```bash
$ python3 main.py 8000 "1.1.1.1" # Launch the application
```

or

```bash
$ python3 main.py
```



## Hosting

The site is currently hosted at https://blazejowski.co.uk

The repository is public and can be found [here](https://github.com/Ryboster/Personal_RESTful_API), although without the database files - those are private.

## Directory Structure

### `/` (root)

Here you'll find files needed to set up and run the website.

### `/lib`

This directory stores all classes and functional scripts used by the server, most notably the `Router` class, which is responsible for answering to user requests with templates.

### `/lib/databases`

This directory contains all databases, and queries used in creating databases.

### `/media`

This directory stores all visual files used by and uploaded to the server.

### `/static`

Here, you'll find all stylesheets and javascript files used by the templates

### `/templates`

hmmmmmmm...
