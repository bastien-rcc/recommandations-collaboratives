# encoding: utf-8

"""
Views for projects application

author  : raphael.marvie@beta.gouv.fr,guillaume.libersat@beta.gouv.fr
created : 2022-12-19 11:56:20 CEST
"""
from django.http import Http404
from django.shortcuts import render

from recoco import utils
from recoco.apps.survey import models as survey_models

from .. import models


def project_detail_from_sharing_link(request, project_ro_key):
    """Return a special view of the project using the sharing link"""
    try:
        project = models.Project.on_site.get(ro_key=project_ro_key)
    except models.Project.DoesNotExist as exc:
        raise Http404 from exc

    try:
        site_config = utils.get_site_config_or_503(request.site)
        survey_models.Session.objects.get_or_create(
            project=project, survey=site_config.project_survey
        )
    except Exception:  # nosec
        pass

    return render(request, "projects/project/detail-ro.html", locals())
