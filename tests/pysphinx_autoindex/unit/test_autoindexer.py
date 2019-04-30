# coding=utf-8
from os.path import abspath, join
from mock import Mock, patch, mock_open
import sys
import unittest

from pysphinx_autoindex.autoindexer import Autoindexer


class AutoindexerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.project_root = abspath(join(__file__, '..', '..', 'data', 'input', 'test-project'))
        cls.index_rst_dir = abspath(join(cls.project_root, 'docs'))
        cls.expected_dir = abspath(join(__file__, '..', '..', 'data', 'expected'))

    def test_init__requires_project_root(self):
        with self.assertRaises(ValueError):
            Autoindexer(
                project_root='/tmp/not_a_dir',
                index_rst_location=abspath(join(self.index_rst_dir, 'index_initial.rst'))
            )

    def test_init__requires_index_rst_location(self):
        with self.assertRaises(ValueError):
            Autoindexer(
                project_root=self.project_root,
                index_rst_location=abspath(join(self.index_rst_dir, 'index_does_not_exist.rst'))
            )

    def test_run(self):
        indexer = Autoindexer(
            project_root=self.project_root,
            index_rst_location=abspath(join(self.index_rst_dir, 'index_initial.rst'))
        )
        indexer._generate_docs_index = Mock()
        indexer._sphinx_formatter = Mock()
        indexer._traverse_modules = Mock()

        indexer.run()

        indexer._generate_docs_index.assert_called_once()
        indexer._sphinx_formatter.assert_called_once()
        indexer._traverse_modules.assert_called_once()

    def test_include_module__return_true_if_no_prefixes(self):
        indexer = Autoindexer(
            project_root=self.project_root,
            index_rst_location=abspath(join(self.index_rst_dir, 'index_initial.rst'))
        )

        self.assertTrue(indexer._include_module('any_mod'))

    def test_include_module__matching_prefix(self):
        indexer = Autoindexer(
            project_root=self.project_root,
            index_rst_location=abspath(join(self.index_rst_dir, 'index_initial.rst')),
            module_prefixes=['mymod_']
        )

        self.assertTrue(indexer._include_module('mymod_mod'))

    def test_include_module__exclude_non_prefix(self):
        indexer = Autoindexer(
            project_root=self.project_root,
            index_rst_location=abspath(join(self.index_rst_dir, 'index_initial.rst')),
            module_prefixes=['mymod_']
        )

        self.assertFalse(indexer._include_module('another_mod'))

    def test_traverse_modules(self):
        indexer = Autoindexer(
            project_root=self.project_root,
            index_rst_location=abspath(join(self.index_rst_dir, 'index_initial.rst')),
            module_prefixes=['test_mod']
        )
        sys.path.append(self.project_root)

        result = indexer._traverse_modules(self.project_root)

        self.assertDictEqual(
            {
                'test_mod_1': set(),
                'test_mod_1.test_class_1': {'TestClass1'},
                'test_mod_1.test_class_2': {'TestClass2'},
                'test_mod_1.test_submod_1': set(),
                'test_mod_1.test_submod_1.test_submodule_class': {'TestSubmoduleClass'},
                'test_mod_1.test_utils': set(),
                'test_mod_2': set()
            }, result
        )

    def test_generate_docs_index__initial_file(self):
        indexer = Autoindexer(
            project_root=self.project_root,
            index_rst_location=abspath(join(self.index_rst_dir, 'index_initial.rst')),
            module_prefixes=['test_mod']
        )
        indexer._write_index = Mock()
        sphinx_data = '''
.. automodule:: test_mod_1
    :members:

.. automodule:: test_mod_1.test_class_1
    :members:

.. autoclass:: TestClass1
    :members:

.. automodule:: test_mod_1.test_class_2
    :members:

.. autoclass:: TestClass2
    :members:

.. automodule:: test_mod_1.test_submod_1
    :members:

.. automodule:: test_mod_1.test_submod_1.test_submodule_class
    :members:

.. autoclass:: TestSubmoduleClass
    :members:
'''
        with open(abspath(join(self.expected_dir, 'index.rst')), 'r') as expected_file:
            expected_result = expected_file.read()

        indexer._generate_docs_index(sphinx_data)

        indexer._write_index.assert_called_once_with(expected_result)

    def test_generate_docs_index__existing_file(self):
        indexer = Autoindexer(
            project_root=self.project_root,
            index_rst_location=abspath(join(self.index_rst_dir, 'index_existing.rst')),
            module_prefixes=['test_mod']
        )
        indexer._write_index = Mock()
        sphinx_data = '''
.. automodule:: test_mod_1
    :members:

.. automodule:: test_mod_1.test_class_1
    :members:

.. autoclass:: TestClass1
    :members:

.. automodule:: test_mod_1.test_class_2
    :members:

.. autoclass:: TestClass2
    :members:

.. automodule:: test_mod_1.test_submod_1
    :members:

.. automodule:: test_mod_1.test_submod_1.test_submodule_class
    :members:

.. autoclass:: TestSubmoduleClass
    :members:
'''
        with open(abspath(join(self.expected_dir, 'index.rst')), 'r') as expected_file:
            expected_result = expected_file.read()

        indexer._generate_docs_index(sphinx_data)

        indexer._write_index.assert_called_once_with(expected_result)

    def test_sphinx_formatter(self):
        mod_dict = {
            'test_mod_1.test_class_1': {'TestHelper1', 'TestClass1'},
            'test_mod_1': set(),
            'test_mod_2.test_utils': set(),
            'test_mod_2': set()
        }
        indexer = Autoindexer(
            project_root=self.project_root,
            index_rst_location=abspath(join(self.index_rst_dir, 'index_existing.rst')),
            module_prefixes=['test_mod']
        )

        result = indexer._sphinx_formatter(mod_dict)

        self.assertEqual(
            '''
.. automodule:: test_mod_1
    :members: 

.. automodule:: test_mod_1.test_class_1
    :members: 

.. autoclass:: TestClass1
    :members: 

.. autoclass:: TestHelper1
    :members: 

.. automodule:: test_mod_2
    :members: 

.. automodule:: test_mod_2.test_utils
    :members: 
''',
            result
        )
