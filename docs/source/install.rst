############
Installation
############

Mac User
========

Please install either by Docker or VirtualBox

1) Docker
---------

Download Docker Desktop
^^^^^^^^^^^^^^^^^^^^^^^
* https://www.docker.com/products/docker-desktop

* System Requirements: MacOS version 10.13 or later


Install Docker Desktop
^^^^^^^^^^^^^^^^^^^^^^
* Double-click ``Docker.dmg`` to start the install process.

  .. image:: img/install_mac.png
     :height: 125
     :width: 300

Start Docker Desktop
^^^^^^^^^^^^^^^^^^^^
* When the installation finishes, Docker starts automatically. If the docker is opened, you could find the logo on the top-right of your computer.

  .. image:: img/open_docker.png
     :height: 24
     :width: 480

* If not, please go to Application and double-click the Docker app

  .. image:: img/application.png
     :height: 272
     :width: 480

Open Command-line interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Run the following commands:

::

   docker pull chihyingdeng/clinical_regex
   docker run -p 80:80 chihyingdeng/clinical_regex

* Here's some commonly used command-line interface:

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

Video
^^^^^
.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
      <iframe width="560" height="315" src="https://www.youtube.com/embed/T3YnfIvBK-Y" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>

2) VirtualBox
-------------

Download VirtualBox
^^^^^^^^^^^^^^^^^^^
* https://www.virtualbox.org/wiki/Downloads


Install VirtualBox
^^^^^^^^^^^^^^^^^^
* Double-click ``VirtualBox-OSX.dmg`` or  ``VirtualBox-Win.exe`` to start the install process.

  .. image:: img/install_virtualbox.png
     :height: 167
     :width: 309

* Please allow apps downloaded from app store and identified developers in the "Security & Privacy" Setting

  .. image:: img/security.png
     :height: 266
     :width: 309

Import appliance
^^^^^^^^^^^^^^^^
* Double-click the file ``ClinicalRegex.ova`` or click on "File -> Import Appliance" in VirtualBox

  .. image:: img/import_appliance.png
     :height: 214
     :width: 533

* Hit "Continue" and then "Import"

* Start the "ClinicalRegex" Virtual Machine 

  .. image:: img/start_VM.png
     :height: 183
     :width: 533

Open the browser
^^^^^^^^^^^^^^^^
* Go to http://localhost:8080/

  .. image:: img/localhost_vb.png
     :height: 30
     :width: 521


Windows User
============
Video
-----
.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe width="560" height="315" src="https://www.youtube.com/embed/ofE-J63zPbE" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>
