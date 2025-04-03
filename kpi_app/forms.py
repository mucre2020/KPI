from django import forms
from .models import KPI, Division, Unit

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()

class FilterForm(forms.Form):
    year = forms.ChoiceField(choices=[], required=False)
    month = forms.ChoiceField(choices=[], required=False)
    division = forms.ChoiceField(choices=[], required=False)
    unit = forms.ChoiceField(choices=[], required=False)  # Add unit field

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        kpis = KPI.objects.all()
        if user.is_authenticated and hasattr(user, 'userprofile'):
            if user.userprofile.role == 'division_manager':
                kpis = kpis.filter(division=user.userprofile.division)
        self.fields['year'].choices = [(y, y) for y in sorted(kpis.values_list('year', flat=True).distinct())]
        self.fields['month'].choices = [(m, m) for m in kpis.values_list('month', flat=True).distinct()]
        self.fields['division'].choices = [(d.name, d.name) for d in Division.objects.all()]
        self.fields['unit'].choices = [('', 'All Units')] + [(u.name, u.name) for u in Unit.objects.all()]