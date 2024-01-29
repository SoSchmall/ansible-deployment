"""Role testing files using testinfra."""


# def test_hosts_file(host):
#     """Validate /etc/hosts file."""
#     f = host.file("/etc/hosts")

#     assert f.exists
#     assert f.user == "root"
#     assert f.group == "root"

# check for either mysql-server or mariadb-server
def test_mysql_installed(host):
    mysql_package = 'mysql-server'
    if host.system_info.distribution == 'debian':
        mysql_package = 'mariadb-server'
    assert host.package(mysql_package).is_installed

# check if mysql is already enabled and running
def test_mysql_running_and_enabled(host):
    mysql_service = host.service("mysql")
    assert mysql_service.is_running
    assert mysql_service.is_enabled

def test_required_packages_installed(host):
    packages = ["php-mysql", "python3-pymysql"]
    for package in packages:
        assert host.package(package).is_installed

# wordpress sql database creation
def test_mysql_db_exists(host):
    db_name = "wordpress"
    cmd = host.run("mysql -e 'SHOW DATABASES;'")
    assert db_name in cmd.stdout

# check for the existence of datascientest user 
def test_mysql_user_exists(host):
    user_name = "datascientest"
    cmd = host.run(f"mysql -e 'SELECT User FROM mysql.user WHERE User = \"{user_name}\";'")
    assert user_name in cmd.stdout

# sql config allowing external connection
def test_mysql_listening_on_all_interfaces(host):
    config_file = "/etc/mysql/mysql.conf.d/mysqld.cnf"
    assert host.file(config_file).contains("bind-address = 0.0.0.0")

