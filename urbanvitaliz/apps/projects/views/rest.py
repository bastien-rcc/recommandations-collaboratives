# encoding: utf-8

"""
Views for projects application

author  : raphael.marvie@beta.gouv.fr,guillaume.libersat@beta.gouv.fr
created : 2021-05-26 15:56:20 CEST
"""

from django.contrib.contenttypes.models import ContentType
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .. import models
from ..serializers import (
    ProjectSerializer,
    TaskFollowupSerializer,
    TaskNotificationSerializer,
    TaskSerializer,
)


########################################################################
# REST API
########################################################################
class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """

    def get_queryset(self):
        return models.Project.objects.for_user(self.request.user).order_by(
            "-created_on", "-updated_on"
        )

    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaskFollowupViewSet(viewsets.ModelViewSet):
    """
    API endpoint for TaskFollowups
    """

    serializer_class = TaskFollowupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = int(self.kwargs["project_id"])
        task_id = int(self.kwargs["task_id"])

        user_projects = list(
            models.Project.objects.for_user(self.request.user).values_list(flat=True)
        )

        if project_id not in user_projects:
            raise PermissionDenied()

        return models.TaskFollowup.objects.filter(task_id=task_id)

    def create(self, request, project_id, task_id):
        data = request.data
        data["task_id"] = task_id
        data["who_id"] = request.user.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        followup = serializer.save()

        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint for project tasks
    """

    @action(
        methods=["post"],
        detail=True,
    )
    def move(self, request, project_id, pk):
        task = self.get_object()

        above_id = request.POST.get("above", None)
        below_id = request.POST.get("below", None)

        if above_id:
            other_pk = above_id
        else:
            other_pk = below_id

        try:
            other_task = models.Task.objects.get(
                project_id=task.project_id, pk=other_pk
            )
        except models.Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if above_id:
            task.above(other_task)
            return Response({"status": "insert above done"})

        if below_id:
            task.below(other_task)
            return Response({"status": "insert below done"})

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        project_id = int(self.kwargs["project_id"])

        user_projects = list(
            models.Project.objects.for_user(self.request.user).values_list(flat=True)
        )

        if project_id not in user_projects:
            raise PermissionDenied()

        return models.Task.objects.filter(project_id=project_id).order_by(
            "-created_on", "-updated_on"
        )

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaskNotificationViewSet(
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint for Task
    """

    def get_queryset(self):
        task_id = int(self.kwargs["task_id"])
        task = models.Task.objects.get(pk=task_id)

        notifications = self.request.user.notifications.unread()

        task_ct = ContentType.objects.get_for_model(models.Task)
        followup_ct = ContentType.objects.get_for_model(models.TaskFollowup)

        task_actions = notifications.filter(
            action_object_content_type=task_ct.pk,
            action_object_object_id=task_id,
        )

        followup_ids = list(task.followups.all().values_list("id", flat=True))

        followup_actions = notifications.filter(
            action_object_content_type=followup_ct.pk,
            action_object_object_id__in=followup_ids,
        )

        return task_actions | followup_actions

    @action(
        methods=["post"],
        detail=False,
    )
    def mark_all_as_read(self, request, project_id, task_id):
        self.get_queryset().mark_all_as_read(request.user)
        return Response({}, status=status.HTTP_200_OK)

    serializer_class = TaskNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]


# eof
