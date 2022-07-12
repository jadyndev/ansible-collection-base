#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) 2021-2022, Famedly GmbH
# GNU Affero General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/agpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: gpg_secretstore
    author:
      - Jadyn Emma Jäger (@jadyndev)
      - Jan Christian Grünhage (@jcgruenhage)
    short_description: read passwords that are compatible with passwordstore.org's pass utility
    description:
      - Enables Ansible to read passwords/secrets from the passwordstore.org pass utility.
        It's also able to read yaml/json files if needed
    options:
      _terms:
        description: query key.
        required: True
      data-type:
        description: If the decrypted data should be interpreted as yaml, json or plain text.
        default: 'plain'
        options:
            - yaml
            - json
            - plain
"""
EXAMPLES = """
# Debug is used for examples, BAD IDEA to show passwords on screen
- name: lookup password without type
  debug:
    var: mypassword
  vars:
    mypassword: "{{ lookup('famedly.local.gpg_secretstore', 'example/plain')}}"

- name: lookup password with type plain
  debug:
    var: mypassword
  vars:
    mypassword: "{{ lookup('famedly.local.gpg_secretstore', 'example/plain', 'plain')}}"

- name: lookup password with type yaml
  debug:
    var: mypassword
  vars:
    mypassword: "{{ lookup('famedly.local.gpg_secretstore', 'example/yaml', 'yaml')}}"

- name: lookup password with type json
  debug:
    var: mypassword
  vars:
    mypassword: "{{ lookup('famedly.local.gpg_secretstore', 'example/json', 'json')}}"
"""

RETURN = """
_raw:
  description:
    - a password
  type: list
  elements: str
"""

from ansible.plugins.lookup import LookupBase
from ansible.module_utils.six import raise_from
from ansible.module_utils.basic import missing_required_lib
from ansible.errors import AnsibleError
from ansible_collections.famedly.base.plugins.module_utils.gpg_utils import (
    SecretStore,
    check_secretstore_import_errors,
)


class LookupModule(LookupBase):
    def run(self, terms: dict, variables, **kwargs):
        errors = []
        traceback = []
        for lib, exception in check_secretstore_import_errors().items():
            errors.append(missing_required_lib(lib))
            traceback.append(exception)
        if errors:
            raise_from(
                AnsibleError("\n".join(errors)),
                "\n".join(traceback),
            )
        if len(terms) == 1:
            data_type = "plain"
        else:
            data_type = terms[1]
        password_store = SecretStore()
        result = password_store.get(terms[0], data_type)
        return [result]
