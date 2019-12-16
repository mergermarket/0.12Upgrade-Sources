# 0.12upgrade-sources

## Description
This docker image will upgrade the Terraform code in your application

All module sources will be migrated to the Terraform 0.12 version of the module

All the code in your application will be migrated to Terraform 0.12


## How to Use
Run from the top level directory of your application

   `docker container run --rm -v $(pwd):$(pwd) -w $(pwd) mergermarket/0.12upgrade-sources`
   
   `git add infra/version.tf`
   
Now you can commit and push the changes


## Limitations
Your Terraform files have to be in an `infra` directory
