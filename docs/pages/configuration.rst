Configuration
=============

Copy the file ``conf/compose.ini.tpl`` to ``conf/compose.ini`` and set
the right Configuration parameters. The config validation is defined in configspec.ini

Main configuration parameters should be defined in the ``[main]`` section.
Another section (``[network-block]``) has been created to define TCP ports to block for outgoing
requests.


.. WARNING::
   Don't use double quotes to protect your values.

   Use ``#`` to comment your lines and not ``;``


Network and changes in general
------------------------------------
You can define your own network in compose.ini by setting a ``subnet``.
It's optional, and it's probably better to let it like that.

.. WARNING::
   If you change that, run ``docker-clean`` which
   removes orphans images, stopped container, etc ...

   As we use ``traefik`` as a reverse proxy, no need to expose any ports
   or to access containers directly via their IP.

   Also, if you change any parameter such as an environment variable
   run a ``stakkr restart --recreate`` to make sure that you start from
   a clean environment.


Services
-----------------
You can define a list of services you want to have. Each service
consists of a yml file in the ``services/`` directory of the
source code. Each container ("Service") will have a hostname
which is the ... service name. To reach, for example,
the elasticsearch server from a web application use ``elasticsearch``.
To connect to mysql it's ``mysql``.

.. code:: cfg

    services=apache,php,mysql

A service can launch a post-start script that has the same name with an
``.sh`` extension (example: ``services/mysql.sh``).

To have a complete list of services, launch :

.. code:: shell

    $ stakkr services


Special case of Elasticsearch
------------------------------
ElasticSearch needs a few manual commands to start from the version 5.x. Before starting stakkr, do the following :

.. code:: shell

    $ mkdir data/elasticsearch
    $ sudo chown -R 1000:1000 data/elasticsearch
    $ sudo sysctl -w vm.max_map_count=262144


Special case of xhgui service
----------------------------------
To be able to profile your script, add the service xhgui and read the
`documentation`_


Other useful parameters
--------------------------

Project name (will be used as container's prefix). It should be
different for each project.

.. code:: ini

    # Change Machines names only if you need it
    project_name=stakkr

PHP Version :

.. code:: ini

    # Set your PHP version from 5.3 to 7.0 (5.6 by default)
    php.version=7.0

MySQL Password if mysql is defined in the services list:

.. code:: ini

    # Password set on first start. Once the data exist won't be changed
    mysql.root_password=changeme

Memory assigned to the VMS:

.. code:: ini

    apache.ram=512M
    elasticsearch.ram=512M
    mysql.ram=512M
    php.ram=512M

.. _documentation: https://github.com/edyan/docker-xhgui


Port Blocking: by default, we can block ports only for the PHP container (as iptables is installed).
Define in a list what port you want to **block for OUTPUT TCP requests**. That has been done to
avoid mistakes such as using a production database and send a lot of emails ...

.. code:: ini

    [network-block]
    php=25,465,587


Files location
------------------

Public Files
~~~~~~~~~~~~~~
-  All files served by the web server are located into ``www/``


Services Data
~~~~~~~~~~~~~~~~~
-  MySQL data is into ``data/mysql``
-  Mongo data is into ``data/mongo``
-  ElasticSearch data is into ``data/elasticsearch``
-  Redis data is into ``data/redis``
- ...

Logs
~~~~~~
-  Logs for Apache and PHP are located into ``logs/``
-  Logs for MySQL are located into ``data/mysql/`` (slow and error).

Configuration
~~~~~~~~~~~~~~~
-  If you need to override the PHP configuration you can put a file in
   ``conf/php-fpm-override`` with a ``.conf`` extension. The format is
   the fpm configuration files one. Example:
   ``php_value[memory_limit] = 127M``.
-  If you need to override the mysql configuration you can put a file in ``conf/mysql-override``
   with a ``.cnf`` extension.


Add binaries
------------
You can add binaries (such as phpunit) that will automatically be
available from the PATH by putting it to ``home/www-data/bin/``


.. IMPORTANT::
   You can use ``home/www-data`` to put everyhting you need to keep:
   your shell parameters in `.bashrc`, your ssh keys/config into `.ssh`, etc.
