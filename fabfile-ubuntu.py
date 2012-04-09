from cuisine import (user_ensure, dir_ensure, user_passwd, package_ensure,
    run, package_update_apt, package_update, dir_exists, file_link, file_exists, repository_ensure_apt)
from fabric.context_managers import cd
from fabric.decorators import hosts
from fabric.state import env
from fabric.utils import warn

HOSTS=['108.171.175.201']

ROOT_USER='root'
ROOT_PASS='john-testU2nq0FLn5'

RTD_USER='rtd_user'
RTD_PASS='rtd_pass_123'

RTD_CLONE='git://github.com/johncosta/readthedocs.org.git'
RTD_CLONE_NAME="readthedocs.org"
RTD_INITIAL_VERSION='v0.1'

CREATE_DB_SQL = """CREATE DATABASE IF NOT EXISTS %(db_name)s DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;"""
CREATE_USER_SQL = """CREATE USER %(db_user)s@localhost IDENTIFIED BY '%(db_password)s';"""
DELETE_USER_SQL = """DROP USER %(db_user)s@localhost;"""
GRANT_PERMISSIONS_SQL = """
    GRANT ALL ON %(db_name)s.* TO '%(db_user)s'@'localhost';
    FLUSH PRIVILEGES;
    """

@hosts(HOSTS)
def stage_rtd():
    user_setup()
    package_setup()
    configure_database()
    project_layout()
    make_virtualenv()
    bootstrap_virtualenv()
    link_django_settings()


@hosts(HOSTS)
def user_setup():
    """ Creates a read the docs user """
    env.user=ROOT_USER
    env.password=ROOT_PASS

    user_ensure(RTD_USER, home='/opt/rtd')
    user_passwd(RTD_USER, RTD_PASS )

@hosts(HOSTS)
def package_setup(use_db_backend=True):
    """ Install all the required packages """
    env.user=ROOT_USER
    env.password=ROOT_PASS

    # for ppa use
    package_update_apt()
    package_update()
    package_ensure('python-software-properties')
    repository_ensure_apt("-y ppa:nginx/stable") # no prompt

    package_update_apt()
    package_update()

    # to get the most up to date nginx
    package_ensure("supervisor")
    package_ensure("nginx")
    package_ensure("git-core gitosis")
    package_ensure("python-pip python-dev build-essential")
    run("aptitude install memcached -y")

    # TODO: This isn't very idempotent
    # As seen in:
    #   https://bitbucket.org/kmike/django-fab-deploy/src/1e9b66839da6/fab_deploy/db/mysql.py
    if use_db_backend:
        version='5.1'
        passwd='changeme123'
        run('aptitude install -y debconf-utils')

        debconf_defaults = [
            "mysql-server-%s mysql-server/root_password_again password %s" % (version, passwd),
            "mysql-server-%s mysql-server/root_password password %s" % (version, passwd),
            ]

        run("echo '%s' | debconf-set-selections" % "\n".join(debconf_defaults))

        warn('\n=========\nThe password for mysql "root" user will be set to "%s"\n=========\n' % passwd)
        run('aptitude install -y mysql-server')
    package_ensure("libmysqlclient-dev") # for mysql

    run("easy_install pip")
    run("pip install virtualenv")
    run("pip install virtualenvwrapper")

@hosts(HOSTS)
def configure_database(use_db_backend=True):
    """ creates the database """
    env.user=RTD_USER
    env.password=RTD_PASS

    if use_db_backend:
        run("mysql -u root -p'changeme123' -e \"%s\"" % (CREATE_DB_SQL % {'db_name': 'readthedocs'} ))
        try:
            run("mysql -u root -p'changeme123' readthedocs -e \"%s\"" % (DELETE_USER_SQL % { 'db_user': 'readthedocs_user'}))
        except:
            pass # may fail the first time through
        run("mysql -u root -p'changeme123' readthedocs -e \"%s\"" % (CREATE_USER_SQL % { 'db_user': 'readthedocs_user', 'db_password': 'readthedocs_pass_123'}))
        run("mysql -u root -p'changeme123' -e \"%s\"" % (GRANT_PERMISSIONS_SQL % { 'db_user': 'readthedocs_user', 'db_name': 'readthedocs'}))


@hosts(HOSTS)
def project_layout():
    """ Makes project directories """
    env.user=RTD_USER
    env.password=RTD_PASS

    dir_ensure("/opt/rtd/apps/readthedocs", recursive=True)
    dir_ensure("/opt/rtd/htdocs")
    dir_ensure("/opt/rtd/tmp")
    dir_ensure("/opt/rtd/logs")

@hosts(HOSTS)
def make_virtualenv():
    """ builds project in virtual environment """
    env.user=RTD_USER
    env.password=RTD_PASS

    # build the virtualenv
    with cd("/opt/rtd/apps/readthedocs"):
        if not dir_exists("/opt/rtd/apps/readthedocs/%s" % RTD_INITIAL_VERSION):
            run("virtualenv %s" % RTD_INITIAL_VERSION)
        if not dir_exists("/opt/rtd/apps/readthedocs/current"):
            file_link("/opt/rtd/apps/readthedocs/%s" % RTD_INITIAL_VERSION, "/opt/rtd/apps/readthedocs/current")

    # clone the repo
    with cd("/opt/rtd/apps/readthedocs/%s" % RTD_INITIAL_VERSION):
        if not dir_exists("/opt/rtd/apps/readthedocs/%s/%s" % (RTD_INITIAL_VERSION, RTD_CLONE_NAME)):
            run("git clone %s %s" % ( RTD_CLONE, RTD_CLONE_NAME) )

@hosts(HOSTS)
def bootstrap_virtualenv():
    """ install required packages """
    env.user=RTD_USER
    env.password=RTD_PASS

    run("source /opt/rtd/apps/readthedocs/current/bin/activate && pip install -r /opt/rtd/apps/readthedocs/current/readthedocs.org/pip_requirements.txt")

@hosts(HOSTS)
def link_django_settings():
    """ links the django settings file for the current env """
    with cd("/opt/rtd/apps/readthedocs/current/readthedocs.org/readthedocs/settings"):
        if not file_exists("currentenv.py"):
            file_link("prod.py","currentenv.py")

@hosts(HOSTS)
def link_nginx():
    # TODO: would be better as sudo
    env.user=ROOT_USER
    env.password=ROOT_PASS

    if not file_exists("/etc/nginx/sites-enabled/rtf.conf"):
        with cd("/etc/nginx/sites-enabled"):
            file_link("/opt/rtd/apps/readthedocs/current/readthedocs.org/conf/nginx.conf", "rtf.conf")

@hosts(HOSTS)
def link_supervisor():
    # TODO: would be beter as sudo
    env.user=ROOT_USER
    env.password=ROOT_PASS

    if not file_exists("/etc/supervisor/conf.d/rtf.conf"):
        with cd("/etc/supervisor/conf.d"):
            file_link("/opt/rtd/apps/readthedocs/current/readthedocs.org/conf/supervisor.conf", "rtf.conf")


@hosts(HOSTS)
def system_prep():
    """ pre-req process startup """
    env.user=ROOT_USER
    env.password=ROOT_PASS

    run("/etc/init.d/nginx restart")
    run("supervisorctl reload")

