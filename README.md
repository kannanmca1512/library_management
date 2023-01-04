# library_management APIS
Library management application

This is sample project code snippet to implement a library application,
django rest framework where introduced for developing the web APIs.

## Installation
Make sure that you have been installed the virtualenv.
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install virtualenv.

```bash
pip install virtualenv
```
After the installation, create an env and activate it using the following commands

```bash
virtualenv -p python3 env
```

```bash
source env/bin/activate
```
Navigate to the project folder and install the dependencies given in the requirements.txt file

```bash
pip install -r requirements.txt
```
After the successfull installation do the migrations to reflect the database configurations.

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

## Usage

run the code snippet 

```bash
python manage.py runserver
```
You can navigate to ```http://127.0.0.1:8000/``` to start testing the APIs.

## Testing
Create a superuser to access the admin panel.
[create superuser](https://www.geeksforgeeks.org/how-to-create-superuser-in-django/)

## Testing apis
You can test the apis using postman.
Navigate to the project root directory, and execute the APIs given in the 
```API_samples.txt``` to view the results.

