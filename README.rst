===============================
Dark Souls Wiki Scrapper
===============================

A collection of scrappers to gather data from the Dark Souls wiki.

As these scrappers use CSS selectors tailored to each page, changes on those pages may break the parsers.

.. image:: https://img.shields.io/badge/docs-release-blue.svg
    :target: http://docs.bernardomg.com/darksouls-wiki-scrapper
    :alt: Dark Souls Wiki Scrapper latest documentation Status
.. image:: https://img.shields.io/badge/docs-develop-blue.svg
    :target: http://docs.bernardomg.com/development/darksouls-wiki-scrapper
    :alt: Dark Souls Wiki Scrapper development documentation Status

Features
--------

- Scrapper for the Dark Souls wiki

Documentation
-------------

Documentation sources are included with the project, and used to generate the
documentation sites:

- The `latest docs`_ are always generated for the latest release, kept in the 'master' branch
- The `development docs`_ are generated from the latest code in the 'develop' branch

The source files for the docs, a small `Sphinx`_ project, are kept in the 'docs folder.

These can be built if needed:

``python setup.py build_docs``

Prerequisites
~~~~~~~~~~~~~

Dependencies are indicated on the requirements.txt file.

These can be installed with:

``pip install --upgrade -r requirements.txt``

Usage
-----

The runner file takes care of executing the scrappers:

``python runner.py``

Testing
-------

The tests included with the project can be run with:

``python setup.py test``

This will delegate the execution to tox.

It is possible to run just one of the test profiles, in this case the py36 profile:

``python setup.py test -p "py3.8"``

Collaborate
-----------

Any kind of help with the project will be well received, and there are two main ways to give such help:

- Reporting errors and asking for extensions through the issues management
- or forking the repository and extending the project

Issues management
~~~~~~~~~~~~~~~~~

Issues are managed at the GitHub `project issues tracker`_, where any Github
user may report bugs or ask for new features.

Getting the code
~~~~~~~~~~~~~~~~

If you wish to fork or modify the code, visit the `GitHub project page`_, where
the latest versions are always kept. Check the 'master' branch for the latest
release, and the 'develop' for the current, and stable, development version.

License
-------

The project has been released under the `MIT License`_.

.. _GitHub project page: https://github.com/Bernardo-MG/darksouls-wiki-scrapper
.. _latest docs: http://docs.bernardomg.com/darksouls-wiki-scrapper
.. _development docs: http://docs.bernardomg.com/development/darksouls-wiki-scrapper
.. _MIT License: http://www.opensource.org/licenses/mit-license.php
.. _project issues tracker: https://github.com/Bernardo-MG/darksouls-wiki-scrapper/issues
.. _Sphinx: http://sphinx-doc.org/
