Module Support
--------------

.. toctree:: :maxdepth: 1

Ansible has many modules, but not all of them are maintained by the core project commiters. Each module should have associated metadata that indicates which of the following categories they fall into. This should be visible in each module's documentation.

Documentation updates for each module can also be edited directly in the module and by submitting a pull request to the module source code; just look for the "DOCUMENTATION" block in the source tree.

If you believe you have found a bug in a module and are already running the latest stable or development version of Ansible, first look in the `issue tracker at github.com/ansible/ansible <http://github.com/ansible/ansible/issues>`_ to see if a bug has already been filed.  If not, we would be grateful if you would file one.

Should you have a question rather than a bug report, inquiries are welcome on the `ansible-project google group <https://groups.google.com/forum/#!forum/ansible-project>`_ or on Ansible's "#ansible" channel, located on irc.freenode.net.

For development-oriented topics, use the `ansible-devel google group <https://groups.google.com/forum/#!forum/ansible-devel>`_  or Ansible's "#ansible" and "#ansible-devel" channels, located on irc.freenode.net.  You should also read :doc:`community`, :doc:`dev_guide/developing_test_pr` and :doc:`dev_guide/developing_modules`.

The modules are hosted on GitHub in the in a subdirectory of the `ansible <https://github.com/ansible/ansible/tree/devel/lib/ansible/modules>`_ repo.

Core
````

These are modules that the core ansible team maintains and will always ship with ansible itself.
They will also receive slightly higher priority for all requests. Non-core modules are still fully usable.

Curated
```````

These modules are currently shipped with Ansible, but might be shipped separately in the future. They are mostly maintained by the community but core committers will oversee any changes or even take care of any issues that arise.

Community
`````````

These modules are currently shipped with Ansible, but might be shipped separately in the future. They are maintained by the community.
They are still fully usable, but the response rate to issues is purely up to the community.


.. seealso::

   :doc:`intro_adhoc`
       Examples of using modules in /usr/bin/ansible
   :doc:`playbooks`
       Examples of using modules with /usr/bin/ansible-playbook
   :doc:`dev_guide/developing_modules`
       How to write your own modules
   :doc:`dev_guide/developing_api`
       Examples of using modules with the Python API
   `Mailing List <http://groups.google.com/group/ansible-project>`_
       Questions? Help? Ideas?  Stop by the list on Google Groups
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel

