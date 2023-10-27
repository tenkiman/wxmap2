# -*- coding: utf-8 -*-
"""\
Here are a collection of examples of how this module can be used.
See the README or the natsort homepage for more details.
"""
from __future__ import unicode_literals, print_function
import pytest
import sys
import warnings
import locale
from operator import itemgetter
from pytest import raises
from natsort import (
    natsorted,
    index_natsorted,
    natsort_key,
    versorted,
    index_versorted,
    humansorted,
    index_humansorted,
    natsort_keygen,
    order_by_index,
    ns,
    realsorted,
    index_realsorted,
    decoder,
    as_ascii,
    as_utf8,
)
from compat.locale import load_locale, has_locale_de_DE
from natsort.utils import _natsort_key


def test_decoder_returns_function_that_can_decode_bytes_but_return_non_bytes_as_is():
    f = decoder('latin1')
    a = 'bytes'
    b = 14
    assert f(b'bytes') == a
    assert f(b) is b  # returns as-is, same object ID
    if sys.version[0] == '3':
        assert f(a) is a  # same object returned on Python3 b/c only bytes has decode
    else:
        assert f(a) is not a
        assert f(a) == a  # not same object on Python2 because str can decode


def test_as_ascii_returns_bytes_as_ascii():
    assert decoder('ascii')(b'bytes') == as_ascii(b'bytes')


def test_as_utf8_returns_bytes_as_utf8():
    assert decoder('utf8')(b'bytes') == as_utf8(b'bytes')


def test_natsort_key_public_raises_DeprecationWarning_when_called():
    # Identical to _natsort_key
    # But it raises a deprecation warning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        assert natsort_key('a-5.034e2') == _natsort_key('a-5.034e2', key=None, alg=ns.I)
        assert len(w) == 1
        assert "natsort_key is deprecated as of 3.4.0, please use natsort_keygen" in str(w[-1].message)
    # It is called for each element in a list when sorting
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        a = ['a2', 'a5', 'a9', 'a1', 'a4', 'a10', 'a6']
        a.sort(key=natsort_key)
        assert len(w) == 7


def test_natsort_keygen_returns_natsort_key_with_alg_option():
    a = 'a-5.034e1'
    assert natsort_keygen()(a) == _natsort_key(a, None, ns.I)
    assert natsort_keygen(alg=ns.F | ns.S)(a) == _natsort_key(a, None, ns.F | ns.S)


def test_natsort_keygen_with_key_returns_same_result_as_nested_lambda_with_bare_natsort_key():
    a = 'a-5.034e1'
    f1 = natsort_keygen(key=lambda x: x.upper())

    def f2(x):
        return _natsort_key(x, lambda y: y.upper(), ns.I)
    assert f1(a) == f2(a)


def test_natsort_keygen_returns_key_that_can_be_used_to_sort_list_in_place_with_same_result_as_natsorted():
    a = ['a50', 'a51.', 'a50.31', 'a50.4', 'a5.034e1', 'a50.300']
    b = a[:]
    a.sort(key=natsort_keygen(alg=ns.F))
    assert a == natsorted(b, alg=ns.F)


def test_natsorted_returns_strings_with_numbers_in_ascending_order():
    a = ['a2', 'a5', 'a9', 'a1', 'a4', 'a10', 'a6']
    assert natsorted(a) == ['a1', 'a2', 'a4', 'a5', 'a6', 'a9', 'a10']


def test_natsorted_returns_list_of_numbers_sorted_as_signed_floats_with_exponents():
    a = ['a50', 'a51.', 'a50.31', 'a-50', 'a50.4', 'a5.034e1', 'a50.300']
    assert natsorted(a, alg=ns.REAL) == ['a-50', 'a50', 'a50.300', 'a50.31', 'a5.034e1', 'a50.4', 'a51.']


def test_natsorted_returns_list_of_numbers_sorted_as_unsigned_floats_without_exponents_with_NOEXP_option():
    a = ['a50', 'a51.', 'a50.31', 'a-50', 'a50.4', 'a5.034e1', 'a50.300']
    assert natsorted(a, alg=ns.N | ns.F | ns.U) == ['a5.034e1', 'a50', 'a50.300', 'a50.31', 'a50.4', 'a51.', 'a-50']
    # UNSIGNED is default
    assert natsorted(a, alg=ns.NOEXP | ns.FLOAT) == ['a5.034e1', 'a50', 'a50.300', 'a50.31', 'a50.4', 'a51.', 'a-50']


def test_natsorted_returns_list_of_numbers_sorted_as_unsigned_ints_with_INT_option():
    a = ['a50', 'a51.', 'a50.31', 'a-50', 'a50.4', 'a5.034e1', 'a50.300']
    assert natsorted(a, alg=ns.INT) == ['a5.034e1', 'a50', 'a50.4', 'a50.31', 'a50.300', 'a51.', 'a-50']
    # INT is default
    assert natsorted(a) == ['a5.034e1', 'a50', 'a50.4', 'a50.31', 'a50.300', 'a51.', 'a-50']


def test_natsorted_returns_list_of_numbers_sorted_as_unsigned_ints_with_DIGIT_and_VERSION_option():
    a = ['a50', 'a51.', 'a50.31', 'a-50', 'a50.4', 'a5.034e1', 'a50.300']
    assert natsorted(a, alg=ns.DIGIT) == ['a5.034e1', 'a50', 'a50.4', 'a50.31', 'a50.300', 'a51.', 'a-50']
    assert natsorted(a, alg=ns.VERSION) == ['a5.034e1', 'a50', 'a50.4', 'a50.31', 'a50.300', 'a51.', 'a-50']


def test_natsorted_returns_list_of_numbers_sorted_as_signed_ints_with_SIGNED_option():
    a = ['a50', 'a51.', 'a50.31', 'a-50', 'a50.4', 'a5.034e1', 'a50.300']
    assert natsorted(a, alg=ns.SIGNED) == ['a-50', 'a5.034e1', 'a50', 'a50.4', 'a50.31', 'a50.300', 'a51.']


def test_natsorted_returns_list_of_numbers_sorted_accounting_for_sign_with_SIGNED_option():
    a = ['a-5', 'a7', 'a+2']
    assert natsorted(a, alg=ns.SIGNED) == ['a-5', 'a+2', 'a7']


def test_natsorted_returns_list_of_numbers_sorted_not_accounting_for_sign_without_SIGNED_option():
    a = ['a-5', 'a7', 'a+2']
    assert natsorted(a) == ['a7', 'a+2', 'a-5']


def test_natsorted_returns_sorted_list_of_version_numbers_by_default_or_with_VERSION_option():
    a = ['1.9.9a', '1.11', '1.9.9b', '1.11.4', '1.10.1']
    assert natsorted(a) == ['1.9.9a', '1.9.9b', '1.10.1', '1.11', '1.11.4']
    assert natsorted(a, alg=ns.VERSION) == ['1.9.9a', '1.9.9b', '1.10.1', '1.11', '1.11.4']


def test_natsorted_returns_sorted_list_with_mixed_type_input_and_does_not_raise_TypeError_on_Python3():
    # You can mix types with natsorted.  This can get around the new
    # 'unorderable types' issue with Python 3.
    a = [6, 4.5, '7', '2.5', 'a']
    assert natsorted(a) == ['2.5', 4.5, 6, '7', 'a']
    a = [46, '5a5b2', 'af5', '5a5-4']
    assert natsorted(a) == ['5a5-4', '5a5b2', 46, 'af5']


def test_natsorted_with_mixed_input_returns_sorted_results_without_error():
    a = ['2', 'ä', 'b', 1.5, 3]
    assert natsorted(a) == [1.5, '2', 3, 'b', 'ä']


def test_natsorted_with_nan_input_returns_sorted_results_with_nan_last_with_NANLAST():
    a = ['25', 5, float('nan'), 1E40]
    # The slice is because NaN != NaN
    assert natsorted(a, alg=ns.NANLAST)[:3] == [5, '25', 1E40, float('nan')][:3]


def test_natsorted_with_nan_input_returns_sorted_results_with_nan_first_without_NANLAST():
    a = ['25', 5, float('nan'), 1E40]
    # The slice is because NaN != NaN
    assert natsorted(a)[1:] == [float('nan'), 5, '25', 1E40][1:]


def test_natsorted_with_mixed_input_raises_TypeError_if_bytes_type_is_involved_on_Python3():
    if sys.version[0] == '3':
        with raises(TypeError) as e:
            assert natsorted(['ä', b'b'])
        assert 'bytes' in str(e.value)
    else:
        assert True


def test_natsorted_raises_ValueError_for_non_iterable_input():
    with raises(TypeError) as err:
        natsorted(100)
    assert str(err.value) == "'int' object is not iterable"


def test_natsorted_recursivley_applies_key_to_nested_lists_to_return_sorted_nested_list():
    data = [['a1', 'a5'], ['a1', 'a40'], ['a10', 'a1'], ['a2', 'a5']]
    assert natsorted(data) == [['a1', 'a5'], ['a1', 'a40'], ['a2', 'a5'], ['a10', 'a1']]


def test_natsorted_applies_key_to_each_list_element_before_sorting_list():
    b = [('a', 'num3'), ('b', 'num5'), ('c', 'num2')]
    assert natsorted(b, key=itemgetter(1)) == [('c', 'num2'), ('a', 'num3'), ('b', 'num5')]


def test_natsorted_returns_list_in_reversed_order_with_reverse_option():
    a = ['a50', 'a51.', 'a50.31', 'a50.4', 'a5.034e1', 'a50.300']
    assert natsorted(a, reverse=True) == natsorted(a)[::-1]


def test_natsorted_sorts_OS_generated_paths_incorrectly_without_PATH_option():
    a = ['/p/Folder (10)/file.tar.gz',
         '/p/Folder/file.tar.gz',
         '/p/Folder (1)/file (1).tar.gz',
         '/p/Folder (1)/file.tar.gz']
    assert natsorted(a) == ['/p/Folder (1)/file (1).tar.gz',
                            '/p/Folder (1)/file.tar.gz',
                            '/p/Folder (10)/file.tar.gz',
                            '/p/Folder/file.tar.gz']


def test_natsorted_sorts_OS_generated_paths_correctly_with_PATH_option():
    a = ['/p/Folder (10)/file.tar.gz',
         '/p/Folder/file.tar.gz',
         '/p/Folder (1)/file (1).tar.gz',
         '/p/Folder (1)/file.tar.gz']
    assert natsorted(a, alg=ns.PATH) == ['/p/Folder/file.tar.gz',
                                         '/p/Folder (1)/file.tar.gz',
                                         '/p/Folder (1)/file (1).tar.gz',
                                         '/p/Folder (10)/file.tar.gz']


def test_natsorted_can_handle_sorting_paths_and_numbers_with_PATH():
    # You can sort paths and numbers, not that you'd want to
    a = ['/Folder (9)/file.exe', 43]
    assert natsorted(a, alg=ns.PATH) == [43, '/Folder (9)/file.exe']


def test_natsorted_returns_results_in_ASCII_order_with_no_case_options():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    assert natsorted(a) == ['Apple', 'Banana', 'Corn', 'apple', 'banana', 'corn']


def test_natsorted_returns_results_sorted_by_lowercase_ASCII_order_with_IGNORECASE():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    assert natsorted(a, alg=ns.IGNORECASE) == ['Apple', 'apple', 'Banana', 'banana', 'corn', 'Corn']


def test_natsorted_returns_results_in_ASCII_order_but_with_lowercase_letters_first_with_LOWERCASEFIRST():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    assert natsorted(a, alg=ns.LOWERCASEFIRST) == ['apple', 'banana', 'corn', 'Apple', 'Banana', 'Corn']


def test_natsorted_returns_results_with_uppercase_and_lowercase_letters_grouped_together_with_GROUPLETTERS():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    assert natsorted(a, alg=ns.GROUPLETTERS) == ['Apple', 'apple', 'Banana', 'banana', 'Corn', 'corn']


def test_natsorted_returns_results_in_natural_order_with_GROUPLETTERS_and_LOWERCASEFIRST():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    assert natsorted(a, alg=ns.G | ns.LF) == ['apple', 'Apple', 'banana', 'Banana', 'corn', 'Corn']


def test_natsorted_places_uppercase_letters_before_lowercase_letters_for_nested_input():
    b = [('A5', 'a6'), ('a3', 'a1')]
    assert natsorted(b) == [('A5', 'a6'), ('a3', 'a1')]


def test_natsorted_with_LOWERCASEFIRST_places_lowercase_letters_before_uppercase_letters_for_nested_input():
    b = [('A5', 'a6'), ('a3', 'a1')]
    assert natsorted(b, alg=ns.LOWERCASEFIRST) == [('a3', 'a1'), ('A5', 'a6')]


def test_natsorted_with_IGNORECASE_sorts_without_regard_to_case_for_nested_input():
    b = [('A5', 'a6'), ('a3', 'a1')]
    assert natsorted(b, alg=ns.IGNORECASE) == [('a3', 'a1'), ('A5', 'a6')]


def test_natsorted_with_LOCALE_returns_results_sorted_by_lowercase_first_and_grouped_letters():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    load_locale('en_US')
    assert natsorted(a, alg=ns.LOCALE) == ['apple', 'Apple', 'banana', 'Banana', 'corn', 'Corn']
    locale.setlocale(locale.LC_ALL, str(''))


def test_natsorted_with_LOCALE_and_CAPITALFIRST_returns_results_sorted_by_capital_first_and_ungrouped():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    load_locale('en_US')
    assert natsorted(a, alg=ns.LOCALE | ns.CAPITALFIRST) == ['Apple', 'Banana', 'Corn', 'apple', 'banana', 'corn']
    locale.setlocale(locale.LC_ALL, str(''))


def test_natsorted_with_LOCALE_and_LOWERCASEFIRST_returns_results_sorted_by_uppercase_first_and_grouped_letters():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    load_locale('en_US')
    assert natsorted(a, alg=ns.LOCALE | ns.LOWERCASEFIRST) == ['Apple', 'apple', 'Banana', 'banana', 'Corn', 'corn']
    locale.setlocale(locale.LC_ALL, str(''))


def test_natsorted_with_LOCALE_and_CAPITALFIRST_and_LOWERCASE_returns_results_sorted_by_capital_last_and_ungrouped():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    load_locale('en_US')
    assert natsorted(a, alg=ns.LOCALE | ns.CAPITALFIRST | ns.LOWERCASEFIRST) == ['apple', 'banana', 'corn', 'Apple', 'Banana', 'Corn']
    locale.setlocale(locale.LC_ALL, str(''))


def test_natsorted_with_LOCALE_and_en_setting_returns_results_sorted_by_en_language():
    load_locale('en_US')
    a = ['c', 'ä', 'b', 'a5,6', 'a5,50']
    assert natsorted(a, alg=ns.LOCALE | ns.F) == ['a5,6', 'a5,50', 'ä', 'b', 'c']
    locale.setlocale(locale.LC_ALL, str(''))


@pytest.mark.skipif(not has_locale_de_DE, reason='requires de_DE locale')
def test_natsorted_with_LOCALE_and_de_setting_returns_results_sorted_by_de_language():
    load_locale('de_DE')
    a = ['c', 'ä', 'b', 'a5,6', 'a5,50']
    assert natsorted(a, alg=ns.LOCALE | ns.F) == ['a5,50', 'a5,6', 'ä', 'b', 'c']
    locale.setlocale(locale.LC_ALL, str(''))


def test_natsorted_with_LOCALE_and_mixed_input_returns_sorted_results_without_error():
    load_locale('en_US')
    a = ['0', 'Á', '2', 'Z']
    assert natsorted(a) == ['0', '2', 'Z', 'Á']
    a = ['2', 'ä', 'b', 1.5, 3]
    assert natsorted(a, alg=ns.LOCALE) == [1.5, '2', 3, 'ä', 'b']
    locale.setlocale(locale.LC_ALL, str(''))


def test_versorted_returns_results_identical_to_natsorted():
    a = ['1.9.9a', '1.11', '1.9.9b', '1.11.4', '1.10.1']
    # versorted is retained for backwards compatibility
    assert versorted(a) == natsorted(a)


def test_realsorted_returns_results_identical_to_natsorted_with_REAL():
    a = ['a50', 'a51.', 'a50.31', 'a-50', 'a50.4', 'a5.034e1', 'a50.300']
    assert realsorted(a) == natsorted(a, alg=ns.REAL)


def test_humansorted_returns_results_identical_to_natsorted_with_LOCALE():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    assert humansorted(a) == natsorted(a, alg=ns.LOCALE)


def test_index_natsorted_returns_integer_list_of_sort_order_for_input_list():
    a = ['num3', 'num5', 'num2']
    b = ['foo', 'bar', 'baz']
    index = index_natsorted(a)
    assert index == [2, 0, 1]
    assert [a[i] for i in index] == ['num2', 'num3', 'num5']
    assert [b[i] for i in index] == ['baz', 'foo', 'bar']


def test_index_natsorted_returns_reversed_integer_list_of_sort_order_for_input_list_with_reverse_option():
    a = ['num3', 'num5', 'num2']
    assert index_natsorted(a, reverse=True) == [1, 0, 2]


def test_index_natsorted_applies_key_function_before_sorting():
    c = [('a', 'num3'), ('b', 'num5'), ('c', 'num2')]
    assert index_natsorted(c, key=itemgetter(1)) == [2, 0, 1]


def test_index_natsorted_handles_unorderable_types_error_on_Python3():
    a = [46, '5a5b2', 'af5', '5a5-4']
    assert index_natsorted(a) == [3, 1, 0, 2]


def test_index_natsorted_returns_integer_list_of_nested_input_list():
    data = [['a1', 'a5'], ['a1', 'a40'], ['a10', 'a1'], ['a2', 'a5']]
    assert index_natsorted(data) == [0, 1, 3, 2]


def test_index_natsorted_returns_integer_list_in_proper_order_for_input_paths_with_PATH():
    a = ['/p/Folder (10)/',
         '/p/Folder/',
         '/p/Folder (1)/']
    assert index_natsorted(a, alg=ns.PATH) == [1, 2, 0]


def test_index_versorted_returns_results_identical_to_index_natsorted():
    a = ['1.9.9a', '1.11', '1.9.9b', '1.11.4', '1.10.1']
    # index_versorted is retained for backwards compatibility
    assert index_versorted(a) == index_natsorted(a)


def test_index_realsorted_returns_results_identical_to_index_natsorted_with_REAL():
    a = ['a50', 'a51.', 'a50.31', 'a-50', 'a50.4', 'a5.034e1', 'a50.300']
    assert index_realsorted(a) == index_natsorted(a, alg=ns.REAL)


def test_index_humansorted_returns_results_identical_to_index_natsorted_with_LOCALE():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    assert index_humansorted(a) == index_natsorted(a, alg=ns.LOCALE)


def test_order_by_index_sorts_list_according_to_order_of_integer_list():
    a = ['num3', 'num5', 'num2']
    index = [2, 0, 1]
    assert order_by_index(a, index) == ['num2', 'num3', 'num5']
    assert order_by_index(a, index) == [a[i] for i in index]


def test_order_by_index_returns_generator_with_iter_True():
    a = ['num3', 'num5', 'num2']
    index = [2, 0, 1]
    assert order_by_index(a, index, True) != [a[i] for i in index]
    assert list(order_by_index(a, index, True)) == [a[i] for i in index]
