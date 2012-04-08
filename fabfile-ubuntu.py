from cuisine import user_ensure, dir_ensure, user_passwd, package_ensure, run, package_upgrade_apt, package_update_apt, package_update, dir_exists, file_link
from fabric.context_managers import cd
from fabric.decorators import hosts
from fabric.state import env

HOSTS=['']  # add host here

ROOT_USER='root' # root user
ROOT_PASS=''     # password

RTD_USER='rtd_user'
RTD_PASS='rtd_pass_123'

RTD_CLONE='git://github.com/johncosta/readthedocs.org.git'
RTD_CLONE_NAME="readthedocs.org"
RTD_INITIAL_VERSION='v0.1'

@hosts(HOSTS)
def user_setup():
    """ Creates a read the docs user """
    env.user=ROOT_USER
    env.password=ROOT_PASS

    user_ensure(RTD_USER, home='/opt/rtd')
    user_passwd(RTD_USER, RTD_PASS )

@hosts(HOSTS)
def package_setup():
    """ Install all the required packages """
    env.user=ROOT_USER
    env.password=ROOT_PASS

    package_update_apt()
    package_update()

    package_ensure("supervisor nginx")
    package_ensure("git-core gitosis")
    package_ensure("python-pip python-dev build-essential")
    run("aptitude install memcached -y")

    run("easy_install pip")
    run("pip install virtualenv")
    run("pip install virtualenvwrapper")

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