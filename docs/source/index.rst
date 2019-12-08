|project|
=========

Installation
------------

.. code:: sh

   pip install vws-test-fixtures

This is tested on Python 3.8+.

Example usage
-------------

.. code:: python

   import requests
   from vws_test_fixtures import authorization_header, rfc_1123_date

   target_id = '...'
   request_path = f'/duplicates/{target_id}'
   content = b''
   method = 'GET'
   date = rfc_1123_date()
   authorization_header = authorization_header(
       access_key='my_access_key',
       secret_key='my_secret_key',
       method=method,
       content=content,
       content_type='',
       date=date,
       request_path=request_path,
   )

   headers = {'Authorization': authorization_string, 'Date': date}

   response = requests.request(
        method=method,
        url=urljoin(base='https://vws.vuforia.com', url=request_path),
        headers=headers,
        data=content,
    )

    assert response.status_code == 200

Reference
---------

.. toctree::
   :maxdepth: 3

   api-reference
   contributing
   release-process
   changelog

