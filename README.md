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

You might encounter a `Permission denied` error launching this application. In such a case, launch it with the following command instead:

```bash
sudo venv/bin/python3 main.py
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

Here, you'll find all stylesheets and javascript files used by the templates.

### `/templates`

This directory contains all templates used in headed requests.

## API

This application uses the `/api` endpoint for headless mode on all of its endpoints.

### `/api/about`

Supported methods: `GET`

### `/api/projects` and `/api/projects/<int:project_ID>`

Supported methods: `GET`, `POST`, `PUT`, `DELETE`

#### `POST`:

to `POST` a new resource, no ID is required. Your request needs to include a valid JSON:

##### structure:

```json
{
    ProjectName: "Rice Cooker",
    ProjectDescription: "In collaboration with Bosch, I designed and built a consumer-grade kitchen appliance."
}
```

#### `PUT`

to `PUT`, a valid `project_ID` must be supplied in the URL, e.g. `/api/projects/1`.

##### Structure:

```json
{
    ProjectName: "Rice Cooker",
    ProjectDescription: "In collaboration with Bosch, I designed and built a consumer-grade kitchen appliance."
}
```

#### `DELETE`

To `DELETE` a resource, no JSON is required. Simply send a `DELETE` request to `/api/projects/<int:project_ID>`, e.g. `/api/projects/1`.



### `/api/feedback`

Supported methods: `GET`, `POST`

#### `POST`

to `POST` a new feedback resource, send a `POST` request to `/api/feedback`. Your request must contain a valid JSON:

##### Structure:

```json
{
    Author: "John Smith",
    Feedback: "Great site! Not enough cat pictures though ..."
}
```



#### 
