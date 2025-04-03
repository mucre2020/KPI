from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import models
import pandas as pd
from .models import Division, Unit, KPI, UserProfile
from .forms import ExcelUploadForm, FilterForm

@login_required
def dashboard(request):
    user_role = request.user.userprofile.role if hasattr(request.user, 'userprofile') else 'director'
    kpis = KPI.objects.all()

    if user_role not in ['director_general', 'admin']:
        if user_role == 'division_manager':
            kpis = kpis.filter(division=request.user.userprofile.division)
        elif user_role == 'director':
            kpis = kpis  # Directors see all, no upload

    form = FilterForm(request.user, request.GET or None)
    if form.is_valid():
        if form.cleaned_data['year']:
            kpis = kpis.filter(year=form.cleaned_data['year'])
        if form.cleaned_data['month']:
            kpis = kpis.filter(month=form.cleaned_data['month'])
        if form.cleaned_data['division'] and user_role in ['director_general', 'admin', 'director']:
            kpis = kpis.filter(division__name=form.cleaned_data['division'])
        if form.cleaned_data['unit']:
            kpis = kpis.filter(unit__name=form.cleaned_data['unit'])

    # Aggregate data for line chart (trends over time)
    trends = kpis.values('year', 'month').annotate(
        total_received=models.Sum('cases_received'),
        total_reported=models.Sum('cases_reported')
    ).order_by('year', 'month')
    trend_labels = [f"{t['month']} {t['year']}" for t in trends]
    trend_received = [t['total_received'] for t in trends]
    trend_reported = [t['total_reported'] for t in trends]

    # Aggregate data for pie chart (cases by division)
    division_cases = kpis.values('division__name').annotate(
        total_received=models.Sum('cases_received')
    ).order_by('division__name')
    division_labels = [d['division__name'] for d in division_cases if d['division__name']]
    division_values = [d['total_received'] for d in division_cases if d['division__name']]

    context = {
        'form': form,
        'kpis': kpis,
        'user_role': user_role,
        'total_received': kpis.aggregate(models.Sum('cases_received'))['cases_received__sum'] or 0,
        'total_reported': kpis.aggregate(models.Sum('cases_reported'))['cases_reported__sum'] or 0,
        'total_amount': kpis.aggregate(models.Sum('amount'))['amount__sum'] or 0,
        'avg_resolution': sum(kpi.resolution_rate for kpi in kpis) / kpis.count() if kpis.exists() else 0,
        'trend_labels': trend_labels,
        'trend_received': trend_received,
        'trend_reported': trend_reported,
        'division_labels': division_labels,
        'division_values': division_values,
    }
    return render(request, 'kpi_app/dashboard.html', context)

# ... (other views: upload_excel, download_summary remain unchanged) ...

@login_required
def upload_excel(request):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role not in ['admin']:
        return redirect('dashboard')
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            df['Cases Received'] = pd.to_numeric(df['Cases Received'], errors='coerce').fillna(0).astype(int)
            df['Cases Reported'] = pd.to_numeric(df['Cases Reported'], errors='coerce').fillna(0).astype(int)
            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
            for _, row in df.iterrows():
                division, _ = Division.objects.get_or_create(name=row['Division'])
                unit, _ = Unit.objects.get_or_create(name=row['Unit'], division=division)
                KPI.objects.create(
                    division=division,
                    unit=unit,
                    year=int(row['Year']),
                    month=row['Month'],
                    cases_received=row['Cases Received'],
                    cases_reported=row['Cases Reported'],
                    amount=row['Amount'] if pd.notna(row['Amount']) else None,
                    uploaded_by=request.user
                )
            return redirect('dashboard')
    else:
        form = ExcelUploadForm()
    return render(request, 'kpi_app/upload.html', {'form': form})

@login_required
def download_summary(request):
    user_role = request.user.userprofile.role if hasattr(request.user, 'userprofile') else 'director'
    kpis = KPI.objects.all()
    if user_role == 'division_manager':
        kpis = kpis.filter(division=request.user.userprofile.division)
    summary_data = {
        "Cases Received": kpis.aggregate(models.Sum('cases_received'))['cases_received__sum'] or 0,
        "Cases Reported": kpis.aggregate(models.Sum('cases_reported'))['cases_reported__sum'] or 0,
        "Resolution Rate (%)": round(sum(kpi.resolution_rate for kpi in kpis) / kpis.count(), 1) if kpis.exists() else 0,
        "Total Amount (RWF)": kpis.aggregate(models.Sum('amount'))['amount__sum'] or 0
    }
    df = pd.DataFrame([summary_data])
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Executive_Summary.csv"'
    df.to_csv(response, index=False)
    return response

# ... (previous imports and dashboard view) ...

@login_required
def unit_details(request):
    unit_name = request.GET.get('unit')
    year = request.GET.get('year')
    month = request.GET.get('month')
    division = request.GET.get('division')

    kpis = KPI.objects.filter(unit__name=unit_name)
    if year:
        kpis = kpis.filter(year=year)
    if month:
        kpis = kpis.filter(month=month)
    if division:
        kpis = kpis.filter(division__name=division)

    # Aggregate data by month for the selected unit
    monthly_data = kpis.values('year', 'month').annotate(
        total_received=models.Sum('cases_received'),
        total_reported=models.Sum('cases_reported')
    ).order_by('year', 'month')

    context = {
        'unit_name': unit_name,
        'monthly_data': monthly_data,
        'labels': [f"{d['month']} {d['year']}" for d in monthly_data],
        'received': [d['total_received'] for d in monthly_data],
        'reported': [d['total_reported'] for d in monthly_data],
    }
    return render(request, 'kpi_app/unit_details.html', context)