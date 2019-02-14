simple_shop
===========

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


:License: MIT


About project
--------
It's simple shop app build with django-cookiecutter. Main features:
-development environment based on docker images
-session based shopping cart
-used django-formtools (FormWizard, FormPreview)
-manage app with permission for staff only
-allauth authentication
-css styling with Sass  

Run project with Docker
^^^^^^
First install docker and docker-compose

Build the stack:
::

  $ docker-compose -f local.yml build

Run the stack:
::

  $ docker-compose -f local.yml up
