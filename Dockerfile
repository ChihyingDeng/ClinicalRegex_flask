FROM python:3.7
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
EXPOSE 80
CMD ["python", "app.py"]