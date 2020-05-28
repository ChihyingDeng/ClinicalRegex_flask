from wtforms import Form, BooleanField, StringField, PasswordField, FileField, validators, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, InputRequired, Length, Optional
from wtforms import TextField, SelectField, BooleanField, StringField, IntegerField, SubmitField, ValidationError, validators, TextAreaField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed


class LoadForm(FlaskForm):
    inputfile = FileField(u'Input File', [FileRequired()])
    outputfile = StringField(u'Output File', [validators.optional(), validators.length(max=10)], default="output.csv")
    run_or_load = SelectField('Function', coerce=int, validators=[InputRequired],
                              choices=[(0, 'Run Regex'), (1, 'Load Annotation'), (2, 'RPDR to CSV')])
    submit_button = SubmitField('Load Annotation')


class RegexForm(FlaskForm):
    pt_ID = SelectField('ID column', coerce=int, validators=[InputRequired])
    report_text = SelectField('Text column', coerce=int, validators=[InputRequired])
    display_words = SelectField('Display words', coerce=int, validators=[InputRequired],
                              choices=[(100, '100 words'), (200, '200 words'), (300, '300 words'), 
                              (400, '400 words'), (0, 'entire note')])
    label1_name = StringField(u'Label 1', [validators.required(), validators.length(max=10)],
                              render_kw={"placeholder": "Label1 name"})
    label1_keyword = TextAreaField(u'', [validators.required(), validators.length(max=200)],
                                   render_kw={"placeholder": "Label1 keywords"})
    label2_name = StringField(u'Label 2', [validators.optional(), validators.length(max=10)],
                              render_kw={"placeholder": "Label2 name (optional)"})
    label2_keyword = TextAreaField(u'', [validators.optional(), validators.length(max=200)],
                                   render_kw={"placeholder": "Label2 keywords (optional)"})
    label3_name = StringField(u'Label 3', [validators.optional(), validators.length(max=10)],
                              render_kw={"placeholder": "Label3 name (optional)"})
    label3_keyword = TextAreaField(u'', [validators.optional(), validators.length(max=200)],
                                   render_kw={"placeholder": "Label3 keywords (optional)"})
    patient_level = BooleanField('Patient Level', default=True)
    positive_hit = BooleanField('Display notes with keywords only', default=True)
    lemmatization = BooleanField('Lemmatization', default=False)
    submit_button = SubmitField('Run Regex')
    noreview_button = SubmitField('Run Regex without review')


class UpdateForm(FlaskForm):
    label1_name = StringField(u'Label 1', [validators.required(), validators.length(max=10)],
                              render_kw={'readonly': True})
    label1_keyword = TextAreaField(u'', [validators.required(), validators.length(max=200)])
    label2_name = StringField(u'Label 2', [validators.optional(), validators.length(max=10)],
                              render_kw={'readonly': True})
    label2_keyword = TextAreaField(u'', [validators.optional(), validators.length(max=200)])
    label3_name = StringField(u'Label 3', [validators.optional(), validators.length(max=10)],
                              render_kw={'readonly': True})
    label3_keyword = TextAreaField(u'', [validators.optional(), validators.length(max=200)])
    submit_button = SubmitField('Update Regex')


class ValueFormOne(FlaskForm):
    label1_value = IntegerField(u'Label 1')
    submit_prev = SubmitField('Prev')
    submit_next = SubmitField('Next')
    submit_save = SubmitField('Save')


class ValueFormTwo(FlaskForm):
    label1_value = IntegerField(u'Label 1',
                                render_kw={"placeholder": "annotation value"})
    label2_value = IntegerField(u'Label 2',
                                render_kw={"placeholder": "annotation value"})
    submit_prev = SubmitField('Prev')
    submit_next = SubmitField('Next')
    submit_save = SubmitField('Save')


class ValueFormThree(FlaskForm):
    label1_value = IntegerField(u'Label 1',
                                render_kw={"placeholder": "annotation value"})
    label2_value = IntegerField(u'Label 2',
                                render_kw={"placeholder": "annotation value"})
    label3_value = IntegerField(u'Label 3',
                                render_kw={"placeholder": "annotation value"})
    submit_prev = SubmitField('Prev')
    submit_next = SubmitField('Next')
    submit_save = SubmitField('Save')

class DownloadForm(FlaskForm):
    submit_download = SubmitField('Download')
    with_report = BooleanField('with report', default=True)


class ValueForm(FlaskForm):
    value = IntegerField('Value', validators=[DataRequired()], render_kw={"placeholder": "1"})
    submit_value = SubmitField('Refresh')

class Zoom(FlaskForm):
    submit_zoom_in = SubmitField('+')
    submit_zoom_out = SubmitField('-')
