# IOTA-mam
This project is forked from django-sshkm is a Django based ssh-key management tool in order to manage decryption of mam streams on IOTA.

## Requirements
- Linux
- RabbitMQ
- Python >= 2.7
- Django >= 1.8
- Celery >= 4.0.0
- Django compatible database like (SQLite, MySQL/MariaDB, PostgreSQL, ...)

## Used Technologies
- [Linux](https://www.kernel.org)
- [Python](https://www.python.org)
- [Django](https://www.djangoproject.com)
- [RabbitMQ](https://www.rabbitmq.com)
- [Celery](http://www.celeryproject.org)
- [Bootstrap](http://getbootstrap.com)
- [jQuery](https://jquery.com)
- [DataTables](https://datatables.net)

## Setup
- Install a RabbitMQ server.
- Install a Django compatible database.
- Install SSHKM:  
  you will need some development tools and libraries: gcc python python-devel python-pip mariadb-devel postgresql-devel openldap-devel httpd-devel  
```bash
pip install django-sshkm
```
- Configure /etc/sshkm/sshkm.conf (create it if it does not exist)  
  You can find an example in your install directory (example: /usr/lib/python2.7/site-packages/sshkm/sshkm.conf).  
  If you use sqlite make sure that the user running celery (see next step) has read and write permissions to the db-file.
- Install a webserver which runs wsgi  
  Example Apache httpd:  
```
Alias /static/ /usr/lib/python2.7/site-packages/sshkm/static/

<Directory /usr/lib/python2.7/site-packages/sshkm/static/>
  Require all granted
</Directory>

WSGIScriptAlias /sshkm /usr/lib/python2.7/site-packages/sshkm/wsgi.py/
WSGIDaemonProcess sshkm user=apache group=apache
WSGIProcessGroup sshkm

<Directory /usr/lib/python2.7/site-packages>
  <Files wsgi.py>
    Require all granted
  </Files>
</Directory>
```
- Run celery  
```
cd /usr/lib/python2.7/site-packages
celery worker -A sshkm -l info
```

## Firewall & SELinux
Be aware of firewall and SELinux issues  
  
You can find more informations in the wiki: https://github.com/sshkm/django-sshkm/wiki
