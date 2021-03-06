SugarCRM service settings
--------------------------

SugarCRM service settings have additional quotas:

- sugarcrm_user_count - total count of user limits that were connected to SPLs.


SugarCRM services list
----------------------

To get a list of services, run GET against **/api/sugarcrm/** as authenticated user.


Create a SugarCRM service
-------------------------

To create a new SugarCRM service, issue a POST with service details to **/api/sugacrm/** as a customer owner.

Request parameters:

 - name - service name,
 - customer - URL of service customer,
 - settings - URL of SugarCRM settings, if not defined - new settings will be created from server parameters,
 - dummy - is service dummy,

The following rules for generation of the service settings are used:

 - backend_url - URL of template group that describes OpenStack instance provision with default parameters
                 (required, e.g.: http://example.com/api/template-groups/16c7675752244f5d9e870a2cb0cfeb02/);
 - username - NodeConductor user username (e.g. User);
 - password - NodeConductor user password (e.g. Password);
 - license_code - License code that will be used for SugarCRM activation (required);
 - user_data - User data that will be passed to CRMs OpenStack instance on creation.
               Word {password} will be replaced with auto-generated admin password
               (default: "#cloud-config:\nruncmd:\n - [bootstrap, -p, {password}]");
 - protocol - CRMs access protocol. (default: "http");
 - phone_regex - RegEx for phone validation;
 - sms_email_from - Name of SMS email sender (SMS will not be send without this parameter);
 - sms_email_rcpt - Name of SMS email recipient (SMS will not be send without this parameter);


Example of a request:


.. code-block:: http

    POST /api/sugarcrm/ HTTP/1.1
    Content-Type: application/json
    Accept: application/json
    Authorization: Token c84d653b9ec92c6cbac41c706593e66f567a7fa4
    Host: example.com

    {
        "name": "My SugarCRM"
        "customer": "http://example.com/api/customers/2aadad6a4b764661add14dfdda26b373/",
        "backend_url": "http://example.com/api/template-groups/16c7675752244f5d9e870a2cb0cfeb02/",
        "username": "User",
        "password": "Password",
        "license_code": "some-code"
    }


Link service to a project
-------------------------
In order to be able to provision SugarCRM resources, it must first be linked to a project. To do that,
POST a connection between project and a service to **/api/sugarcrm-service-project-link/** as staff user or customer
owner.
For example,

.. code-block:: http

    POST /api/sugarcrm-service-project-link/ HTTP/1.1
    Content-Type: application/json
    Accept: application/json
    Authorization: Token c84d653b9ec92c6cbac41c706593e66f567a7fa4
    Host: example.com

    {
        "project": "http://example.com/api/projects/e5f973af2eb14d2d8c38d62bcbaccb33/",
        "service": "http://example.com/api/sugarcrm/b0e8a4cbd47c4f9ca01642b7ec033db4/"
    }

To remove a link, issue DELETE to url of the corresponding connection as staff user or customer owner.


Project-service connection list
-------------------------------
To get a list of connections between a project and an oracle service, run GET against
**/api/sugarcrm-service-project-link/** as authenticated user. Note that a user can only see connections of a project
where a user has a role.


Service-project-link quotas
---------------------------

 - user_limit_count - limitation for total number of users in all CRMs.
 - crm_count - CRMs count.


Create a new SugarCRM resource
------------------------------
A new SugarCRM instance can be created by users with project administrator role, customer owner role or with
staff privilege (is_staff=True). To create a CRM, client must issue POST request to **/api/sugarcrm-crms/** with
parameters:

 - name - CRM name;
 - description - CRM description (optional);
 - link to the service-project-link object;
 - user_count - maximal number of users in CRM (default: 10);


 Example of a valid request:

.. code-block:: http

    POST /api/sugarcrm-crms/ HTTP/1.1
    Content-Type: application/json
    Accept: application/json
    Authorization: Token c84d653b9ec92c6cbac41c706593e66f567a7fa4
    Host: example.com

    {
        "name": "test CRM",
        "description": "sample description",
        "service_project_link": "http://example.com/api/sugarcrm-service-project-link/1/",
        "size": 1024,
        "user_count": 20
    }

Updating a SugarCRM resource
----------------------------

SugarCRM can be update by issuing PUT request against **/api/sugarcrm-crms/<crm_uuid>/**.

Supported fields for update are **name** and **description**. Quota management for users is performed
through **/api/quotas/** endpoint by POSTing a new limit for the **user_count** quota with scope
of the SugarCRM instance.


SugarCRM resource display
-------------------------

To get SugarCRM resource data issue GET request against **/api/sugarcrm-crms/<crm_uuid>/**.
Field "instance_url" is visible only for staff.

Example rendering of the CRM object:

.. code-block:: javascript

    [
        {
            "url": "http://example.com/api/sugarcrm-crms/7693d9308e0641baa95720d0046e5696/",
            "uuid": "7693d9308e0641baa95720d0046e5696",
            "name": "test-sugarcrm",
            "description": "",
            "start_time": "2015-10-19T08:06:15Z",
            "service": "http://example.com/api/sugarcrm/655b79490b63442d9264d76ab9478f62/",
            "service_name": "sugarcrm service",
            "service_uuid": "655b79490b63442d9264d76ab9478f62",
            "project": "http://example.com/api/projects/0e86f04bb1fd48e181742d0598db69d5/",
            "project_name": "sugarcrm project",
            "project_uuid": "0e86f04bb1fd48e181742d0598db69d5",
            "customer": "http://example.com/api/customers/3b0fc2c0f0ed4f40b26126dc9cbd8f9f/",
            "customer_name": "sugarcrm customer",
            "customer_native_name": "",
            "customer_abbreviation": "",
            "project_groups": [],
            "resource_type": "SugarCRM.CRM",
            "state": "Provisioning",
            "created": "2015-10-20T10:35:19.146Z",
            "instance_url": "http://example.com/api/openstack-instances/42c35f288c524d52b86d945adde91db2/",
            "api_url": "http://example.com",
            "publishing_state": "not published",
            "quotas": [
                {
                    "url": "http://example.com/api/quotas/224c771110cc4340aa6a18f58861b307/",
                    "uuid": "224c771110cc4340aa6a18f58861b307",
                    "name": "user_count",
                    "limit": 10.0,
                    "usage": 0.0,
                }
            ]
        }
    ]

Delete CRM
----------

To delete CRM - issue DELETE request against **/api/sugarcrm-crms/<crm_uuid>/**.


List CRM users
--------------

To get list of all registered on CRM users - issue GET request against **/api/sugarcrm-crms/<crm_uuid>/users/**.
Only users with view access to CRM can view CRM users.

Supported filters:

 - ?user_name
 - ?first_name
 - ?last_name
 - ?status - the status can be Active, Inactive or Reserved.

Response example:

.. code-block:: javascript

    [
        {
            "url": "http://example.com/api/sugarcrm-crms/24156c367e3a41eea81e374073fa1060/users/a67a5b55-bb5f-1259-60a2-562e3c88fb34/",
            "uuid": "a67a5b55-bb5f-1259-60a2-562e3c88fb34",
            "user_name": "user",
            "status": "Active",
            "last_name": "User",
            "first_name": "",
            "email": "user@example.com"
        }
    ]


Create new CRM user
-------------------

To create new CRM user - issue POST request against **/api/sugarcrm-crms/<crm_uuid>/users/**.

Request parameters:

 - user_name - new user username;
 - last_name - new user last name;
 - first_name - new user first name (can be empty);
 - email - new user email (can be empty);
 - phone - new user mobile phone number (can be empty);
 - status - new user status (can be empty);


Example of a request:


.. code-block:: http

    POST /api/sugarcrm/24156c367e3a41eea81e374073fa1060/users/ HTTP/1.1
    Content-Type: application/json
    Accept: application/json
    Authorization: Token c84d653b9ec92c6cbac41c706593e66f567a7fa4
    Host: example.com

    {
        "user_name": "test_user",
        "last_name": "test user last name"
    }


Update a CRM user
-----------------

To update CRM user - issue PATCH request against **/api/sugarcrm-crms/<crm_uuid>/users/<user_id>/**.


Example of a request:


.. code-block:: http

    PUT /api/sugarcrm/24156c367e3a41eea81e374073fa1060/users/cc420109-a419-3d5b-558b-567168cf750f/ HTTP/1.1
    Content-Type: application/json
    Accept: application/json
    Authorization: Token c84d653b9ec92c6cbac41c706593e66f567a7fa4
    Host: example.com

    {
        "email": "test_user@example.com",
    }


Delete a CRM user
-----------------

To delete CRM user - issue DELETE request against **/api/sugarcrm-crms/<crm_uuid>/users/<user_id>/**.


Reset user password
-------------------

To reset user password - issue POST request against **/api/sugarcrm-crms/<crm_uuid>/users/<user_id>/password/**.
You can specify `notify` parameter in order to send user notification about newly created password.


Example of a valid request:

.. code-block:: http

    POST /api/sugarcrm-crms/db82a52368ba4957ac2cdb6a37d22dee/users/cc420109-a419-3d5b-558b-5671/password/ HTTP/1.1
    Content-Type: application/json
    Accept: application/json
    Authorization: Token c84d653b9ec92c6cbac41c706593e66f567a7fa4
    Host: example.com

    {
        "notify": "true"
    }

Example of response:

    {
        "password": "uONLv0UjcI"
    }
