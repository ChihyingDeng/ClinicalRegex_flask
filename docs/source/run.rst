Run ClinicalRegex
=================

Select Files
^^^^^^^^^^^^
* Please select the input file. The input file only accept RPDR(``.txt``), CSV(``.csv``), and Excel(``.xls, .xlsx``) format
* Please enter the name of output file
* Here's same the sample input files and output file: https://github.com/ChihyingDeng/ClinicalRegex_flask/tree/master/sample_files

  .. image:: img/select_file.png
     :height: 400
     :width: 681

Run Regex
^^^^^^^^^
* Please select the columns for ``patient ID`` when you on patient level; select the columns for ``note ID`` when you on note level (unselected patient level).
* Please select the columns for report text.
* Please enter the label name and the keyword set for the labels. You could only have one label and leave label 2 and label 3 blank.
* The keyword should be separated by ``,``.
* The report text will be lemmatized. For example, if you enter the keyword 'test', it will capture all the words like "test, tests, tested, testing'. If you only want to capture the word "test", please enter ``(test)``.
* You could also use regular expression in the keyword, but when you are using Regex, it won't apply lemmatization automatically.
* If ``Patient level`` is selected, the program will search all the notes belong to a patient and combine the text around the keyword together.
* If ``Display notes with keywords only`` is selected, the program will only display the notes/patients with keyword found, but the output file will still include all the notes/patients.

  .. image:: img/run_regex_keywords.png
     :height: 399 
     :width: 676

* The default value is ``1`` if the keywords exist in the report and ``0`` if not.
* If you go to next or previous notes, it will automatically saved the default value.
* **If you modify the annotation value, please remember to SAVE it** by clicking on the ``save`` button. Otherwise it will saved as default value.

  .. image:: img/run_regex_result.png
     :height: 487
     :width: 676

* If you click on ``Value Counts``, it will direct you to the page listing all the note you've annotated, not annotated. You could click on the number and jump to that note/patient.

  .. image:: img/not_annotated.png
     :height: 492
     :width: 676

*  You could also found out which note you annotated as ``1`` for each label. You could click on the number and jump to that note/patient to check for the report text and annotation.

  .. image:: img/label2.png
     :height: 492
     :width: 676 

*  You could download the output file with or without report text by clicking on the ``download`` button


Update Keywords
^^^^^^^^^^^^^^^
* You could update the keywords during the annotation. The annotation value you've made won't change. 
* Please **DO NOT** add any new keywords to the label when you're doing on the patient level. You could add limitaion to the keyword set. 
* For example, if you're searching for the keyword 'value' and there's 67 patients found with the keyword. You have already annotated for three patients.
 
  .. image:: img/value_before_update.png
     :height: 485
     :width: 676

* If you want to exclude the 'lab value' and 'component value', you could add condition to the keyword set.

  .. image:: img/update.png
     :height: 326
     :width: 676

* After updating the keyword, there are only 9 more patients you need to annotate. The annotation value and captured text of the previous 3 patients won't change.

  .. image:: img/value_after_update.png
     :height: 485
     :width: 676

* Again, please **DO NOT** add any new keywords to the label when you're doing on the patient level. The reports text for the previous patients you've annotated were searched using the old keyword set and combined together. If you hope to update the combined report text, please click on ``run regex`` and start over using the new keyword set.

Load Annotation
^^^^^^^^^^^^^^^
* Please select the output file you have saved before as an input file
* Please enter the name of output file
* Please choose the ``load annotation`` function

  .. image:: img/load_annotation.png
     :height: 337
     :width: 676

RPDR to CSV
^^^^^^^^^^^
* Please select a RPDR file as input and click on 'submit', a CSV file will be downloaded using the same name.