=================
Mistral Dashboard
=================

Horizon plugin for Mistral.

Setup Instructions
==================
This instruction assumes that Horizon is already installed and it's installation
folder is <horizon>. Detailed information on how to install Horizon can be
found at http://docs.openstack.org/developer/horizon/quickstart.html#setup.

The installation folder of Mistral Dashboard will be referred to as <mistral-dashboard>.

The following should get you started::

Clone the repository into your local OpenStack directory:

    $ git clone https://github.com/openstack/mistral-dashboard.git

Install mistral-dashboard

    $ sudo pip install -e <mistral-dashboard>

Or if you're planning to run Horizon server in a virtual environment (see below):

    $ tox -evenv -- pip install -e ../mistral-dashboard/

and then

    $ ln -s <mistral-dashboard>/_50_mistral.py.example \
      <horizon>/openstack_dashboard/local/enabled/_50_mistral.py

Since Mistral only supports Identity v3, you must ensure that the dashboard
points the proper OPENSTACK_KEYSTONE_URL in <horizon>/openstack_dashboard/local/local_settings.py file::

    OPENSTACK_API_VERSIONS = {
        "identity": 3,
    }

    OPENSTACK_KEYSTONE_URL = "http://%s:5000/v3" % OPENSTACK_HOST

Also, make sure you have changed OPENSTACK_HOST to point to your Keystone
server and check all endpoints are accessible. You may want to change
OPENSTACK_ENDPOINT_TYPE to "publicURL" if some of them are not.

When you're ready, you would need to either restart your apache::

    $ sudo service apache2 restart

or run the development server (in case you have decided to use local horizon)::

    $ cd ../horizon/
    $ tox -evenv -- python manage.py runserver

Debug Instructions
==================
**Pycharm**

Set PyCharm debug settings:

  1. Enter debug configurations menu
  2. Create a new Django Server configuration
  3. Enter some port so it won't run on the default (for example - port: 4000)
  4. On the same window click on Environment variables
     a. Make sure you have PYTHONUNBUFFERED set as 1
     b. Create a new pair - DJANGO_SETTINGS_MODULE : openstack_dashboard.settings

You should now be able to debug and run the project using PyCharm.