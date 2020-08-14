from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ClientModelForm

# Create your views here.
from .models import Client

@login_required(login_url='/')
def client_list_view(request):
    qs = Client.objects.all()
    context = {'object_list': qs, 'title': 'Klienci'}
    return render(request, 'clients.html', context)

@login_required(login_url='/')
def client_create_view(request):
    form = ClientModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        form.save()
        form = ClientModelForm()
    qs = Client.objects.all()
    context = {'object_list': qs, 'form': form, 'title': 'Nowy klient', 'commit': 'Utwórz'}
    return render(request, 'client_new.html', context)

@login_required(login_url='/')
def client_detail_view(request, client_id):
    obj = get_object_or_404(Client, id=client_id)
    page_label = Client.objects.get(pk=client_id)
    context = {'object': obj, 'title': page_label.client_name}
    return render(request, 'client.html', context)

@login_required(login_url='/')
def client_update_view(request, client_id):
    obj = get_object_or_404(Client, id=client_id)
    form = ClientModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    page_label = Client.objects.get(pk=client_id)
    context = {'object': obj, 'title': page_label.client_name, 'form': form, 'commit': 'Zapisz'}
    return render(request, 'client_new.html', context)

@login_required(login_url='/')
def client_delete_view(request, client_id):
    obj = get_object_or_404(Client, id=client_id)
    obj.delete()
    return redirect('/clients')