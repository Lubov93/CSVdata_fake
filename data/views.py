from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from data.forms import DataForm, ColumnFormset, DataRowsForm
from data.models import Data, DataColumn
from data.tasks import create_csv


@login_required
def list_all_datas(request):
    """
    Display all datas belong to current user
    """
    user = User.objects.get(id=request.user.id)
    all_datas = Data.objects.filter(user=user)

    context = {"datas": all_datas}
    return render(request, 'data/list_datas.html', context)


@login_required
def create_data(request):
    """
    Create data with columns
    """
    user = User.objects.get(id=request.user.id)
    data_form = DataForm(request.GET or None)
    formset = ColumnFormset(queryset=DataColumn.objects.none())

    if request.method == 'POST':
        data_form = DataForm(request.POST)
        formset = ColumnFormset(request.POST)
        if data_form.is_valid() and formset.is_valid():
            data = data_form.save(commit=False)
            data.user = user
            data = data_form.save()

            for form in formset:
                column = form.save(commit=False)
                column.data = data
                column.save()
            return redirect('data:datas')
        else:
            return HttpResponse(
                'Fields are incorrect.Please,  try again.')

    context = {'data_form': data_form, 'formset': formset}
    return render(request, 'data/create.html', context)


@login_required
def data_view(request, id):
    """Display a list of created csv files and their status"""
    data = Data.objects.get(id=id)
    form = DataRowsForm(request.POST or None)

    if request.method == 'POST':
        rows = int(request.POST.get('rows'))

        generating_task = create_csv.delay(data.id, rows)

        task_id = generating_task.task_id

        context = {'data': data, 'form': form, 'task_id': task_id}
        return render(request, 'data/view_data.html', context)
    else:
        form = DataRowsForm()
    context = {'data': data, 'form': form}
    return render(request, 'data/view_data.html', context)