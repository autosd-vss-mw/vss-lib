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
# flake8: noqa: E501

import logging
import logging.config
import os
import sys


def setup_logging(default_path='/etc/vss-lib/logging.conf',
                  default_level=logging.INFO, env_key='VSS_LIB_LOG_CFG'):
    """
    Setup logging configuration.

    Args:
        default_path (str): Path to the default logging configuration file.
        default_level (int): Default logging level.
        env_key (str): Environment variable key to override the config file path.
    """
    path = os.getenv(env_key, default_path)
    if os.path.exists(path):
        try:
            logging.config.fileConfig(path, disable_existing_loggers=False)
            logging.getLogger(__name__).info(f'Loaded logging configuration from {path}')
        except Exception as e:
            print(f"Error loading logging configuration from {path}: {e}",
                  file=sys.stderr)
            logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(
            level=default_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
        logging.getLogger(__name__).warning(
            f'Logging configuration file not found at {path}. Using default settings.'
        )


# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)
