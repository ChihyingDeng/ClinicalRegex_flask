import csv
import re
import string
import sys
import numpy as np
import pandas as pd


def _remove_punctuation(s):
    return s.translate(None, string.punctuation)


class NotePhraseMatches(object):
    """Describes all phrase matches for a particular RPDR Note"""

    def __init__(self, note_dict):
        self.note_dict = note_dict
        self.phrase_matches = []

    def add_phrase_match(self, phrase_match):
        self.phrase_matches.append(phrase_match)

    def finalize_phrase_matches(self):
        self.phrase_matches.sort(key=lambda x: x.match_start)


class PhraseMatch(object):
    """Describes a single phrase match to a single RPDR Note for a phrase."""

    def __init__(self, extracted_value, match_start, match_end, phrase):
        # Binary 0/1s for extracting phrase presence, else numerical value.
        self.extracted_value = extracted_value
        self.match_start = match_start
        self.match_end = match_end
        self.phrase = phrase


class ClinicianNotes(object):

    PHRASE_TYPE_WORD = 0
    PHRASE_TYPE_NUM = 1
    PHRASE_TYPE_DATE = 2

    RPDR_NOTE_KEYWORD = 'NOTE'
    RPDR_PATIENT_KEYWORD = 'EMPI'

    def __init__(
            self,
            input_file,
            row,
            note_keyword="NOTE",
            patient_keyword="EMPI",
            extract_numerical_value=False):

        self.report_description = None
        self.report_type = None
        self.ignore_punctuation = False

        phrase_type = ""
        extract_date = False

        if extract_numerical_value:
            self.phrase_type = PHRASE_TYPE_NUM
        elif extract_date:
            self.phrase_type = PHRASE_TYPE_DATE
        else:
            self.phrase_type = PHRASE_TYPE_WORD

        self.patient_keyword = patient_keyword
        self.note_keyword = note_keyword
        self.extract_numerical_value = extract_numerical_value
        self.note_dicts = input_file.to_dict('records')

    def search_phrases(self, phrases):
        self.phrases = [p.strip() for p in phrases.split(',')]
        return(self._extract_values_from_notes(self.phrases))

    def _extract_values_from_notes(self, phrases):
        """Return a list of NotePhraseMatches for each note in note_dict."""
        note_phrase_matches = []

        if self.ignore_punctuation:
            phrases = [_remove_punctuation(phrase) for phrase in phrases]

        for note_dict in self.note_dicts:
            if self.ignore_punctuation:
                note_dict[self.note_keyword].translate(
                    None, string.punctuation)
            phrase_matches = self._extract_phrase_from_notes(note_dict)
            note_phrase_matches.append(phrase_matches)

        return(note_phrase_matches)

    def _extract_phrase_from_notes(self, note_dict):
        """Return a PhraseMatch object with the value as a binary 0/1 indicating
        whether one of the phrases was found in note"""

        string_lookup = {
            self.PHRASE_TYPE_WORD: [
                r'(^|(?<=\W))%s($|(?=\W))'],
            self.PHRASE_TYPE_NUM: [r'(?:%s)\s*(?:of|is|was|were|are|\:)?[:]*[\s]*([0-9]+\.?[0-9]*)'],
            self.PHRASE_TYPE_DATE: [
                r'(?:%s)\s*(?:of|is|was|were|are|\:)?[:]*[\s]*(\d+/\d+/\d+)',
                r'(?:%s)\s*(?:of|is|was|were|are|\:)?[:]*[\s]*(\d+-\d+-\d+)']}

        pattern_strings = string_lookup[self.phrase_type]

        try:
            note = str(note_dict[self.note_keyword])
        except KeyError:
            print("Wrong Note Keyword entered")
            raise

        phrase_matches = NotePhraseMatches(note_dict)

        for phrase in self.phrases:

            for pattern_string in pattern_strings:

                pattern_string = pattern_string % phrase
                re_flags = re.I | re.M | re.DOTALL
                pattern = re.compile(pattern_string, flags=re_flags)
                match_iter = pattern.finditer(note)

                try:
                    while True:
                        match = next(match_iter)

                        try:
                            float_create = float(match.groups()[0])
                        except ValueError:
                            float_create = None

                        extracted_value_lookup = {
                            self.PHRASE_TYPE_WORD: 1,
                            self.PHRASE_TYPE_NUM: float_create,
                            self.PHRASE_TYPE_DATE: match.groups()[0]

                        }

                        extracted_value = extracted_value_lookup[self.phrase_type]

                        new_match = PhraseMatch(extracted_value, match.start(),
                                                match.end(), phrase)

                        phrase_matches.add_phrase_match(new_match)

                except StopIteration:
                    continue

        phrase_matches.finalize_phrase_matches()
        return phrase_matches

    def _findMaches(self, note_phrase_matches, note_key):
        dict_list = []
        for note_phrase_match in note_phrase_matches:
            note = note_phrase_match.note_dict[self.note_keyword]
            matches = []
            for phrase_match in note_phrase_match.phrase_matches:
                match_start = phrase_match.match_start
                match_end = phrase_match.match_end
                matched_text = note[match_start:match_end]
                char_start = re.search(r'\w', matched_text).start()
                match_start += char_start
                matched_text = matched_text.strip()
                match_end = match_start + len(matched_text)
                matches.append((match_start, match_end))

        return matches


PHRASE_TYPE_WORD = 0
PHRASE_TYPE_NUM = 1
PHRASE_TYPE_DATE = 2

RPDR_NOTE_KEYWORD = 'NOTE'
RPDR_PATIENT_KEYWORD = 'EMPI'


def run_regex(
        input_filename,
        phrases,
        row,
        note_keyword=RPDR_NOTE_KEYWORD,
        patient_keyword=RPDR_PATIENT_KEYWORD,
        extract_numerical_value=False,
        extract_date=False,
        report_description=None,
        report_type=None,
        ignore_punctuation=False):

    note = ClinicianNotes(
        input_filename,
        row,
        note_keyword=note_keyword,
        patient_keyword=patient_keyword)
    note_phrase_matches = note.search_phrases(phrases)
    return note._findMaches(note_phrase_matches, note_keyword)
