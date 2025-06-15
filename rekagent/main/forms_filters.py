from django import forms
from datetime import date, timedelta


class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        label='Начальная дата',
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    end_date = forms.DateField(
        label='Конечная дата',
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Установка значений по умолчанию, если не заданы
        if not args and not kwargs.get('data'):
            self.fields['end_date'].initial = date.today()
            self.fields['start_date'].initial = date.today() - \
                timedelta(days=30)
