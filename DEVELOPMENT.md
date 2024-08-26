# Development

## Developing and Testing

Developing and Testing this collection may be done without building and installing
by cloning this repository inside following directory structure:

./collections/ansible_collections/rnx/updu/

```
mkdir -p ./collections/ansible_collections/rnx
cd ./collections/ansible_collections/rnx
git clone [repo url] updu
```

## Building

Building the collection may be done using following `ansible-galaxy` command:

```
ansible-galaxy collection build
```

## Deployment on Galaxy

On every new deployment, the version in the `galaxy.yml` file must be increased.
see [ansible doc on versioning](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_distributing.html#understanding-collection-versioning).


```
ansible-galaxy collection publish rnx-udpu-X.X.X.tar.gz --token <api-token>
```
