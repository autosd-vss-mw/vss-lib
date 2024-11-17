# Vehicle Signal Specification (VSS) Middleware to create and manage Kubernetes cluster(s)

## Table of Contents
- [Overview](#overview)
- [Why?](#why)
- [Features](#features)
- [Requirements](#requirements)
- [Kubernetes](#kubernetes)
  - [Creating a Kubernetes cluster](#creating-a-kubernetes-cluster)
  - [Creating a pod](#creating-a-pod)
  - [Deleting a cluster](#deleting-a-cluster)

## Overview

The `KubernetesClusterManager` class is part of VSS Middleware to provide an easy-to-use interface for creating, managing, and interacting with Kubernetes clusters using `kind` (Kubernetes in Docker). It leverages the `kubectl` command-line tool to apply, update, and delete resources, making it simple to manage Pods, Namespaces, and other Kubernetes resources.

## Why?

The purpose of creating this resource in the Middleware is to enable seamless interaction and resource management within Kubernetes clusters (cloud vendors) directly from edge devices, such as vehicles, as more edge vendors are leveraging cloud connectivity to dynamically spawn and manage cloud-based resources from the edge.

## Features

- **Cluster Management**: Create and delete Kubernetes clusters using `kind`.
- **Resource Management**: Apply, update, and delete Kubernetes resources (e.g., Pods, Namespaces) using YAML manifests.
- **Resource Existence Handling**: Automatically check if resources exist before applying or creating them.
- **Customizable**: Supports applying user-defined YAML manifests for flexible resource management.
- **Built-in Error Handling**: Provides robust error handling using exceptions (`RuntimeError`, `FileNotFoundError`) for better reliability and debugging.

## Requirements

- Python 3.6+
- `kind` (Kubernetes in Docker)
- `kubectl` or `oc` (OpenShift CLI)

## Kubernetes

### Creating a kubernetes cluster

```bash
 ./create_cluster
enabling experimental podman provider
Creating cluster "test-cluster" ...
 ✓ Ensuring node image (kindest/node:v1.31.2) 🖼
 ✓ Preparing nodes 📦 📦 📦
 ✓ Writing configuration 📜
 ✓ Starting control-plane 🕹️
 ✓ Installing CNI 🔌
 ✓ Installing StorageClass 💾
 ✓ Joining worker nodes 🚜
Set kubectl context to "kind-test-cluster"
You can now use your cluster with:

kubectl cluster-info --context kind-test-cluster

Have a question, bug, or feature request? Let us know! https://kind.sigs.k8s.io/#community 🙂
Cluster 'test-cluster' created successfully.
Listing nodes in the cluster...
NAME                         STATUS     ROLES           AGE   VERSION
test-cluster-control-plane   NotReady   control-plane   15s   v1.31.2
test-cluster-worker          NotReady   <none>          2s    v1.31.2
test-cluster-worker2         NotReady   <none>          2s    v1.31.2
```

Code:
```bash
from vss_lib.cloud.k8s import KubernetesClusterManager

PATH_KIND_CONFIG="/usr/local/lib/python3.12/site-packages/vss_lib/cloud/k8s/kind-config.yaml"

if __name__ == "__main__":
    manager = KubernetesClusterManager(cluster_name='test-cluster', config_file=f"{PATH_KIND_CONFIG}")
    manager.create_cluster()
    manager.list_nodes()
```

### Creating a pod

```bash
$ ./create_example_pod
Creating custom namespace...
namespace/custom-namespace created
Creating custom pod in custom namespace...
pod/custom-pod created

$ kubectl get pods -n custom-namespace
NAME         READY   STATUS    RESTARTS   AGE
custom-pod   1/1     Running   0          20s
```

### Deleting a cluster
```bash
$ ./delete_cluster
enabling experimental podman provider
Deleting cluster "test-cluster" ...
Deleted nodes: ["test-cluster-worker2" "test-cluster-worker" "test-cluster-control-plane"]
```
