import os
import re
import requests
import tempfile
import shutil
from python_terraform import *


def get_registry_module(module_name):
    resp = requests.get(f"https://registry.terraform.io/v1/modules/mergermarket/{module_name}")
    if resp.status_code != 200:
        print('GET /tasks/ {}'.format(resp.status_code))
        raise Exception("Api Error")
    if len(resp.json()['modules']) > 1:
        print(f"{len(resp.json()['modules'])} modules returned - should be only 1")
        raise Exception('Search failed')
    for module in resp.json()['modules']:
        module_name = re.split('acuris/', module['id'])[0] + "acuris"
        module_version = re.split('acuris/', module['id'])[-1]
        return module_name, module_version


def convert_module_name(line):
    module_name = re.split(r"github.com/mergermarket/tf_", line)[-1]
    no_quotes = module_name.replace('"', '')
    change_underscores = no_quotes.replace('_', '-')
    no_cr = change_underscores.rstrip()
    no_refs = no_cr.replace('?ref=', '-')
    return no_refs


def scan_file(file_name):
    tf_file = open(file_name,'r')
    temp = tempfile.NamedTemporaryFile(delete=False, mode ='w+t') 
    line_list = tf_file.readlines()
    new_lines = []
    
    for line in line_list:
        if re.match(r".*source.*=.*github.com/mergermarket/tf_.*", line):
            name, version = get_registry_module(convert_module_name(line))
            print(f"{name}:{version}")
            new_lines.append(f'source = "{name}"\n')
            new_lines.append(f'version = "{version}"\n')
        elif re.match(
            r".*\ssource\s=.*", line) and not re.match(
            r".*mergermarket.*", line) and not bool(re.match(
            r'.*source\s=\s"\.\/.*', line)):
            new_lines.append(re.sub(r'source\s=\s"', 'source = "./', line))    
        else:
            new_lines.append(line)    
    temp.writelines(new_lines)

    tf_file.close() 
    temp.close()
    shutil.copy(temp.name, file_name)


def main():
    for root, _, files in os.walk("./infra"):
        for file in files:
            if file.endswith(".tf"):
                scan_file(os.path.join(root, file))
    
    t = Terraform(working_dir='./infra')
    t.cmd('version', capture_output=False)
    t.cmd('fmt', capture_output=False)
    t.cmd('init', capture_output=False)
    t.cmd('0.12upgrade', '-yes', capture_output=False)

main()