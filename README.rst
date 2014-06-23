=================
Mistral Dashboard
=================

Horizon plugin for Mistral.

Setup Instructions
==================

The following should get you started::

    $ sudo pip install -e /opt/stack/mistral-dashboard
    $ ln -s /opt/stack/mistral-dashboard/_50_mistral.py.example \
      /opt/stack/horizon/openstack_dashboard/local/enabled/_50_mistral.py

Since Mistral only supports Identity v3, you may need to edit the
``local_settings.py`` file to point to proper OPENSTACK_KEYSTONE_URL::

    OPENSTACK_API_VERSIONS = {
        "identity": 3,
    }

    OPENSTACK_KEYSTONE_URL = "http://%s:5000/v3" % OPENSTACK_HOST

Also, make sure you have changed OPENSTACK_HOST to point to your Keystone
server and check all endpoints are accessible. You may want to change
OPENSTACK_ENDPOINT_TYPE to "publicURL" if some of them are not.

Depending on your setup, you may also need to add a service and endpoints to
keystone::

    $ MISTRAL_URL="http://[host]:[port]/v1"
    $ keystone service-create --name mistral --type workflow
    $ keystone endpoint-create --service_id mistral --publicurl $MISTRAL_URL \
      --adminurl $MISTRAL_URL --internalurl $MISTRAL_URL

When you're ready, you would need to either restart your apache::

    $ sudo service apache2 restart

or run the development server (in case you have decided to use local horizon)::

    $ cd ../horizon/
    $ tox -evenv -- python manage.py runserver


