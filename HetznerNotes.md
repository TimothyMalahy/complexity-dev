- following - https://community.hetzner.com/tutorials/run-django-app-on-webhosting-or-managed-server
  - pre step 1.1 of that article
    - Created cloud service for 8.99/month
    - sudo add-apt-repository universe
    - sudo apt-get update
    - apt install python3-pip
  - step 1.1
    - installed break system pacakges and virtualenv
    - *mkdir /usr/home
    - *mkdir /usr/home/holu
    - mkdir /usr/home/holu/virtualenvs
    - *python3 -m virtualenv /usr/home/holu/virtualenvs/.venv
    - . /usr/home/holu/virtualenvs/.venv/bin/activate
  - step 1.2
    - normal instructions
  - step 1.3
    - normal instructions
  - step 2.1
    - mkdir /usr/home/holu/djangoprojects
    - *env -C "/usr/home/holu/djangoprojects" django-admin startproject complexityindex
  - step 2.2
    - *vim /usr/home/holu/djangoprojects/complexityindex/complexityindex/settings.py
    - edited allowed hosts to be "complexityindex.com"
  - step 3 (prepare document root of webserver)
    - *mkdir -p /usr/home/holu/public_html/complexityindex
  - step 3 Option 1 - FastCGI
    - *vim /usr/home/holu/public_html/complexityindex/djangoapp.fcgi
    - 