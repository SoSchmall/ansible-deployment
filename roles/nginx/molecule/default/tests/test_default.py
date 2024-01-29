"""Role testing files using testinfra."""


# def test_hosts_file(host):
#     """Validate /etc/hosts file."""
#     f = host.file("/etc/hosts")

#     assert f.exists
#     assert f.user == "root"
#     assert f.group == "root"

def test_php_installed(host):
    """Check if PHP-FPM is installed."""
    php_fpm = host.package("php-fpm")
    assert php_fpm.is_installed

def test_nginx_installed(host):
    """Check if Nginx is installed."""
    nginx = host.package("nginx")
    assert nginx.is_installed

def test_nginx_running_and_enabled(host):
    """Ensure that Nginx is running and enabled."""
    nginx = host.service("nginx")
    assert nginx.is_running
    assert nginx.is_enabled

def test_nginx_wp_config_file_exists(host):
    """Check if the Nginx config file for WordPress exists."""
    nginx_conf = host.file(f"/etc/nginx/sites-available/demo.com")
    assert nginx_conf.exists
    assert nginx_conf.user == "root"
    assert nginx_conf.group == "root"

def test_nginx_default_config_removed(host):
    """Ensure the default Nginx configuration is removed."""
    default_site_enabled = host.file("/etc/nginx/sites-enabled/default")
    default_site_available = host.file("/etc/nginx/sites-available/default")
    assert not default_site_enabled.exists
    assert not default_site_available.exists

def test_nginx_vhost_symlink(host):
    """Check if Nginx WordPress virtual host symlink is correctly set."""
    nginx_vhost = host.file(f"/etc/nginx/sites-enabled/demo.com")
    assert nginx_vhost.is_symlink
    assert nginx_vhost.linked_to == f"/etc/nginx/sites-available/demo.com"

# Because of reverse proxy, still checks if port 80 is available, otherwise no nginx and no proxy will be achieved.
def test_http_port_open(host):
    """Verify that HTTP port 80 is open."""
    assert host.socket("tcp://0.0.0.0:80").is_listening
