from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProjectModelForm

# Create your views here.
from .models import Project
from klienci.models import Client

@login_required(login_url='/')
def project_list_view(request):
    qs = Project.objects.all()
    context = {'object_list': qs, 'title': 'Projekty'}
    return render(request, 'projects.html', context)

@login_required(login_url='/')
def project_create_view(request):
    form = ProjectModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        form.save()
        form = ProjectModelForm()
    qs = Client.objects.all()
    context = {'object_list': qs, 'form': form, 'title': 'Nowy projekt', 'commit': 'Utwórz'}
    return render(request, 'project_new.html', context)

@login_required(login_url='/')
def project_detail_view(request, project_id):
    obj = get_object_or_404(Project, id=project_id)
    page_label = Project.objects.get(pk=project_id)
    context = {'object': obj, 'title': page_label.project_name}
    return render(request, 'project.html', context)

@login_required(login_url='/')
def project_update_view(request, project_id):
    obj = get_object_or_404(Project, id=project_id)
    form = ProjectModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    page_label = Project.objects.get(pk=project_id)
    context = {'object': obj, 'title': page_label.project_name, 'form': form, 'commit': 'Zapisz'}
    return render(request, 'project_new.html', context)

@login_required(login_url='/')
def project_delete_view(request, project_id):
    obj = get_object_or_404(Project, id=project_id)
    obj.delete()
    return redirect('/')
