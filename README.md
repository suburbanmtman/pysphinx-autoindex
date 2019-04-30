# pysphinx-autoindex
Autogenerates sphinx index.rst automodule and autoclass directives for a project to help auto-generate documentation for all code automatically.

## Usage
`python pysphinx_autoindex/autoindexer.py <project root> <index_rst_location> [<module_prefix1>, ...]`

where
- *project_root* is the local file path to the base of your project (e.g. your github repo)
- *index_rst_location* is the local file path to the Sphinx `index.rst` file (e.g. `<your project>/docs/source/index.rst`)
- *module_prefix1..n* is a list of whitelisted module prefixes. By default all modules will be included.
