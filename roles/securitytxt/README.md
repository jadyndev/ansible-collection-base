# `famedly.base.securitytxt`

Template a security.txt file (see [RFC 9116](https://www.rfc-editor.org/rfc/rfc9116)) and serves it using nginx.

## Role variables

- `securitytxt_expires`: mandatory, containing a timestamp, formatted as `%Y-%m-%d %H:%M:%S` when the file expires. Is treated as UTC.
- `securitytxt_contacts`: mandatory, list of at least one string that contains URIs for how to contact the organisation
- `securitytxt_preferred_languages`: optional, list of language tags
- `securitytxt_acknowledgements`: optional, url where acknowledgements are published
- `securitytxt_canonical`: optional, list of url where this file is expected to be served
- `securitytxt_encryption`: optional, url where a PGP key can be obtained
- `securitytxt_hiring`: optional, url where open security positions are published
- `securitytxt_policy`: optional, url where the security policy is published

## License

AGPL-3.0-only

## Author Information

- Jan Christian Grünhage <jan.christian@gruenhage.xyz>
