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

Open Command-line interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Run the following commands:

::

   docker pull chihyingdeng/clinical_regex
   docker run -p 80:80 chihyingdeng/clinical_regex

* Here's some commonly used command-line interface:

  + Windows: search for ``cmd``

    .. image:: img/CLI_windows.png
       :height: 400
       :width: 472

  + Mac:

    .. image:: img/CLI1.png
       :height: 350
       :width: 482

    .. image:: img/CLI2.png
       :height: 242
       :width: 482

Open the browser
^^^^^^^^^^^^^^^^^
* Go to http://localhost/

  .. image:: img/localhost.png
     :height: 30
     :width: 521

* You can also open the browser from docker's dashboard and stop the docker image after you've done.

  .. image:: img/dashboard.png
     :height: 300
     :width: 651

 * After installation, if you want to start the ClinicalRegex program again, please restart the docker image and open the browser.