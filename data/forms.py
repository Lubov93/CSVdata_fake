from django import forms

from .models import *


class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ('name', 'separator',)


ColumnFormset = forms.modelformset_factory(
    DataColumn,
    fields=('name', 'column_type', 'integer_range_from',
            'integer_range_to', 'order'),
    extra=4,
)


class DataRowsForm(forms.Form):
    rows = forms.IntegerField()