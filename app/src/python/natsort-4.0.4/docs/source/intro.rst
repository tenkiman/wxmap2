.. default-domain:: py
.. module:: natsort

The :mod:`natsort` module
=========================

Natural sorting for python. 

    - Source Code: https://github.com/SethMMorton/natsort
    - Downloads: https://pypi.python.org/pypi/natsort
    - Documentation: http://pythonhosted.org/natsort/

:mod:`natsort` was initially created for sorting scientific output filenames that
contained floating point numbers in the names. There was a serious lack of
algorithms out there that could perform a natural sort on `floats` but
plenty for `ints`; check out
`this StackOverflow question <http://stackoverflow.com/q/4836710/1399279>`_
and its answers and links therein,
`this ActiveState forum <http://code.activestate.com/recipes/285264-natural-string-sorting/>`_,
and of course `this great article on natural sorting <http://blog.codinghorror.com/sorting-for-humans-natural-sort-order/>`_
from CodingHorror.com for examples of what I mean.
:mod:`natsort` was created to fill in this gap.  It has since grown
and can now sort version numbers (which seems to be the
most common use case based on user feedback) as well as some other nice features.

Quick Description
-----------------

When you try to sort a list of strings that contain numbers, the normal python
sort algorithm sorts lexicographically, so you might not get the results that you
expect::

    >>> a = ['a2', 'a9', 'a1', 'a4', 'a10']
    >>> sorted(a)
    ['a1', 'a10', 'a2', 'a4', 'a9']

Notice that it has the order ('1', '10', '2') - this is because the list is
being sorted in lexicographical order, which sorts numbers like you would
letters (i.e. 'b', 'ba', 'c').

:mod:`natsort` provides a function :func:`~natsorted` that helps sort lists
"naturally", either as real numbers (i.e. signed/unsigned floats or ints),
or as versions.  Using :func:`~natsorted` is simple::

    >>> from natsort import natsorted
    >>> a = ['a2', 'a9', 'a1', 'a4', 'a10']
    >>> natsorted(a)
    ['a1', 'a2', 'a4', 'a9', 'a10']

:func:`~natsorted` identifies numbers anywhere in a string and sorts them
naturally.

Sorting versions is handled properly by default (as of :mod:`natsort` version >= 4.0.0):

.. code-block:: python

    >>> a = ['version-1.9', 'version-2.0', 'version-1.11', 'version-1.10']
    >>> natsorted(a)
    ['version-1.9', 'version-1.10', 'version-1.11', 'version-2.0']

If you need to sort release candidates, please see :ref:`rc_sorting` for
a useful hack.

You can also perform locale-aware sorting (or "human sorting"), where the
non-numeric characters are ordered based on their meaning, not on their
ordinal value; this can be achieved with the :func:`~humansorted` function:

.. code-block:: python

    >>> a = ['Apple', 'Banana', 'apple', 'banana']
    >>> natsorted(a)
    ['Apple', 'Banana', 'apple', 'banana']
    >>> import locale
    >>> locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    'en_US.UTF-8'
    >>> from natsort import humansorted
    >>> humansorted(a)
    ['apple', 'Apple', 'banana', 'Banana']

You may find you need to explicitly set the locale to get this to work
(as shown in the example).
Please see :ref:`bug_note` and the Installation section 
below before using the :func:`~humansorted` function.

You can sort signed floats (i.e. real numbers) using the :func:`~realsorted`;
this is useful in scientific data analysis. This was the default behavior of
:func:`~natsorted` for :mod:`natsort` version < 4.0.0:

.. code-block:: python

    >>> from natsort import realsorted
    >>> a = ['num5.10', 'num-3', 'num5.3', 'num2']
    >>> natsorted(a)
    ['num2', 'num5.3', 'num5.10', 'num-3']
    >>> realsorted(a)
    ['num-3', 'num2', 'num5.10', 'num5.3']

You can mix and match ``int``, ``float``, and ``str`` (or ``unicode``) types
when you sort::

    >>> a = ['4.5', 6, 2.0, '5', 'a']
    >>> natsorted(a)
    [2.0, '4.5', '5', 6, 'a']
    >>> # On Python 2, sorted(a) would return [2.0, 6, '4.5', '5', 'a']
    >>> # On Python 3, sorted(a) would raise an "unorderable types" TypeError

:mod:`natsort` does not officially support the `bytes` type on Python 3, but
convenience functions are provided that help you decode to `str` first::

    >>> from natsort import as_utf8
    >>> a = [b'a', 14.0, 'b']
    >>> # On Python 2, natsorted(a) would would work as expected.
    >>> # On Python 3, natsorted(a) would raise a TypeError (bytes() < str())
    >>> natsorted(a, key=as_utf8) == [14.0, b'a', 'b']
    True
    >>> a = [b'a56', b'a5', b'a6', b'a40']
    >>> # On Python 2, natsorted(a) would would work as expected.
    >>> # On Python 3, natsorted(a) would return the same results as sorted(a)
    >>> natsorted(a, key=as_utf8) == [b'a5', b'a6', b'a40', b'a56']
    True

The natsort algorithm does other fancy things like 

 - recursively descend into lists of lists
 - control the case-sensitivity
 - sort file paths correctly
 - allow custom sorting keys
 - exposes a natsort_key generator to pass to list.sort

Please see the :ref:`examples` for a quick start guide, or the :ref:`api`
for more details.

Installation
------------

Installation of :mod:`natsort` is ultra-easy.  Simply execute from the
command line::

    easy_install natsort

or, if you have ``pip`` (preferred over ``easy_install``)::

    pip install natsort

Both of the above commands will download the source for you.

You can also download the source from http://pypi.python.org/pypi/natsort,
or browse the git repository at https://github.com/SethMMorton/natsort.

If you choose to install from source, you can unzip the source archive and
enter the directory, and type::

    python setup.py install

If you wish to run the unit tests, enter::

    python setup.py test

If you want to build this documentation, enter::

    python setup.py build_sphinx

:mod:`natsort` requires Python version 2.7 or greater or Python 3.2 or greater.

The most efficient sorting can occur if you install the 
`fastnumbers <https://pypi.python.org/pypi/fastnumbers>`_ package (it helps
with the string to number conversions.)  ``natsort`` will still run (efficiently)
without the package, but if you need to squeeze out that extra juice it is
recommended you include this as a dependency.  ``natsort`` will not require (or
check) that `fastnumbers <https://pypi.python.org/pypi/fastnumbers>`_ is installed.

On BSD-based systems (this includes Mac OS X), the underlying ``locale`` library
can be buggy (please see http://bugs.python.org/issue23195); ``locale`` is
used for the ``ns.LOCALE`` option and ``humansorted`` function.. To remedy this,
one can 

    1. Use "\*.ISO8859-1" locale (i.e. 'en_US.ISO8859-1') rather than "\*.UTF-8"
       locale. These locales do not suffer from as many problems as "UTF-8"
       and thus should give expected results.
    2. Use `PyICU <https://pypi.python.org/pypi/PyICU>`_.  If
       `PyICU <https://pypi.python.org/pypi/PyICU>`_ is installed, ``natsort``
       will use it under the hood; this will give more
       reliable cross-platform results in the long run. ``natsort`` will not
       require (or check) that `PyICU <https://pypi.python.org/pypi/PyICU>`_
       is installed at installation. Please visit
       https://github.com/SethMMorton/natsort/issues/21 for more details and
       how to install on Mac OS X. **Please note** that using
       `PyICU <https://pypi.python.org/pypi/PyICU>`_ is the only way to
       guarantee correct results for all input on BSD-based systems, since
       every other suggestion is a workaround.
    3. Do nothing. As of ``natsort`` version 4.0.0, ``natsort`` is configured
       to compensate for a broken ``locale`` library in terms of case-handling;
       if you do not need to be able to properly handle non-ASCII characters
       then this may be the best option for you. 

Note that the above solutions *should not* be required for Windows or
Linux since in Linux-based systems and Windows systems ``locale`` *should* work
just fine.

:mod:`natsort` comes with a shell script called :mod:`natsort`, or can also be called
from the command line with ``python -m natsort``.  The command line script is
only installed onto your ``PATH`` if you don't install via a wheel.  There is
apparently a known bug with the wheel installation process that will not create
entry points.
