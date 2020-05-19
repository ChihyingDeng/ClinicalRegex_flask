# ClinicalRegex_flask
[![DOI](https://zenodo.org/badge/217560091.svg)](https://zenodo.org/badge/latestdoi/217560091)

## Install dependencies

```
sudo easy_install pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Start Program
```
python3 app.py
```
or
```
gunicorn -b 0.0.0.0:80 wsgi:app
```
## Docker image
```
chihyingdeng/clinical_regex
```

## Documentation
https://clinicalregex.readthedocs.io/

