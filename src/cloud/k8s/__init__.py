"""
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import subprocess
import os


class KubernetesClusterManager:
    def __init__(self, cluster_name='kind-cluster', config_file='kind-config.yaml', kind_version='0.25.0', kubectl_version='v1.27.0'):
        self.cluster_name = cluster_name
        self.config_file = config_file
        self.kind_version = kind_version
        self.kubectl_version = kubectl_version
        self._check_tools_installed()

    def _check_tools_installed(self):
        """Check if kind, kubectl, or oc are installed on the system."""
        self._check_command('kind', install_instructions=f"""
You can install 'kind' by running the following commands:
  curl -Lo ./kind https://kind.sigs.k8s.io/dl/v{self.kind_version}/kind-$(uname)-amd64
  chmod +x ./kind
  sudo mv ./kind /usr/local/bin/kind
            """)

        # Check if either kubectl or oc exists
        kubectl_or_oc_found = any(self._check_command(cmd, suppress_output=True) for cmd in ['kubectl', 'oc'])
        if not kubectl_or_oc_found:
            print("Error: Neither 'kubectl' nor 'oc' is installed or found in the system's PATH.")
            print(f"You can install 'kubectl' by running the following commands (default version {self.kubectl_version}):")
            print(f"""
  curl -LO "https://dl.k8s.io/release/{self.kubectl_version}/bin/$(uname -s | tr '[:upper:]' '[:lower:]')/amd64/kubectl"
  chmod +x ./kubectl
  sudo mv ./kubectl /usr/local/bin/kubectl
            """)
            print("Alternatively, you can install 'oc' by following instructions at:")
            print("  https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest/")

            exit(1)

    def _check_command(self, cmd, install_instructions=None, suppress_output=False):
        """Check if a command is available on the system."""
        try:
            # Check if the command exists in the PATH
            subprocess.run(['which', cmd], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            if not suppress_output:
                print(f"Error: '{cmd}' is not installed or not found in the system's PATH.")
                if install_instructions:
                    print(install_instructions)
            return False

    def create_cluster(self):
        """Create a Kubernetes cluster using kind and the provided configuration file."""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Configuration file '{self.config_file}' not found.")

        try:
            subprocess.run(
                ['kind', 'create', 'cluster', '--name', self.cluster_name, '--config', self.config_file],
                check=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to create cluster: {e}")

    def list_nodes(self):
        """List all nodes in the Kubernetes cluster."""
        try:
            subprocess.run(['kubectl', 'get', 'nodes'], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to list nodes: {e}")

    def delete_cluster(self):
        """Delete the kind Kubernetes cluster."""
        try:
            subprocess.run(['kind', 'delete', 'cluster', '--name', self.cluster_name], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to delete the cluster: {e}")

    def apply_yaml(self, yaml_manifest, resource_type=None, resource_name=None, namespace=None):
        """
        Apply a YAML manifest using kubectl, checking if the resource already exists.
        If the resource exists, it prints a message and does not re-apply.

        Args:
            yaml_manifest (str): The YAML content to apply.
            resource_type (str, optional): The type of the resource (e.g., pod, namespace).
            resource_name (str, optional): The name of the resource.
            namespace (str, optional): The namespace of the resource (if applicable).
        """
        if resource_type and resource_name:
            # Check if the resource already exists
            cmd = ['kubectl', 'get', resource_type, resource_name]
            if namespace:
                cmd.extend(['-n', namespace])

            try:
                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return
            except subprocess.CalledProcessError:
                # Resource does not exist, proceed to apply the manifest
                pass

        # Apply the manifest
        try:
            subprocess.run(
                ['kubectl', 'apply', '-f', '-'],
                input=yaml_manifest.encode('utf-8'),
                check=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to apply the YAML manifest: {e}")

    def delete_resource(self, resource_type, resource_name):
        """Delete a resource in the Kubernetes cluster by type and name."""
        try:
            subprocess.run(['kubectl', 'delete', resource_type, resource_name], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to delete {resource_type} '{resource_name}': {e}")

    def apply_to_remote_clusters(self, clusters, manifest_file, kubeconfig_files):
        """
        Applies a given YAML manifest to multiple remote Kubernetes clusters.

        Parameters:
        - clusters (list of str): A list of cluster names to which the manifest should be applied.
        - manifest_file (str): The path to the YAML manifest file to be applied.
        - kubeconfig_files (list of str): A list of kubeconfig file paths for the remote clusters.

        Returns:
        - None
        """
        if len(clusters) != len(kubeconfig_files):
            raise RuntimeError(f"Number of clusters is different from kubeconfig files")

        for cluster, kubeconfig in zip(clusters, kubeconfig_files):
            try:
                # Switch context and apply the manifest using the specified kubeconfig
                apply_command = f"kubectl --kubeconfig={kubeconfig} apply -f {manifest_file}"
                subprocess.run(apply_command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Failed to apply the YAML manifest: {e}")
