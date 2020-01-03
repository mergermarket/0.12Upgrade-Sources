# 0.12upgrade-sources

## Description
This docker image will upgrade the Terraform code in your application

All module sources will be migrated to the Terraform 0.12 version of the module

All the code in your application will be migrated to Terraform 0.12


## How to Use
Run from the top level directory of your application
```shell
docker container run --rm -v $(pwd):$(pwd) -w $(pwd) mergermarket/0.12upgrade-sources  
git add infra/versions.tf 
```   
Now you can commit and push the changes


## Limitations
Your Terraform files have to be in an `infra` directory


## Gotchas
* You will need to remove any fixed versions of AWS modules, ie. delete the version line in the example below  
```HCL
     source  = "terraform-aws-modules/vpc/aws"`
     version = "1.46.0"
```
* Any `ignore_changes` in the lifecycle sections need to be a list of non quoted strings, ie.
 ```HCL 
      lifecycle {
         create_before_destroy = true
         ignore_changes        = [static_routes_only]
      }
```
* Wrapping `concat` and `split` with square brackets is no longer required. ie,
```HCL
     route_table_ids = [concat(
        module.vpc.public_route_table_ids,
        module.vpc.private_route_table_ids,
     )]
  ```
  should be     
  ```HCL
     route_table_ids = concat(
        module.vpc.public_route_table_ids,
        module.vpc.private_route_table_ids,
     )
  ```
* Any module sources that are local to the module must begin with either ./ or ../.  With versions 0.11 you didn't need the dots and slashes. So   
`   source = "vpc_setup"`  
needs to be changed to  
`   source = "./vpc_setup"`
 
