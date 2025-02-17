import logging

from celery import Task, shared_task, states
from celery.exceptions import Ignore, Reject
from requests import RequestException

from apps.sites.services.profile_services import RcraProfileServiceError

logger = logging.getLogger(__name__)


class RcraProfileTasks(Task):
    """RcraProfileTasks acts as our base Celery class that encapsulate all logic related
    to a user's RCRAInfo profile"""

    username: str


@shared_task(name="sync profile", base=RcraProfileTasks, bind=True, acks_late=True)
def sync_user_sites(self: RcraProfileTasks, username: str) -> None:
    """
    This task initiates a call to the RcraProfileService to pull a user's RCRAInfo profile
    and update that information in Haztrak.
    """
    from apps.sites.services import RcraProfileService

    try:
        profile_service = RcraProfileService(username=username)
        profile_service.pull_rcra_profile()
    except (ConnectionError, RequestException, TimeoutError):
        # ToDo retry if network error, see celery docs
        raise Reject()
    except RcraProfileServiceError as exc:
        self.update_state(state=states.FAILURE, meta={"error": f"{str(exc)}"})
        raise Ignore()
    except Exception as exc:
        self.update_state(state=states.FAILURE, meta={"unknown error": f"{str(exc)}"})
        raise Ignore()
