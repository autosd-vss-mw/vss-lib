# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

PYTHON_FILES := src/base_model.py src/config_loader.py src/vspec_parser.py src/vss_logging.py src/vendor_interface.py src/canbus.py
CYTHON_FILES := src/base_model.pyx src/config_loader.pyx src/vspec_parser.pyx src/vss_logging.pyx src/vendor_interface.pyx src/canbus.pyx

# Alias default target to python target
.PHONY: default
default: python

.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make                    - Alias for 'make python' to install the Python package"
	@echo "  make python             - Install the Python package using 'sudo pip install .'"
	@echo "  make python_uninstall   - Uninstall the Python package using 'sudo pip uninstall vss_lib'"
	@echo "  make cpython            - Convert Python files to Cython (.pyx), build C extensions"
	@echo "  make cpython_uninstall  - Remove Cython generated files and build artifacts"
	@echo "  make help               - Show this help message and explain each target"

.PHONY: python
python:
	@echo "Installing Python package..."
	sudo pip install .

.PHONY: python_uninstall
python_uninstall:
	@echo "Uninstalling Python package vss_lib..."
	sudo pip uninstall -y vss_lib

.PHONY: cpython
cpython: $(PYTHON_FILES)
	@echo "Converting Python files to Cython and building C extensions..."
	cp src/base_model.py src/base_model.pyx
	cp src/config_loader.py src/config_loader.pyx
	cp src/vspec_parser.py src/vspec_parser.pyx
	cp src/vss_logging.py src/vss_logging.pyx
	cp src/vendor_interface.py src/vendor_interface.pyx
	cp src/canbus.py src/canbus.pyx
	python setup_cpython.py build_ext --inplace

.PHONY: cpython_uninstall
cpython_uninstall:
	@echo "Removing Cython generated files and build artifacts..."
	rm -f $(CYTHON_FILES)
	rm -rf build
	rm -f *.so
