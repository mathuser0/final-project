#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `final_project` package."""

from unittest import TestCase
import final_project
from final_project import cli, __main__ as final_project_main
import re


class Testpset_x(TestCase):
    """Tests for `pset_x` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def is_version(self,v):
        if isinstance(v, str):
            return bool(re.match(r'^\d+.\d+.', v))
        else:
            return False

    def test_pset_version(self):
        """Check that version of Pset can be obtained"""
        assert self.is_version(final_project.__version__)

    def test_cli(self):
        """Check that scaffold of main function in cli.py can be run and returns 0"""
        self.assertEqual(cli.main(),0)

    def test_main(self):
        """Check that main function in __main__.py can be run and returns 0"""
        final_project_main.main()

# the following code works fine if it is rendered with cookiecutter,
# however pytest-cookies gets completely screwed by the jinja2 code:

# 
#     def test_csci_utils(self):
#         """Check that csci_utils can be imported and version can be obtained"""
#         import csci_utils
#         assert self.is_version(csci_utils.__version__)
# 
