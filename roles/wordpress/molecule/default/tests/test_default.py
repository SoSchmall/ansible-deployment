"""Role testing files using testinfra."""


# def test_hosts_file(host):
#     """Validate /etc/hosts file."""
#     f = host.file("/etc/hosts")

#     assert f.exists
#     assert f.user == "root"
#     assert f.group == "root"


def test_php_and_extensions_installed(host):
    packages = ["php-pear", "php-fpm", "php-dev", "php-zip", "php-curl", 
                "php-xmlrpc", "php-gd", "php-mysql", "php-mbstring", "php-xml"]
    for package in packages:
        assert host.package(package).is_installed

def test_nginx_installed(host):
    assert host.package("nginx").is_installed

def test_wordpress_directory(host):
    wp_dir = host.file("/var/www/demo.com")
    assert wp_dir.exists
    assert wp_dir.is_directory

def test_wordpress_installation(host):
    wp_index = host.file(f"/var/www/demo.com/index.php")
    assert wp_index.exists

def test_wordpress_directory_ownership(host):
    wp_dir = host.file("/var/www/demo.com")
    assert wp_dir.user == "www-data"
    assert wp_dir.group == "www-data"

def test_php_fpm_running(host):
    php_ver = host.run("dpkg -l | grep php-fpm | awk '{print $3}' | grep -o '[0-9]\\.[0-9]' | head -n 1").stdout.strip()
    php_fpm_service = host.service(f"php{php_ver}-fpm")
    assert php_fpm_service.is_running
    assert php_fpm_service.is_enabled

def test_nginx_running(host):
    nginx_service = host.service("nginx")
    assert nginx_service.is_running
    assert nginx_service.is_enabled

def test_nginx_vhost_configuration(host):
    nginx_vhost = host.file(f"/etc/nginx/sites-available/demo.com")
    assert nginx_vhost.exists

def test_default_nginx_config_removed(host):
    default_site_enabled = host.file("/etc/nginx/sites-enabled/default")
    default_site_available = host.file("/etc/nginx/sites-available/default")
    assert not default_site_enabled.exists
    assert not default_site_available.exists

def test_nginx_vhost_symlink(host):
    nginx_vhost_link = host.file(f"/etc/nginx/sites-enabled/demo.com")
    assert nginx_vhost_link.is_symlink
    assert nginx_vhost_link.linked_to == f"/etc/nginx/sites-available/demo.com"
