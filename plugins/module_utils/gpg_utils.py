#!/usr/bin/python3
# coding: utf-8

# (c) 2021, Famedly GmbH
# GNU Affero General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/agpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

# Check if all required libs can loaded
import os.path
from pathlib import Path
from typing import Union

import gnupg
import json
import yaml


class GPGException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class PasswordStoreException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class PasswordDecodeError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class TrustLevel:
    UNKNOWN = "o"
    INVALID = "i"
    DISABLED = "d"
    REVOKED = "r"
    EXPIRED = "e"
    UNKNOWN_VALIDITY = "-"
    UNDEFINED_VALIDITY = "q"
    NOT_VALID = "n"
    MARGINAL = "m"
    FULLY = "f"
    ULTIMATELY = "u"
    WELL_KNOWN_PRIVATE = "w"
    SPECIAL = "s"
    SIGNATURE_GOOD = "!"
    SIGNATURE_BAD = "-"
    NO_PUBKEY = "?"
    SIGNATURE_ERROR = "%"


class SecretStore:
    SUPPORTED_TYPES = ["plain", "json", "yaml"]
    ENCODING = "UTF-8"
    RECIPIENT_METHODS = ["keyring", "pass_file", "list"]

    def __init__(
        self,
        password_store_path: str = "~/.password-store/",
        file_extension: str = ".gpg",
        keyring: str = "pubring.kbx",
        gnupg_home: str = "~/.gnupg",
        pass_gpg_id_file: str = ".gpg-id",
    ):
        self.password_store_path = Path(password_store_path)
        self.file_extension = file_extension
        self.pass_gpg_id_file = pass_gpg_id_file

        # Create gpg object
        self.__gpg = gnupg.GPG(
            gnupghome=Path(gnupg_home).expanduser().absolute().as_posix(),
            keyring=keyring,
        )
        self.gpg = self.__gpg

    def __load(self, slug: str) -> str:
        file = (
            (self.password_store_path / (slug + self.file_extension))
            .expanduser()
            .absolute()
            .as_posix()
        )
        try:
            with open(file, "rb") as f:
                result = self.__gpg.decrypt_file(f)
                if result.ok:
                    return result.data.decode(self.ENCODING)
                else:
                    raise GPGException(result.status)
        except FileNotFoundError:
            raise FileNotFoundError

    def __save(self, slug: str, data: str, recipients: list[str]) -> bool:
        file = Path(
            (self.password_store_path / (slug + self.file_extension))
            .expanduser()
            .absolute()
            .as_posix()
        )
        Path.mkdir(file.parent, parents=True, exist_ok=True)
        result = self.__gpg.encrypt(data.encode(self.ENCODING), recipients)
        if result.ok:
            with open(file, "wb") as f:
                f.write(result.data)
            return True
        else:
            raise GPGException(result.status)

    def get(self, slug: str, data_type: str = "plain") -> Union[str, dict, list]:
        data_type = data_type.lower()

        if data_type not in self.SUPPORTED_TYPES:
            raise NotImplementedError("Datatype %s is not supported".format(data_type))

        raw = self.__load(slug)
        try:
            if data_type == "plain":
                return raw
            if data_type == "json":
                return json.loads(raw)
            if data_type == "yaml":
                return yaml.safe_load(raw)
        except (json.decoder.JSONDecodeError, yaml.YAMLError) as e:
            raise PasswordDecodeError

    def __get_recipients_from_keyring(self) -> list[str]:
        recipients = []
        for key in self.__gpg.list_keys():
            if key["trust"] in [
                TrustLevel.FULLY,
                TrustLevel.MARGINAL,
                TrustLevel.ULTIMATELY,
            ]:
                recipients.append(key["fingerprint"])
        return recipients

    def __get_recipients_from_pass_file(self, password_slug: str) -> list[str]:
        base_path = self.password_store_path.expanduser().absolute() / password_slug
        while base_path.as_posix() != "/":
            if os.path.isfile(base_path / self.pass_gpg_id_file):
                break
            base_path = base_path.parent
        else:
            raise FileNotFoundError(
                "Could not find {} in tree".format(self.pass_gpg_id_file)
            )
        with open(base_path / self.pass_gpg_id_file) as f:
            return f.read().splitlines()

    def put(
        self,
        slug: str,
        data: Union[str, dict, list],
        data_type: str = None,
        recipient_method: str = "pass_file",
        recipients_list: list[str] = None,
    ):
        if not isinstance(data, str) and data_type is None:
            data_type = "yaml"
        elif isinstance(data, str) and data_type is None:
            data_type = "plain"

        if data_type not in self.SUPPORTED_TYPES:
            raise NotImplementedError("Datatype {} is not supported".format(data_type))

        if data_type == "plain":
            result = data
        if data_type == "json":
            result = json.dumps(data, indent=4)
        if data_type == "yaml":
            result = yaml.safe_dump(data)

        if isinstance(recipients_list, list):
            recipient_method = "list"
        if recipient_method not in self.RECIPIENT_METHODS:
            raise NotImplementedError(
                "Recipient method {} is not supported".format(recipient_method)
            )
        if recipient_method == "keyring":
            recipients = self.__get_recipients_from_keyring()
        if recipient_method == "pass_file":
            recipients = self.__get_recipients_from_pass_file(slug)
        if recipient_method == "list":
            recipients = recipients_list
        if len(recipients) == 0:
            raise PasswordStoreException("Empty recipient  list")
        self.__save(slug, result, recipients)
