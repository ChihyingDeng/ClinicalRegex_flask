============
Installation
============

Docker
------

Download Docker Desktop
^^^^^^^^^^^^^^^^^^^^^^^
* https://www.docker.com/products/docker-desktop

* System Requirements: 

  + MacOS version 10.13 or later

  + Windows 10 Pro, Enterprise, or Education (Build 15063 or later)


Install Docker Desktop
^^^^^^^^^^^^^^^^^^^^^^
* Double-click ``Docker.dmg`` (Mac) or  ``Docker for Windows Installer`` (Windows)  to start the install process.

  .. image:: img/install_mac.png
     :height: 125
     :width: 300

* If you are using windows, make sure Hyper-V and Virtualization are enabled for Docker Desktop to function correctly.

  + https://docs.docker.com/docker-for-windows/troubleshoot/

  + `enable Hyper-V <https://docs.microsoft.com/en-us/archive/blogs/canitpro/step-by-step-enabling-hyper-v-for-use-on-windows-10>`_

  + `enable Virtualization <https://support.bluestacks.com/hc/en-us/articles/115003174386-How-can-I-enable-virtualization-VT-on-my-PC-#“8”>`_

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


.. raw:: html 

   <video height="400" width="600" controls src="img/installation.mp4"></video> 


VirtualBox
----------

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

