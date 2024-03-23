# Bookstore Web-App

## Introduction

Bookstore Web-App is a group project worked on by students as part of a Software
Engineering Course.

This is a Django-based web application for a bookstore, designed and developed
for a Software Engineering course. It functions as a complete "full-stack"
application, utilizing:

- Django: A high-level Python web framework that handles the back-end logic, URL
  routing, and templating for the application.
- PostgreSQL: A powerful object-relational database management system (ORDBMS)
  that stores and manages data for the bookstore, including book information,
  customers, and orders.

This project serves as a platform to:

- Explore Django functionalities: Gain hands-on experience with Django's
  features like models, views, templates, and URL configurations.
- Practice application-database interactions: Utilize Django's Object-Relational
  Mapper (ORM) to interact with the PostgreSQL database, allowing for CRUD
  (Create, Read, Update, Delete) operations on bookstore data.
- Develop a user interface: Design a user-friendly web interface using Django's
  templating system to manage book inventory, customer accounts, and the
  ordering process.

## Getting Started

### Set up local repository

<details><summary> Linux </summary>

**Requires** `curl`

If you're using fish, switch to bash first (by running `bash`).

```sh
sh -c "$(curl -sS https://raw.githubusercontent.com/cdf144/bookstore-web-app/main/scripts/install.sh)"
```

</details>

<details><summary> MacOS </summary>

Download
[install.sh](https://raw.githubusercontent.com/cdf144/bookstore-web-app/main/scripts/install.sh),
then run it

```sh
./install.sh
```

</details>

<details><summary> Windows </summary>

Download
[install.ps1](https://raw.githubusercontent.com/cdf144/bookstore-web-app/main/scripts/install.ps1),
then run it.

```sh
./install.ps1
```

> **Note**
> 
> If you get an error that says something along the lines of "the script cannot
> be loaded because the execution of scripts...", your Execution Policy is not
> setup properly. To resolve this, run Windows PowerShell **as Administrator**,
> then run this command:
>
> ```
> set-executionpolicy Unrestricted
> ```
>
> Note that after running this command, there is a risk of malicious scripts
> being run on your machine. If you want a "safer" Execution Policy, set it to
> `RemoteSigned` instead. More information
> [here](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.4).

</details>

### Run the app

Make sure you are in the project's root folder and venv is activated.

```sh
python manage.py runserver
```
