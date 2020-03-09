Installation
============

Download Docker Desktop
^^^^^^^^^^^^^^^^^^^^^^^
* https://www.docker.com/products/docker-desktop

Install Docker Desktop
^^^^^^^^^^^^^^^^^^^^^^
* Double-click ``Docker.dmg`` (Mac) or  ``Docker for Windows Installer`` (Windows)  to start the install process.

  .. image:: img/install_mac.png
     :height: 125
     :width: 300

Start Docker Desktop
^^^^^^^^^^^^^^^^^^^^
* When the installation finishes, Docker starts automatically. 
  If not, please go to Application and double-click the Docker app

  .. image:: img/application.png
     :height: 283
     :width: 500

Open command-line terminal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Windows: search for ``cmd``

  .. image:: img/CLI_windows.png
     :height: 400
     :width: 472

* Mac:

  .. image:: img/CLI1.png
     :height: 350
     :width: 482

  .. image:: img/CLI2.png
     :height: 242
     :width: 482

* Run the following command:

::

   docker pull chihyingdeng/clinical_regex
   docker run -p 80:80 chihyingdeng/clinical_regex

Open the browser
^^^^^^^^^^^^^^^^^
* Go to http://localhost/

  .. image:: img/localhost.png
     :height: 30
     :width: 521

* You can also open the browser from docker dashboard, stop, or start the docker image.

  .. image:: img/docker.png
     :height: 243
     :width: 175

  .. image:: img/docker_dashboard.png
     :height: 400
     :width: 682