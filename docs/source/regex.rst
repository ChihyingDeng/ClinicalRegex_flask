Commonly used Regex
===================

+--------------+------------------------------------------------+
|``.``         |any character except newline                    |
+--------------+------------------------------------------------+
|``\w\d\s``    |word, digit, whitespace                         |
+--------------+------------------------------------------------+
|``\W\D\S``    |not word, digit, whitespace                     |
+--------------+------------------------------------------------+
|``[abc]``     |any of a, b, or c                               |
+--------------+------------------------------------------------+
|``[^abc]``    |not a, b, or c                                  |
+--------------+------------------------------------------------+
|``[a-g]``     |character between a & g                         |
+--------------+------------------------------------------------+
|``^abc$``     |start / end of the string                       |
+--------------+------------------------------------------------+
|``\b\B``      |word, not-word boundary                         |
+--------------+------------------------------------------------+
|``(?:abc)``   |non-capturing group                             |
+--------------+------------------------------------------------+
|``(?=abc)``   |positive lookahead (if followed by pattern)     |
+--------------+------------------------------------------------+
|``(?!abc)``   |negative lookahead (if not followed by pattern) |
+--------------+------------------------------------------------+
|``(?<!abc)``  |negative lookahead (if not preceded by pattern) |
+--------------+------------------------------------------------+
|``a*a+a?``    |0 or more, 1 or more, 0 or 1                    |
+--------------+------------------------------------------------+
|``a{5}a{2,}`` |exactly five, two or more                       |
+--------------+------------------------------------------------+
|``a{1,3}``    |between one & three                             |
+--------------+------------------------------------------------+
|``a+?a{2,}?`` |match as few as possible                        |
+--------------+------------------------------------------------+
|``ab|cd``     |match ab or cd                                  |
+--------------+------------------------------------------------+

Please visit https://regexr.com for more information

Example
^^^^^^^
+------------------------------+-------------------------------------------------------------------+
|``goal (of|for) cares?``      |goal of care, goal for care, goal of cares, goal for cares         |
+------------------------------+-------------------------------------------------------------------+
|``ECOG\s{0,2}[1-3]``          |ECOG1,ECOG2,ECOG3,ECOG 1,ECOG 2,ECOG 3,ECOG  1,ECOG  2,ECOG  3     |
+------------------------------+-------------------------------------------------------------------+
|``hypertension(?! crisis)``   |It will only capture 'hypertension' without 'hypertension crisis'  |
+------------------------------+-------------------------------------------------------------------+
|``(?<!superior )mediastinum`` |It will only capture 'mediastinum' without 'superior mediastinum'  |
+------------------------------+-------------------------------------------------------------------+
* Please note that, the negative lookahead will only accept fixed length of text, you can' write the Regex as ``(?<!(abc|abcdef))zzzz``, because abc and abcdef have different length. Please use ``(?<!abc)(?<!abcdef)zzzz`` instead.