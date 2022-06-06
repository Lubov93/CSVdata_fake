from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from data.models import Data


@login_required
def list_all_datas(request):
    """
    Display all datas belong to current user
    """
    user = User.objects.get(id=request.user.id)
    all_datas = Data.objects.filter(user=user)

    context = {"datas": all_datas}
    return render(request, 'data/list_datas.html', context)
