import logging
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from django.core.management.base import BaseCommand
from projects import tasks
from projects.models import Project, ImportedFile
from builds.models import Version

log = logging.getLogger(__name__)

class Command(BaseCommand):

    help = '''\
Creates a readthedocs demo api user for one button deploy
'''

    def handle(self, *args, **kwargs):
        """ Creates demo api user """
        try:
            user = User.objects.get(username="test")
        except ObjectDoesNotExist:
            user = User.objects.create(username="test", email="test@example.com")
            user.set_password("test")
            user.save()
