# encoding: utf-8

"""
Views for projects application

author  : raphael.marvie@beta.gouv.fr,guillaume.libersat@beta.gouv.fr
created : 2021-05-26 15:56:20 CEST
"""

from django.contrib.auth.decorators import login_required

from django.core.exceptions import PermissionDenied

from django import forms

from django.urls import reverse

from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from . import models


########################################################################
# On boarding
########################################################################


def onboarding(request):
    """Return the onboarding page"""
    if request.method == "POST":
        form = OnboardingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return render(request, "projects/thanks.html", locals())
    else:
        form = OnboardingForm()
    return render(request, "projects/onboarding.html", locals())


class OnboardingForm(forms.ModelForm):
    """Form for onboarding a new local authority"""

    class Meta:
        model = models.Project
        fields = [
            "email",
            "first_name",
            "last_name",
            "org_name",
            "name",
            "location",
            "description",
            "impediments",
        ]


########################################################################
# Local authorities
########################################################################


@login_required
def myprojects(request):
    """Return the project followup for local authorities"""
    projects = models.Project.fetch(email=request.user.email)
    return render(request, "projects/myprojects.html", locals())


########################################################################
# Switchtender
########################################################################


@login_required
def project_list(request):
    """Return the projects for the switchtender"""
    is_staff_or_403(request.user)
    projects = models.Project.fetch().order_by("-created_on")
    return render(request, "projects/project/list.html", locals())


@login_required
def project_detail(request, project_id=None):
    """Return the details of given project for switchtender"""
    is_staff_or_403(request.user)
    project = get_object_or_404(models.Project, pk=project_id)
    return render(request, "projects/project/detail.html", locals())


@login_required
def create_note(request, project_id=None):
    """Create a new note for a project"""
    is_staff_or_403(request.user)
    project = get_object_or_404(models.Project, pk=project_id)
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.project = project
            instance.save()
            return redirect(reverse("projects-project-detail", args=[project_id]))
    else:
        form = NoteForm()
    return render(request, "projects/project/note.html", locals())


@login_required
def update_note(request, note_id=None):
    """Update an existing note for a project"""
    is_staff_or_403(request.user)
    note = get_object_or_404(models.Note, pk=note_id)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse("projects-project-detail", args=[note.project_id]))
    else:
        form = NoteForm(instance=note)
    return render(request, "projects/project/note.html", locals())


class NoteForm(forms.ModelForm):
    """Form new project note creation"""

    class Meta:
        model = models.Note
        fields = ["content", "tags", "public"]


@login_required
def create_task(request, project_id=None):
    """Create a new task for a project"""
    is_staff_or_403(request.user)
    project = get_object_or_404(models.Project, pk=project_id)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.project = project
            instance.save()
            return redirect(reverse("projects-project-detail", args=[project_id]))
    else:
        form = TaskForm()
    return render(request, "projects/project/task.html", locals())


@login_required
def update_task(request, task_id=None):
    """Update an existing task for a project"""
    is_staff_or_403(request.user)
    task = get_object_or_404(models.Task, pk=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse("projects-project-detail", args=[task.project_id]))
    else:
        form = TaskForm(instance=task)
    return render(request, "projects/project/task.html", locals())


class TaskForm(forms.ModelForm):
    """Form new project task creation"""

    class Meta:
        model = models.Task
        fields = ["content", "tags", "public", "deadline"]


########################################################################
# Helpers
########################################################################


def is_staff_or_403(user):
    """Raise a 403 error is user is not a staff member"""
    if not user or not user.is_staff:
        raise PermissionDenied("L'information demandée n'est pas disponible")


# eof
