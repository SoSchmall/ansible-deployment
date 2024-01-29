############### Requirements ###############

This project is running the following packages version:

python version = 3.8.10 (default, Nov 22 2023, 10:22:35) [GCC 9.4.0]
jinja version = 3.1.3

molecule 4.0.4 using python 3.8 
ansible:2.12.10
delegated:4.0.4 from molecule
docker:2.1.0 from molecule_docker requiring collections: community.docker>=3.0.2 ansible.posix>=1.4.0

############### Introduction ###############

The project is running wordpress in a distributed environment using reverse proxy. Ansible is running on a master host to configure its clients:
    -Client1: Nginx behaving as a proxy redirecting to the backend of wordpress
    -Client2: Wordpress
    -Client3: MySQL

############### Configuration ###############

Client1 redirects its requests to Client2, which tries to connect to its remote database on Client3.

MySQL must allow external connection (bind-address) and must make sure that external hosts are allowed to access wordpress database (not just database permission but also hosts permission which in this case datascientest% --every datascientest host--, which is insecure). Either, the range of ip addresses can be used or a specific one. Note that, in this case, 0.0.0.0 is attributed to bind-address rather than wordpress ip address. This is easier for test purposes. Indeed, wordpress database has the least privileges to run perfectly: SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER,INDEX.

Files in group_vars are encrypted using ansible-vault. To decrypt them, use the command ansible-vault decrypt "file-name", with password qwerty


