import unittest

from .discovery import discover_tests


class TestDiscoverTests(unittest.TestCase):
    longMessage = False

    def test_returns_one_valid_test_function_from_file(self):
        from test_data.discovery.one_valid_test import test_one

        path = "test_data/discovery/one_valid_test.py"
        actual = discover_tests(path)

        expected = [test_one]
        self.assertEqual(
            expected,
            actual,
            f"expected {expected} to be discovered from {path}, got {actual}",
        )

    def test_returns_multiple_valid_tests_from_file(self):
        from test_data.discovery.two_valid_tests import test_one, test_two

        path = "test_data/discovery/two_valid_tests.py"
        actual = discover_tests(path)

        expected = [test_one, test_two]
        self.assertEqual(
            expected,
            actual,
            f"expected {expected} to be discovered from {path}, got {actual}",
        )

    def test_returns_one_valid_test_class_from_file(self):
        from test_data.discovery.one_valid_class import TestOne

        path = "test_data/discovery/one_valid_class.py"
        actual = discover_tests(path)

        expected = [TestOne]
        self.assertEqual(
            expected,
            actual,
            f"expected {expected} to be discovered from {path}, got {actual}",
        )

    def test_returns_multiple_valid_test_classes_from_file(self):
        from test_data.discovery.two_valid_classes import TestOne, TestTwo

        path = "test_data/discovery/two_valid_classes.py"
        actual = discover_tests(path)

        expected = [TestOne, TestTwo]
        self.assertEqual(
            expected,
            actual,
            f"expected {expected} to be discovered from {path}, got {actual}",
        )

    def test_returns_test_functions_and_test_classes_from_file(self):
        from test_data.discovery.functions_and_classes import test_one, test_two, TestOne, TestTwo

        path = "test_data/discovery/functions_and_classes.py"
        actual = discover_tests(path)

        expected = [test_one, test_two, TestOne, TestTwo]
        self.assertEqual(
            expected,
            actual,
            f"expected {expected} to be discovered from {path}, got {actual}",
        )

    def test_returns_tests_in_definition_order(self):
        from test_data.discovery.unsorted_tests import test_a, test_b, TestA, TestB

        path = "test_data/discovery/unsorted_tests.py"
        actual = discover_tests(path)

        expected = [test_b, TestB, test_a, TestA]
        self.assertEqual(
            expected,
            actual,
            f"expected {expected} to be discovered from {path}, got {actual}",
        )

    def test_tests_defined_imported_from_other_modules_are_ignored(self):
        from test_data.discovery.imports_test_function import (
            test_defined_in_this_module,
            TestDefinedInThisModule,
        )

        path = "test_data/discovery/imports_test_function.py"
        actual = discover_tests(path)

        expected = [test_defined_in_this_module, TestDefinedInThisModule]
        self.assertEqual(
            expected,
            actual,
            f"expected {expected} to be discovered from {path}, got {actual}",
        )
