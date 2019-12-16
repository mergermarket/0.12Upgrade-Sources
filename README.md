# 0.12Upgrade-Sources

## Description
This docker image will upgrade the Terraform code in your application

All module sources will be migrated to the Terraform 0.12 version of the module

All the code in your application will be migrated to Terraform 0.12


## How to Use
Run from the top level directory of your application

   `docker container run --rm -v $(pwd):$(pwd) -w $(pwd) mergermarket/0.12Upgrade-Sources`


## Limitations
This only works on `tf` files in the `infra` directory 
