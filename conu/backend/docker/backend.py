# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
This is backend for docker engine
"""
import logging

from conu.apidefs.backend import Backend
from conu.backend.docker.container import DockerContainer
from conu.backend.docker.image import DockerImage
from conu.backend.docker.client import get_client
from conu.backend.docker.constants import CONU_ARTIFACT_TAG


logger = logging.getLogger(__name__)


# let this class inherit docstring from its parent
class DockerBackend(Backend):
    """
    For more info on using the Backend classes, see documentation of
    the parent :class:`conu.apidefs.backend.Backend` class.
    """
    ContainerClass = DockerContainer
    ImageClass = DockerImage

    @staticmethod
    def cleanup_containers():
        client = get_client()
        conu_containers = client.containers(filters={'label': CONU_ARTIFACT_TAG}, all=True)
        for c in conu_containers:
            id = c['Id']
            logger.debug("Removing container %s created by conu", id)
            client.stop(id)
            client.remove_container(id)

    def __exit__(self, exc_type, exc_val, exc_tb):
        super(DockerBackend, self).__exit__(exc_type, exc_val, exc_tb)
        if self.cleanup:
            DockerBackend.cleanup_containers()
