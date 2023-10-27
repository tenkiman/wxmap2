# -*- coding: utf-8 -*-
"""\
Test the Unicode numbers module.
"""
from __future__ import unicode_literals
import unicodedata
from natsort.compat.py23 import py23_range, py23_unichr
from natsort.unicode_numbers import (
    numeric_hex,
    numeric_chars,
    numeric,
    digit_chars,
    digits,
)


def test_numeric_chars_contains_only_valid_unicode_numeric_characters():
    for a in numeric_chars:
        assert unicodedata.numeric(a, None) is not None


def test_digit_chars_contains_only_valid_unicode_digit_characters():
    for a in digit_chars:
        assert unicodedata.digit(a, None) is not None


def test_numeric_chars_contains_all_valid_unicode_numeric_characters():
    set_numeric_hex = set(numeric_hex)
    set_numeric_chars = set(numeric_chars)
    for i in py23_range(0X110000):
        try:
            a = py23_unichr(i)
        except ValueError:
            break
        if a in set('0123456789'):
            continue
        if unicodedata.numeric(a, None) is not None:
            assert i in set_numeric_hex
            assert a in set_numeric_chars


def test_digit_chars_contains_all_valid_unicode_digit_characters():
    set_numeric_hex = set(numeric_hex)
    set_numeric_chars = set(numeric_chars)
    for i in py23_range(0X110000):
        try:
            a = py23_unichr(i)
        except ValueError:
            break
        if a in set('0123456789'):
            continue
        if unicodedata.digit(a, None) is not None:
            assert i in set_numeric_hex
            assert a in set_numeric_chars


def test_combined_string_contains_all_characters_in_list():
    assert numeric == ''.join(numeric_chars)
    assert digits == ''.join(digit_chars)
