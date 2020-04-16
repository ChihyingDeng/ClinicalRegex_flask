from .extract_values import run_regex
import re
import os
import pandas as pd
import bisect
import spacy
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
nlp.max_length = 3000000


class ValueCounts:
    def __init__(self):
        self.label = None
        self.annotation = None
        self.label_idx = None
        self.annotation_idx = None
        self.label_prog = None
        self.annotation_prog = None
        self.label_prog_str = None
        self.annotation_prog_str = None


class DataModel:
    def __init__(self):
        self.input_fname = None
        self.output_fname = None
        self.input_df = pd.DataFrame([])
        self.output_df = pd.DataFrame([])
        self.cols = None
        self.cols_dict = None
        self.pt_ID = None
        self.report_text = None
        self.patient_level = True
        self.positive_hit = True
        self.display_words = 100
        self.label_name = []
        self.phrases = []
        self.allphrases = []
        self.current_row_index = None
        self.num_label = None
        self.num_keywords = None
        self.matches_text = []
        self.matches_display = None
        self.matches_value = []
        self.annotated_value = None
        self.search_value = 1
        self.load_annotation = False
        self.save = True
        self.update_keyword = False
        self.lemmatization = False
        self.font_size = 10

    def is_empty(self):
        return self.output_df.empty

    def sort_data(self):
        try:
            if any(self.input_df[self.pt_ID].isna()):
                self.input_df = self.input_df[~self.input_df[self.pt_ID].isna()].reset_index(drop=True)
            if any(self.input_df[self.report_text].isna()):
                self.input_df = self.input_df[~self.input_df[self.report_text].isna()].reset_index(drop=True)

            # move id and report text columns to front
            if not self.update_keyword:
                input_columns = self.input_df.columns.values.tolist()
                output_columns = [self.pt_ID, self.report_text] + \
                    list(set(input_columns) - set([self.pt_ID, self.report_text]))
                self.output_df = self.input_df[output_columns]
            else:
                annotated_df = self.output_df[~self.output_df['L1_' + self.label_name[0]].isna()].copy()

            # Concate report text on patient's level
            if self.patient_level:
                if self.update_keyword:
                    output_df = self.input_df
                    output_df[self.report_text] = output_df.apply(self._add_header, axis=1)
                    output_df = output_df.groupby(self.pt_ID)[self.report_text].apply(
                        lambda x: '\n'.join(x)).to_frame().reset_index()
                    output_df = self.output_df.merge(
                        output_df.rename(
                            columns={
                                self.report_text: 'new_' +
                                self.report_text}),
                        on=self.pt_ID)
                    self.output_df[self.report_text] = output_df['new_' + self.report_text]
                else:
                    self.output_df[self.report_text] = self.output_df.apply(self._add_header, axis=1)
                    self.output_df = self.output_df.groupby(self.pt_ID)[self.report_text].apply(
                        lambda x: '\n'.join(x)).to_frame().reset_index()
            else:
                self.output_df[self.report_text] = self.output_df.apply(self._add_header, axis=1)

            # clean phrases
            self.output_df[self.report_text] = self.output_df[self.report_text].astype(
                str).apply(lambda x: self._clean_phrase(x))
            self.allphrases = []
            for i in range(self.num_label):
                self.phrases[i] = self.phrases[i].replace(', ', ',')
                self.allphrases.extend(self.phrases[i].split(','))
                if not self.update_keyword:
                    length = len(self.output_df)
                    self.output_df.insert(3 * i + 2, 'L%d_' % (i + 1) + self.label_name[i], [None] * length)
                    self.output_df.insert(3 * i + 3, 'L%d_' % (i + 1) + self.label_name[i] + '_span', [None] * length)
                    self.output_df.insert(3 * i + 4, 'L%d_' % (i + 1) + self.label_name[i] + '_text', [None] * length)

            if self.lemmatization:
                # Lemmatization and update phrases
                lemma_phrases, lemma_phrases_dict = [], {}
                for i in range(self.num_label):
                    update_phrases = []
                    for phrase in self.phrases[i].split(','):
                        doc = nlp(phrase.lower())
                        # don't lemmatize the phrases when phrases containing regular expression
                        if not re.search(r'[^\w\s/]', phrase):
                            lemma = ' '.join([token.lemma_ for token in doc])
                        else:
                            lemma = phrase
                        update_phrases.append(lemma)
                        lemma_phrases_dict[lemma] = {phrase.lower(), lemma}
                    lemma_phrases.extend(update_phrases)
                    self.phrases[i] = ','.join(update_phrases)

                # update lemma_phrases_dict
                text = self.output_df[self.report_text].str.cat(sep=' ')
                text = re.sub(r'[^\w\s]|[\d_]', '', text)
                doc = nlp(' '.join(set(text.lower().replace('\n', ' ').split(' '))))
                for token in doc:
                    if token.lemma_ in lemma_phrases:
                        lemma_phrases_dict[token.lemma_].add(token.text)
                for i in range(self.num_label):
                    update_phrases = []
                    for phrase in self.phrases[i].split(','):
                        if len(lemma_phrases_dict[phrase]) > 1:
                            update_phrases.append('(' + '|'.join(lemma_phrases_dict[phrase]) + ')')
                        else:
                            update_phrases.append(''.join(lemma_phrases_dict[phrase]))
                    self.allphrases.extend(update_phrases)
                    self.phrases[i] = ','.join(update_phrases)

            # search keywords set
            self.output_df['regex'] = self.output_df[self.report_text].apply(lambda x: self._search_keywords(x))
            if all(self.output_df['regex'] == 0):
                self.output_df['regex'] = 1
                return "No keywords found!"

            if self.update_keyword:
                annotated_id = annotated_df[self.pt_ID].tolist()
                not_annotated_df = self.output_df[~self.output_df[self.pt_ID].isin(annotated_id)]
                self.num_keywords = (len(annotated_df) +
                                     not_annotated_df[not_annotated_df['regex'] == 1].shape[0], self.output_df.shape[0])
                self.current_row_index = len(annotated_id) - 1
                not_annotated_df = not_annotated_df.sort_values(by='regex', ascending=False)
                self.output_df = pd.concat([annotated_df, not_annotated_df],
                                           axis=0).reset_index(drop=True).drop(columns=['regex'])
            else:
                self.num_keywords = (self.output_df[self.output_df['regex'] == 1].shape[0], self.output_df.shape[0])
                self.output_df = self.output_df.sort_values(
                    by='regex',
                    ascending=False).reset_index(
                    drop=True).drop(
                    columns=['regex'])

            self.output_df['keywords'] = ''
            self.output_df.loc[0, 'keywords'] = str(self.num_keywords[0]) + '-' + str(self.num_keywords[1])
            for i in range(self.num_label):
                self.output_df.loc[i + 1, 'keywords'] = str(self.phrases[i])
            if self.update_keyword:
                self.output_df.loc[self.num_label + 1, 'keywords'] = self.current_row_index
        except BaseException:
            return "Something went wrong, did you select an appropriately columns or using the right format of regex?"
        return "done"

    def _add_header(self, df):
        cols = df.index.tolist()
        cols.remove(self.report_text)
        return '[Header_Start]' + '|'.join(list(map(str, df[cols].tolist()))) + \
            '[Header_End]' + df[self.report_text]

    def _clean_phrase(self, phrase):
        cleaned = str(phrase.replace('||', '|').replace('\\r', '\\n'))
        cleaned = re.sub(r'(\n+|\r\r)', '\n', cleaned)
        cleaned = re.sub(r'( +|\t+)', ' ', cleaned)
        cleaned = re.sub(r'\r', '', cleaned)
        return str(cleaned.strip())

    def _search_keywords(self, text):
        for phrase in self.allphrases:
            if re.search(r'(^|(?<=\W))%s($|(?=\W))' % (phrase.lower()), text.lower()):
                return 1
        return 0

    def combine_keywords_notes(self, text):
        output = []
        for t in text.split('[Header_Start]'):
            if not t:
                continue
            header = '%s\n%s\n%s\n' % ('=' * 100, t.split('[Header_End]')[0], '=' * 100)
            note = t.split('[Header_End]')[-1]
            if self.display_words == 0:
                df = pd.DataFrame([note], columns=['text'])
            else:
                df = pd.DataFrame(map(' '.join, zip(*[iter(note.split(' '))] * self.display_words)), columns=['text'])
                d, m = divmod(len(note.split(' ')), self.display_words)
                if m > 0:
                    df.loc[d] = ' '.join(note.split(' ')[d*self.display_words:])
            df['regex'] = df['text'].apply(lambda x: self._search_keywords(x))
            if any(df['regex'] == 1):
                output.append(header + df[df['regex'] == 1].reset_index(drop=True)['text'].str.cat(sep='\n----\n'))
        return '\n'.join(output) if output else 'No keywords found!'

    def _find_matches(self, phrases, label_name, current_note_df):
        match_indices = current_note_df.at[self.current_row_index, label_name]

        if match_indices and isinstance(match_indices, str):
            match_indices = [[int(j) for j in i.split('-')] for i in match_indices.split('|')]
        else:
            match_indices = run_regex(
                current_note_df,
                phrases,
                self.current_row_index,
                self.report_text,
                self.pt_ID)

        return match_indices

    def get_matches_indices(self, length, text):
        self.matches_display = {i: [None] for i in range(len(length))}
        self.matches_text = []
        self.matches_value = []
        for i in range(self.num_label):
            match_indices = self._find_matches(
                self.phrases[i],
                "L%d_" % (i + 1) + self.label_name[i] + '_span',
                self.output_df.iloc[[self.current_row_index]])
            if match_indices:
                for start, end in match_indices:
                    idx = min(bisect.bisect(length, start), len(self.matches_display) - 1)
                    if idx > 0:
                        start = start - length[idx - 1]
                        end = end - length[idx - 1]
                    if self.matches_display[idx] == [None]:
                        self.matches_display[idx] = [(start, end, i + 1)]
                    else:
                        self.matches_display[idx].append((start, end, i + 1))
            self.matches_text.append(match_indices)

            value = self.output_df.at[self.current_row_index, "L%d_" % (i + 1) + self.label_name[i]]
            if not value or pd.isnull(value):
                value = 1 if match_indices else 0
            elif isinstance(value, str):
                value = int(value)
            elif not isinstance(value, int):
                value = value.astype('Int64')
            self.matches_value.append(value)

        for i in range(len(text)):
            if self.matches_display[i] != [None]:
                prev, new_list = 0, []
                for start, end, label in sorted(self.matches_display[i], key=lambda x: x[0]):
                    new_list.append((prev, start, end, label))
                    prev = end
                self.matches_display[i] = new_list

    def save_matches(self, value):
        for i in range(self.num_label):
            match = '|'.join(['{}-{}'.format(start, end) for start, end in self.matches_text[i]])
            report = self.output_df.at[self.current_row_index, self.report_text]
            match_text = '|'.join([report[start:end] for start, end in self.matches_text[i]])
            self.annotated_value = value
            self.output_df.loc[self.current_row_index, 'L%d_' % (i + 1) + self.label_name[i]] = value[i]
            self.output_df.loc[self.current_row_index, 'L%d_' % (i + 1) + self.label_name[i] + '_span'] = match
            self.output_df.loc[self.current_row_index, 'L%d_' % (i + 1) + self.label_name[i] + '_text'] = match_text
        self.output_df.loc[self.num_label + 1, 'keywords'] = self.current_row_index
        self.output_df.to_csv('output/' + self.output_fname, index=False)
        self.output_df.drop(columns=[self.report_text]).to_csv('output/noreport_' + self.output_fname, index=False)
        self.save = True

    def get_value_counts(self):
        value_counts = ValueCounts()
        notes = self.num_keywords[0] + 1e-8 if self.positive_hit else self.num_keywords[1] + 1e-8
        value_counts.label = [(self.label_name[i], len(self.output_df[self.output_df['L%d_%s' %
                                                                                     (i + 1, self.label_name[i])] == self.search_value])) for i in range(self.num_label)]
        value_counts.annotation = (len(self.output_df.loc[:notes -
                                                          1][self.output_df.loc[:notes -
                                                                                1]['L1_' +
                                                                                   self.label_name[0]].isna()]), len(self.output_df[~self.output_df['L1_' +
                                                                                                                                                    self.label_name[0]].isna()]))
        value_counts.label_idx = []
        for i in range(self.num_label):
            value_counts.label_idx.append(self.output_df.index[self.output_df['L%d_' % (
                i + 1) + self.label_name[i]] == self.search_value].tolist())
        value_counts.annotation_idx = (self.output_df.loc[:notes -
                                                          1].index[self.output_df.loc[:notes -
                                                                                      1]['L1_' +
                                                                                         self.label_name[0]].isna()].tolist(), self.output_df.index[~self.output_df['L1_' +
                                                                                                                                                                    self.label_name[0]].isna()].tolist())
        value_counts.label_prog = [round(100 * value_counts.label[i][1] / notes, 2) for i in range(self.num_label)]
        value_counts.annotation_prog = (
            round(
                100 *
                value_counts.annotation[0] /
                notes,
                2),
            round(
                100 *
                value_counts.annotation[1] /
                notes,
                2))
        value_counts.label_prog_str = ['width: ' + str(int(i)) + '%;' for i in value_counts.label_prog]
        value_counts.annotation_prog_str = ['width: ' + str(int(i)) + '%;' for i in value_counts.annotation_prog]

        return value_counts

    def rpdr_to_csv(self):
        # reformat RPDR to CSV file
        with open(self.input_fname, 'r') as file:
            data, header, fields = [], [], []
            for line in file:
                line = line.rstrip()
                if line.strip() == '':
                    continue
                if not header:
                    if line.count('|') < 8:
                        return 'error'
                    header = [field.lower().strip()
                              for field in line.split('|')]
                    continue
                if not fields and '|' in line:
                    fields = [field.lower().strip()
                              for field in line.split('|')]
                    fields[-1] = line
                    report = []
                elif '[report_end]' in line:
                    report.append(line)
                    fields[-1] += '\n'.join(report)
                    data.append(fields)
                    fields = []
                else:
                    report.append(line)
        self.input_fname = ''.join(self.input_fname.split('.')[:-1]) + '.csv'
        data = pd.DataFrame(data, columns=header)
        data.to_csv(self.input_fname, index=False)
        self.input_df = data
