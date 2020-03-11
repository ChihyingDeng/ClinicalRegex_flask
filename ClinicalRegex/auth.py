import pandas as pd
import os
from flask import redirect, render_template, flash, Blueprint, request, url_for, send_file, send_from_directory
from flask import current_app as app
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination, get_page_parameter, get_per_page_parameter, get_page_args
from wtforms.fields import Label
from .forms import LoadForm, RegexForm, UpdateForm, ValueFormOne, ValueFormTwo, ValueFormThree, DownloadForm, ValueForm
from .datamodel import DataModel

bootstrap = Bootstrap(app)

# Blueprint Configuration
auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static')
WTF_CSRF_ENABLED = False
data = DataModel()


@auth_bp.route('/', methods=['GET', 'POST'])
def login_page():
    load = request.args.get('load')
    if load==True:
        form = LoadForm(run_or_load = 1)
    else:
        form = LoadForm(run_or_load = 0)

    if request.method == 'POST':
        if form.is_submitted() and form.data['inputfile']:
            inputfile_name = form.data['inputfile'].filename
            file_type = inputfile_name.split('.')[-1]
            if file_type in ['txt', 'csv', 'xls', 'xlsx']:
                try:
                    global data
                    data = DataModel()
                    # upload input file
                    data.input_fname = os.path.join('input', inputfile_name)
                    request.files['inputfile'].save(data.input_fname)
                    # read input file
                    if file_type == 'txt':
                        if data.rpdr_to_csv() == 'error':
                            flash('Invalid RPDR file')
                            return redirect(url_for('auth_bp.login_page',load=False))
                    elif file_type == 'csv':
                        data.input_df = pd.read_csv(data.input_fname)
                    else:
                        data.input_df = read_excel(data.input_fname)
                    data.output_fname = request.form.get('outputfile')
                    if form.data['run_or_load'] == 0:  # Run Regex
                        return redirect(url_for('auth_bp.run_regex'))
                    elif form.data['run_or_load'] == 1:  # Load Annotation
                        data.load_annotation = True
                        return redirect(url_for('auth_bp.annotation', jump=None))
                    else:  # RPDR to CSV
                        flash('File downloaded')
                        return send_file('../' + data.input_fname, mimetype='text/csv',
                                         attachment_filename=data.input_fname.split('/')[-1], as_attachment=True)
                except BaseException:
                    flash('Invalid file')
                    return redirect(url_for('auth_bp.login_page',load=False))

    return render_template('login.html',
                           form=form,
                           title='ClinicalRegex',
                           template='login-page',
                           body="select file")


@auth_bp.route('/run_regex', methods=('GET', 'POST'))
def run_regex():
    data.annotated_value = None
    data.output_df = pd.DataFrame([])
    try:
        if not data.cols_dict:
            cols = data.input_df.columns.values.tolist()
            data.cols_dict = {col.lower(): idx for idx, col in enumerate(cols)}
            data.cols = [(idx, col.lower()) for idx, col in enumerate(cols)]

        if not data.label_name:
            msg = ''
            pt_ID_default = data.cols_dict.get('empi') or data.cols_dict.get('id')
            report_text_default = data.cols_dict.get('report_text') or data.cols_dict.get('comments')
            form = RegexForm(pt_ID=pt_ID_default, report_text=report_text_default)
        else:
            msg = "The output file will be overwritten!!"
            if data.num_label == 1:
                form = RegexForm(pt_ID=data.cols_dict[data.pt_ID],
                                report_text=data.cols_dict[data.report_text],
                                label1_name=data.label_name[0],
                                label1_keyword=data.phrases[0])
            elif data.num_label == 2:
                form = RegexForm(pt_ID=data.cols_dict[data.pt_ID],
                                report_text=data.cols_dict[data.report_text],
                                label1_name=data.label_name[0],
                                label1_keyword=data.phrases[0],
                                label2_name=data.label_name[1],
                                label2_keyword=data.phrases[1])
            else:
                form = RegexForm(pt_ID=data.cols_dict[data.pt_ID],
                                report_text=data.cols_dict[data.report_text],
                                label1_name=data.label_name[0],
                                label1_keyword=data.phrases[0],
                                label2_name=data.label_name[1],
                                label2_keyword=data.phrases[1],
                                label3_name=data.label_name[2],
                                label3_keyword=data.phrases[2])

        form.pt_ID.choices = data.cols
        form.report_text.choices = data.cols
        if request.method == 'POST':
            if form.is_submitted() and form.data['label1_name'] and form.data['label1_keyword']:
                if not (form.data['label2_name'] and not form.data['label2_keyword']) and not (
                        form.data['label3_name'] and not form.data['label3_keyword']):
                    cols = data.input_df.columns.values.tolist()
                    data.pt_ID = cols[form.data['pt_ID']]
                    data.report_text = cols[form.data['report_text']]
                    data.patient_level = form.data['patient_level']
                    data.positive_hit = form.data['positive_hit']
                    data.phrases = [form.data['label1_keyword'], form.data['label2_keyword'], form.data['label3_keyword']]
                    data.label_name = [form.data['label1_name'], form.data['label2_name'], form.data['label3_name']]
                    return redirect(url_for('auth_bp.annotation', jump=None))

            flash('Please enter the name and keywords of label')
            return redirect(url_for('auth_bp.run_regex'))
    except:
        flash('Something went wrong')
        return redirect(url_for('auth_bp.login_page',load=False))

    return render_template('regex.html', form=form, msg=msg)


@auth_bp.route('/annotation', methods=('GET', 'POST'))
def annotation():
    try: 
        if not data.save and data.annotated_value:
            data.save_matches(data.annotated_value)
        data.save = False

        jump = request.args.get('jump')

        if data.is_empty() and data.load_annotation:
            data.phrases, data.label_name = [''] * 3, [''] * 3
            data.output_df = data.input_df
            cols = data.output_df.columns.values.tolist()
            if 'L1_' not in cols[2] or '_span' not in cols[3] or '_text' not in cols[4] or 'keywords' not in cols[-1]:
                flash('Please select the correct file to load the annotation')
                return redirect(url_for('auth_bp.login_page'))
            data.pt_ID, data.report_text = cols[:2]
            data.num_keywords = tuple(int(i) for i in data.output_df.loc[0, 'keywords'].split('-'))
            try:
                for i in range(3):
                    if 3 * i + 5 < len(cols) and 'L%d_' % (i + 1) in cols[3 * i + 2]:
                        data.label_name[i] = cols[3 * i + 2][3:]
                        data.phrases[i] = data.output_df.loc[i + 1, 'keywords']
                        data.num_label = i + 1
                    else:
                        break
            except BaseException:
                flash('Please select the correct file to load the annotation')
                return redirect(url_for('auth_bp.login_page', load=False))
        
        if data.label_name[2]:
            form = ValueFormThree()
            data.num_label = 3
        elif data.label_name[1]:
            form = ValueFormTwo()
            data.num_label = 2
        else:
            form = ValueFormOne()
            data.num_label = 1
        if data.update_keyword or (data.is_empty() and not data.load_annotation):
            msg = data.sort_data()
            if msg != "done":
                flash(msg)
                return redirect(url_for('auth_bp.run_regex'))

            
        # pagination
        if jump:
            start_page = int(jump) + 1
        elif data.load_annotation or data.update_keyword:
            start_page = int(data.output_df.loc[data.num_label + 1, 'keywords']) + 2
        else:
            start_page = 1

        data.update_keyword = False
        page = int(request.args.get('page', start_page))
        per_page = 1
        offset = (page - 1) * per_page
        total_length = data.num_keywords[0] if data.positive_hit else data.num_keywords[1]
        pagination = Pagination(page=page, total=total_length, search=False,
                                per_page=per_page, css_framework='bootstrap3',
                                inner_window=5, outer_window=0)

        text = data.output_df.loc[page - 1, data.report_text].split('\n')
        length = [len(text[0]) + 1]
        for i in range(1, len(text)):
            length.append(len(text[i]) + 1 + length[i - 1])
        header = 'Patient ID: ' if data.patient_level else 'Note ID: '
        id_text = [(header + str(data.output_df.loc[page - 1, data.pt_ID]), text)]
        data.current_row_index = page - 1
        data.get_matches_indices(length, text)
        if data.num_label > 2:
            form.label3_value.label = Label(field_id="label3_value", text=data.label_name[2])
            form.label3_value.render_kw = {"placeholder": data.matches_value[2]}
        if data.num_label > 1:
            form.label2_value.label = Label(field_id="label2_value", text=data.label_name[1])
            form.label2_value.render_kw = {"placeholder": data.matches_value[1]}
        if data.num_label > 0:
            form.label1_value.label = Label(field_id="label1_value", text=data.label_name[0])
            form.label1_value.render_kw = {"placeholder": data.matches_value[0]}

        if data.num_label > 0:
            value = [data.matches_value[0]] if not form.data['label1_value'] else [form.data['label1_value']]
        if data.num_label > 1:
            value.append(data.matches_value[1] if not form.data['label2_value'] else form.data['label2_value'])
        if data.num_label > 2:
            value.append(data.matches_value[2] if not form.data['label3_value'] else form.data['label3_value'])

        data.annotated_value = value
        value_counts = data.get_value_counts()

        downloadform = DownloadForm()
        if request.method == 'POST':
            if form.is_submitted() and form.submit_button.data:
                data.save_matches(data.annotated_value)
                value_counts = data.get_value_counts()

            if downloadform.validate_on_submit() and downloadform.submit_download.data:
                if downloadform.data['with_report']:
                    return send_file('../output/' + data.output_fname,
                        mimetype='text/csv',
                        attachment_filename=data.output_fname,
                        as_attachment=True)
                else:
                    return send_file('../output/noreport_' + data.output_fname,
                        mimetype='text/csv',
                        attachment_filename='noreport_' + data.output_fname,
                        as_attachment=True)
    except:
        flash('Something went wrong')
        return redirect(url_for('auth_bp.login_page', load=False))

    return render_template('annotation.html', form=form, downloadform=downloadform,
                           pagination=pagination, page=page, per_page=per_page,
                           id_text=id_text, matches=data.matches_display, num_keywords=data.num_keywords,
                           num_label=data.num_label, value_counts=value_counts)


@auth_bp.route('/value_counts', methods=('GET', 'POST'))
def value_counts():
    try:
        if not data.save and data.annotated_value:
            data.save_matches(data.annotated_value)

        if data.label_name[2]:
            form = ValueFormThree()
        elif data.label_name[1]:
            form = ValueFormTwo()
        else:
            form = ValueFormOne()

        if data.num_label > 2:
            form.label3_value.label = Label(field_id="label3_value", text=data.label_name[2])
            form.label3_value.render_kw = {'readonly': True}
        if data.num_label > 1:
            form.label2_value.label = Label(field_id="label2_value", text=data.label_name[1])
            form.label2_value.render_kw = {'readonly': True}
        if data.num_label > 0:
            form.label1_value.label = Label(field_id="label1_value", text=data.label_name[0])
            form.label1_value.render_kw = {'readonly': True}

        form.submit_button.render_kw = {'readonly': True}
        value_counts = data.get_value_counts()

        downloadform = DownloadForm()
        valueform = ValueForm()

        if request.method == 'POST':
            if downloadform.validate_on_submit() and downloadform.submit_download.data:
                return send_file(
                    '../output/' + data.output_fname,
                    mimetype='text/csv',
                    attachment_filename=data.output_fname,
                    as_attachment=True)
            if valueform.validate_on_submit() and valueform.submit_value.data:
                data.search_value = valueform.data['value']
                value_counts = data.get_value_counts()
                return redirect(url_for('auth_bp.value_counts'))
    except:
        flash('Something went wrong')
        return redirect(url_for('auth_bp.run_regex'))

    return render_template('valuecounts.html', form=form, downloadform=downloadform, valueform=valueform,
                           num_label=data.num_label, num_keywords=data.num_keywords, value_counts=value_counts)


@auth_bp.route('/update_keyword', methods=['GET', 'POST'])
def update_keyword():
    try:
        if data.is_empty():
            msg = "please run regex first!"
            pt_ID_default =  data.cols_dict.get('empi') or data.cols_dict.get('id')
            report_text_default = data.cols_dict.get('report_text') or data.cols_dict.get('comments')
            form = RegexForm(pt_ID=pt_ID_default, report_text=report_text_default)
            return redirect(url_for('auth_bp.run_regex'))
        data.annotated_value = None
        data.update_keyword = True
        if data.num_label == 1:
            form = UpdateForm(pt_ID=data.cols_dict[data.pt_ID],
                            report_text=data.cols_dict[data.report_text],
                            label1_name=data.label_name[0],
                            label1_keyword=data.phrases[0])
            form.label2_keyword.render_kw = {"placeholder": "", 'readonly': True}
            form.label3_keyword.render_kw = {"placeholder": "", 'readonly': True}
        elif data.num_label == 2:
            form = UpdateForm(pt_ID=data.cols_dict[data.pt_ID],
                            report_text=data.cols_dict[data.report_text],
                            label1_name=data.label_name[0],
                            label1_keyword=data.phrases[0],
                            label2_name=data.label_name[1],
                            label2_keyword=data.phrases[1])
            form.label3_keyword.render_kw = {"placeholder": "", 'readonly': True}
        else:
            form = UpdateForm(pt_ID=data.cols_dict[data.pt_ID],
                            report_text=data.cols_dict[data.report_text],
                            label1_name=data.label_name[0],
                            label1_keyword=data.phrases[0],
                            label2_name=data.label_name[1],
                            label2_keyword=data.phrases[1],
                            label3_name=data.label_name[2],
                            label3_keyword=data.phrases[2])

        msg = "The annotation values you have made won't be changed, please go back and make sure the annotation values are correct if necessary!!"
        if request.method == 'POST':
            if form.is_submitted() and form.data['label1_keyword']:
                data.phrases = [form.data['label1_keyword'], form.data['label2_keyword'], form.data['label3_keyword']]
                return redirect(url_for('auth_bp.annotation', jump=None))
            flash('Something went wrong')
            return redirect(url_for('auth_bp.login_page', load = False))
    except:
        flash('Something went wrong')
        return redirect(url_for('auth_bp.login_page',load=False))

    return render_template('regex.html', form=form, msg=msg)
