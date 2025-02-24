# vim: ts=4:sw=4:expandtab

# BleachBit
# Copyright (C) 2008-2025 Andrew Ziem
# https://www.bleachbit.org
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
Test case for module Update
"""

import logging
import os

from tests import common
from bleachbit.Network import download_url_to_fn, get_gtk_version, get_ip_for_url, get_user_agent
import bleachbit.Network

logger = logging.getLogger(__name__)


class NetworkTestCase(common.BleachbitTestCase):
    """Test case for module Network"""

    def test_download_url_to_fn(self):
        """Unit test for function download_url_to_fn()"""
        # 200: no error
        # 404: not retryable error
        # 503: retryable error
        tests = (('http://httpstat.us/200', True),
                 ('http://httpstat.us/404', False),
                 ('http://httpstat.us/503', False))
        fn = os.path.join(self.tempdir, 'download')
        on_error_called = [False]

        def on_error(msg1, msg2):
            print('test on_error(%s, %s)' % (msg1, msg2))
            on_error_called[0] = True
        for test in tests:
            self.assertNotExists(fn)
            url = test[0]
            expected_rc = test[1]
            on_error_called = [False]
            rc = download_url_to_fn(
                url, fn, None, on_error=on_error, timeout=20)
            err_msg = 'test_download_url_to_fn({}) returned {} instead of {}'.format(
                url, rc, expected_rc)
            self.assertEqual(rc, expected_rc, err_msg)
            if expected_rc:
                self.assertExists(fn)
            self.assertNotEqual(rc, on_error_called[0])
            # minimal parameters
            rc = download_url_to_fn(url, fn)
            self.assertEqual(rc, expected_rc, err_msg)
            from bleachbit.FileUtilities import delete
            delete(fn, ignore_missing=True)

    def test_get_gtk_version(self):
        """Unit test for get_gtk_version()"""
        gtk_ver = get_gtk_version()
        self.assertIsInstance(gtk_ver, str)
        self.assertRegex(gtk_ver, r"^\d+\.\d+\.\d+$")

    def test_get_ip_for_url(self):
        """Unit test for get_ip_for_url()"""
        for good_url in ('https://www.example.com', bleachbit.update_check_url):
            ip_str = get_ip_for_url(good_url)
            import ipaddress
            ip = ipaddress.ip_address(ip_str)
        for bad_url in (None, '', 'https://test.invalid'):
            ret = get_ip_for_url(bad_url)
            self.assertEqual(
                ret[0], '(', 'get_ip_for_url({})={}'.format(bad_url, ret))

    def test_get_user_agent(self):
        """Unit test for method get_user_agent()"""
        agent = get_user_agent()
        logger.debug("user agent = '%s'", agent)
        self.assertIsString(agent)
