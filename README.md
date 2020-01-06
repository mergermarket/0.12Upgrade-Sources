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
&nbsp;
* Any `ignore_changes` in the lifecycle sections need to be a list of non quoted strings, ie.
 ```HCL 
      lifecycle {
         create_before_destroy = true
         ignore_changes        = [static_routes_only]
      }
 ```
&nbsp;
* Wrapping `concat` and `split` with square brackets is no longer required. ie,
```HCL
     route_table_ids = [concat(
        module.vpc.public_route_table_ids,
        module.vpc.private_route_table_ids,
     )]
  ```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  should be     
  ```HCL
       route_table_ids = concat(
          module.vpc.public_route_table_ids,
          module.vpc.private_route_table_ids,
       )
  ```  
&nbsp;
* How we use `count` can cause problems....  
&nbsp;
  NOTE making these changes will destroy and recrearte all of the resources created using the 'count'. It is much better to have the resources managed using the `for_each` due to the issues with the array in the state files         
&nbsp;
  *  In v0.12+ count needs to be a number, if your code tries to use a bollean to set count to either 1 or 0 it will fail. 
  Solution is to use the boolean to return a 1 or a zero, i.e.  
  ```HCL
     count = var.enabled ? 1 : 0
  ```
  * You used to be able to use count.index on a set (i.e. whats returned from data.aws_route_tables) 
  ```HCL
      data "aws_route_tables" "routetables" {
        provider = "aws.vpc"
        vpc_id   = "${data.aws_vpc.vpc.id}"
      }

      resource "aws_route" "tgw_routes" {
        count                  = "${length(data.aws_route_tables.routetables.ids)}"
        route_table_id         = "${data.aws_route_tables.routetables.ids[count.index]}"  
  ```  

  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;With Terrform 0.12 this is no longer possible but you can use the new `for_each`
  ```HCL
       data "aws_route_tables" "routetables" {
         provider = aws.vpc
         vpc_id   = data.aws_vpc.vpc.id
       }

       resource "aws_route" "tgw_routes" {
         for_each               = data.aws_route_tables.routetables.ids
         route_table_id         = each.value
      
