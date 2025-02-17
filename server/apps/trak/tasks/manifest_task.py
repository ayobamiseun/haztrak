import datetime
import logging
from typing import Dict, List, Optional

from celery import Task, shared_task, states
from celery.exceptions import Ignore, Reject

from apps.sites.models import RcraSiteType
from apps.trak.models import QuickerSign

logger = logging.getLogger(__name__)


@shared_task(name="pull manifest", bind=True, acks_late=True)
def pull_manifest(self: Task, *, mtn: List[str], username: str) -> dict:
    """
    This task initiates a call to the ManifestService to pull a manifest by MTN
    """

    from apps.core.services import TaskService
    from apps.trak.services import ManifestService

    logger.debug(f"start task {self.name}, manifest {mtn}")
    task_status = TaskService(task_id=self.request.id, task_name=self.name, status="STARTED")
    try:
        manifest_service = ManifestService(username=username)
        results = manifest_service.pull_manifests(tracking_numbers=mtn)
        task_status.update_task_status(status="SUCCESS", results=results)
        return results
    except (ConnectionError, TimeoutError):
        task_status.update_task_status(status="FAILURE")
        raise Reject()
    except Exception as exc:
        task_status.update_task_status(status="FAILURE")
        self.update_state(state=states.FAILURE, meta={"unknown error": str(exc)})
        raise Ignore()


@shared_task(name="sign manifests", bind=True, acks_late=True)
def sign_manifest(
    self: Task,
    *,
    username: str,
    mtn: List[str],
    site_id: str,
    site_type: RcraSiteType | str,
    printed_name: str,
    printed_date: datetime.datetime,
    transporter_order: Optional[int] = None,
) -> Dict:
    """
    a task to Quicker Sign manifest, by MTN, in RCRAInfo
    """
    from apps.trak.services import ManifestService

    logger.debug(f"start task {self.name}, manifest {mtn}")
    try:
        manifest_service = ManifestService(username=username)
        signature = QuickerSign(
            mtn=mtn,
            site_id=site_id,
            site_type=site_type,
            printed_name=printed_name,
            printed_date=printed_date,
            transporter_order=transporter_order,
        )
        results = manifest_service.sign_manifest(signature)
        return results
    except (ConnectionError, TimeoutError) as exc:
        raise Reject(exc)
    except ValueError as exc:
        self.update_state(state=states.FAILURE, meta={"error": f"{repr(exc)}"})
        raise Ignore()
    except Exception as exc:
        self.update_state(state=states.FAILURE, meta={"unknown error": f"{exc}"})
        raise Ignore()


@shared_task(name="sync site manifests", bind=True)
def sync_site_manifests(self, *, site_id: str, username: str):
    """asynchronous task to sync an EPA site's manifests"""
    from apps.sites.services import SiteService

    try:
        site_service = SiteService(username=username)
        results = site_service.sync_rcra_manifest(site_id=site_id)
        return results
    except Exception as exc:
        logger.error(f"failed to sync {site_id} manifest")
        self.update_state(state=states.FAILURE, meta={f"error: {exc}"})
        raise Ignore()


@shared_task(name="create rcra manifests", bind=True)
def create_rcra_manifest(self, *, manifest: dict, username: str):
    """
    asynchronous task to use the RCRAInfo web services to create an electronic (RCRA) manifest
    it accepts a Python dict of the manifest data to be submitted as JSON, and the username of the
    user who is creating the manifest
    """
    from apps.core.services import TaskService
    from apps.trak.services import ManifestService, ManifestServiceError

    logger.info(f"start task: {self.name}")
    task_status = TaskService(task_id=self.request.id, task_name=self.name, status="STARTED")
    try:
        manifest_service = ManifestService(username=username)
        new_manifest = manifest_service.create_rcra_manifest(manifest=manifest)
        if new_manifest:
            task_status.update_task_status(status="SUCCESS", results=new_manifest)
            return new_manifest
        raise ManifestServiceError("error creating manifest")
    except ManifestServiceError as exc:
        logger.error(f"failed to create manifest ({manifest}): {exc.message}")
        task_status.update_task_status(status="FAILURE", results=exc.message)
        return {"error": exc.message}
    except Exception as exc:
        logger.error("error: ", exc)
        task_status.update_task_status(status="FAILURE", results={"result": str(exc)})
        return {"error": f"Internal Error: {exc}"}
