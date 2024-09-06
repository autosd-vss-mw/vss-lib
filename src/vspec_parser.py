# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from vspec.model import Model


def load_vspec_file(vspec_file):
    """
    Load a VSS file and return the model.

    Args:
        vspec_file (str): The path to the VSS file.

    Returns:
        Model: The VSS model loaded from the file.
    """
    return Model.from_file(vspec_file)


def get_signal(model, path):
    """
    Find and return a signal by its path.

    Args:
        model (Model): The VSS model.
        path (str): The signal path within the model.

    Returns:
        Signal: The signal object if found, else None.
    """
    return model.find(path)
