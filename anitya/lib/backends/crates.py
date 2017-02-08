# -*- coding: utf-8 -*-
# This file is a part of the Anitya project.
#
# Copyright © 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""
A backend for the Rust community’s crate host, `crates.io <https://crates.io/>`_.

Crates.io provides an API to determine a package's version, so this backend
makes use of that API rather than using regular expressions like some other
backends. The API is very simple. An HTTP GET request to
``https://crates.io/api/v1/crates/{name}/versions`` returns a JSON response
using the schema::

  {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "crates.io versions",
    "description": "https://crates.io/api/v1/crates/$name/versions",
    "type": "array",
    "definitions": {
      "version": {
        "type": "object",
        "properties": {
          "crate":      { "type": "string" },
          "created_at": { "type": "string", "format": "date-time" },
          "dl_path":    { "type": "string" },
          "downloads":  { "type": "integer" },
          "features": {
            "type": "object",
            # FIXME: 0+ elements
            # str: list(str)
          },
          "id":         { "type": "integer" },
          "links": {
            "type": "object",
            "properties": {
              "authors":           { "type": "string" },
              "dependencies":      { "type": "string" },
              "version_downloads": { "type": "string" }
            }
            "required": ["authors", "dependencies", "version_downloads"]
          },
          "num":        { "type": "string" },
          "updated_at": { "type": "string", "format": "date-time" },
          "yanked":     { "type": "boolean" },
        },
        "required": [
          "crate",
          "created_at",
          "dl_path",
          "downloads",
          "features",
          "id",
          "links",
          "num",
          "updated_at",
          "yanked"
        ]
      }
    },
    "items": {
      "anyOf": [
        { "$ref": "#/definitions/version" }
      ]
    }
  }

For example, ``https://crates.io/api/v1/crates/itoa/versions`` results in::

    {
        "versions": [
            {
                "crate": "itoa",
                "created_at": "2017-01-26T05:02:29Z",
                "dl_path": "/api/v1/crates/itoa/0.2.1/download",
                "downloads": 150,
                "features": {},
                "id": 43354,
                "links": {
                    "authors": "/api/v1/crates/itoa/0.2.1/authors",
                    "dependencies": "/api/v1/crates/itoa/0.2.1/dependencies",
                    "version_downloads": "/api/v1/crates/itoa/0.2.1/downloads"
                },
                "num": "0.2.1",
                "updated_at": "2017-01-26T05:02:29Z",
                "yanked": false
            }
    }
"""
import requests

from anitya.lib.backends import BaseBackend
from anitya.lib.exceptions import AnityaPluginException


class CratesBackend(BaseBackend):
    """The crates class for projects hosted on crates.io."""

    name = 'crates.io'
    examples = [
        'https://crates.io/crates/clap',
        'https://crates.io/crates/serde',
    ]

    @classmethod
    def _get_versions(cls, project):
        """
        Make a request for all versions of the project provided.

        Args:
            project (anitya.lib.model.Project): The Rust project to retrieve
                versions for.

        Returns:
            list: A list of version dictionaries. Each dictionary is in the format::
                {
                    "crate": "itoa",
                    "created_at": "2017-01-26T05:02:29Z",
                    "dl_path": "/api/v1/crates/itoa/0.2.1/download",
                    "downloads": 150,
                    "features": {},
                    "id": 43354,
                    "links": {
                        "authors": "/api/v1/crates/itoa/0.2.1/authors",
                        "dependencies": "/api/v1/crates/itoa/0.2.1/dependencies",
                        "version_downloads": "/api/v1/crates/itoa/0.2.1/downloads"
                    },
                    "num": "0.2.1",
                    "updated_at": "2017-01-26T05:02:29Z",
                    "yanked": false
                }

        Raises:
            AnityaPluginException: If the URL was unreachable or the response
                was in an unexpected format.
        """
        url = 'https://crates.io/api/v1/crates/{}/versions'.format(project.name)
        try:
            req = cls.call_url(url)
            req.raise_for_status()
            data = req.json()
        except requests.RequestException as e:
            raise AnityaPluginException('Could not contact {url}: '
                                        '{reason!r}'.format(url=url, reason=e))
        except ValueError as e:
            raise AnityaPluginException('Failed to decode JSON: {!r}'.format(e))

        return data['versions']

    @classmethod
    def get_version(cls, project):
        """
        Get the latest version of the project provided.

        Args:
            project (anitya.lib.model.Project): The Rust project to retrieve
                the latest version for.

        Returns:
            str: A version string.

        Raises:
            AnityaPluginException: If the URL was unreachable or the response
                was in an unexpected format.
        """
        return cls._get_versions(project)[0]['num']

    @classmethod
    def get_versions(cls, project):
        """
        Get all versions of the project provided.

        Args:
            project (anitya.lib.model.Project): The Rust project to retrieve
                versions for.

        Returns:
            list: A list of version strings.

        Raises:
            AnityaPluginException: If the URL was unreachable or the response
                was in an unexpected format.
        """
        return [v['num'] for v in cls._get_versions(project)]

    @classmethod
    def get_ordered_versions(cls, project):
        """
        Get all versions of the project provided, ordered from newest to oldest.

        Args:
            project (anitya.lib.model.Project): The Rust project to retrieve
                versions for.

        Returns:
            list: A list of version strings.

        Raises:
            AnityaPluginException: If the URL was unreachable or the response
                was in an unexpected format.
        """
        # crates API returns already ordered versions
        return cls.get_versions(project)