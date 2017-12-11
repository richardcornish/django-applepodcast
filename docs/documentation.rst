.. _documentation:

Documentation
*************

`Full documentation <https://django-applepodcast.readthedocs.io/>`_ is available online.

However, you can also build the documentation from source.

Clone the code repository.

.. code-block:: bash

   $ git clone git@github.com:richardcornish/django-applepodcast.git
   $ cd django-applepodcast/

Install `Sphinx <http://www.sphinx-doc.org/>`_, |sphinx-autobuild|_, and |sphinx_rtd_theme|_.

.. |sphinx-autobuild| replace:: ``sphinx-autobuild``
.. _sphinx-autobuild: https://pypi.python.org/pypi/sphinx-autobuild

.. |sphinx_rtd_theme| replace:: ``sphinx_rtd_theme``
.. _sphinx_rtd_theme: https://pypi.python.org/pypi/sphinx_rtd_theme

.. code-block:: bash

   $ pipenv install sphinx sphinx-autobuild sphinx_rtd_theme --three

Create an HTML build.

.. code-block:: bash

   $ (cd docs/ && make html)

Or use ``sphinx-autobuild`` to watch for live changes.

.. code-block:: bash

   $ sphinx-autobuild docs/ docs/_build_html

Open `127.0.0.1:8000 <http://127.0.0.1:8000>`_.
