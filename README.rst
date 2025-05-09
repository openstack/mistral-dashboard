=================
Mistral Dashboard
=================

.. image:: https://governance.openstack.org/tc/badges/mistral-dashboard.svg

.. Change things from this point on

Horizon plugin for Mistral.

Setup Instructions
==================
This instruction assumes that Horizon is already installed and it's installation
folder is <horizon>. Detailed information on how to install Horizon can be
found at https://docs.openstack.org/horizon/latest/contributor/quickstart.html#setup.

The installation folder of Mistral Dashboard will be referred to as <mistral-dashboard>.

The following should get you started. Clone the repository into your local
OpenStack directory:

.. code:: console

    $ git clone https://opendev.org/openstack/mistral-dashboard.git

Install mistral-dashboard:

.. code:: console

    $ sudo pip install -e <mistral-dashboard>

Or if you're planning to run Horizon server in a virtual environment (see below):

.. code:: console

    $ tox -evenv -- pip install -e ../mistral-dashboard/

and then:

.. code:: console

    $ cp -b <mistral-dashboard>/mistraldashboard/enabled/_50_mistral.py <horizon>/openstack_dashboard/local/enabled/_50_mistral.py

Since Mistral only supports Identity v3, you must ensure that the dashboard
points the proper OPENSTACK_KEYSTONE_URL in <horizon>/openstack_dashboard/local/local_settings.py file::

    OPENSTACK_API_VERSIONS = {
        "identity": 3,
    }

    OPENSTACK_KEYSTONE_URL = "http://%s:5000/v3" % OPENSTACK_HOST

Also, make sure you have changed OPENSTACK_HOST to point to your Keystone
server and check all endpoints are accessible. You may want to change
OPENSTACK_ENDPOINT_TYPE to "publicURL" if some of them are not.

When you're ready, you would need to either restart your apache:

.. code:: console

    $ sudo service apache2 restart

or run the development server (in case you have decided to use local horizon):

.. code:: console

    $ cd ../horizon/
    $ tox -evenv -- python manage.py runserver

Mistral-Dashboard Debug Instructions
------------------------------------

For debug instructions refer to `OpenStack Mistral Debugging and Testing
<https://docs.openstack.org/mistral/latest/contributor/debugging_and_testing.html>`_
