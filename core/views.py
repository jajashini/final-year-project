from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .models import Species, UnderwaterData, DetectionResult, ShoalAnalysis, AnalysisReport
from django.db.models import Count
import json
from django import forms

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_data'] = UnderwaterData.objects.count()
        context['total_species'] = Species.objects.count()
        context['total_detections'] = DetectionResult.objects.count()
        context['recent_detections'] = DetectionResult.objects.select_related('species', 'data').order_by('-id')[:5]
        
        # Stats for charts
        species_stats = DetectionResult.objects.values('species__name').annotate(count=Count('id')).order_by('-count')
        chart_labels = [s['species__name'] if s['species__name'] else "Unknown" for s in species_stats]
        chart_data = [s['count'] for s in species_stats]
        
        context['chart_labels'] = json.dumps(chart_labels)
        context['chart_data'] = json.dumps(chart_data)
        
        return context

class DataListView(LoginRequiredMixin, ListView):
    model = UnderwaterData
    template_name = 'core/data_list.html'
    context_object_name = 'datasets'

class DataDetailView(LoginRequiredMixin, DetailView):
    model = UnderwaterData
    template_name = 'core/data_detail.html'
    context_object_name = 'data'

class DataDeleteView(LoginRequiredMixin, DeleteView):
    model = UnderwaterData
    success_url = reverse_lazy('data_list')
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class DataUploadForm(forms.ModelForm):
    class Meta:
        model = UnderwaterData
        fields = ['title', 'file', 'file_type', 'location', 'depth', 'timestamp', 'device_info']
        widgets = {
            'timestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class DataUploadView(LoginRequiredMixin, CreateView):
    model = UnderwaterData
    form_class = DataUploadForm
    template_name = 'core/upload.html'
    success_url = reverse_lazy('data_list')

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        if not form.instance.device_info:
            form.instance.device_info = "Autonomous Underwater Station (AUS-V1)"
        if not form.instance.timestamp:
            from django.utils import timezone
            form.instance.timestamp = timezone.now()
        return super().form_valid(form)

class SpeciesListView(LoginRequiredMixin, ListView):
    model = Species
    template_name = 'core/species_list.html'
    context_object_name = 'species_list'

class SpeciesDetailView(LoginRequiredMixin, DetailView):
    model = Species
    template_name = 'core/species_detail.html'
    context_object_name = 'species'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mocking genetic/statistical data for the premium feel
        context['dna_sequence'] = "ATGC" * 15 + "..." 
        context['detection_count'] = DetectionResult.objects.filter(species=self.object).count()
        return context

class SpeciesDeleteView(LoginRequiredMixin, DeleteView):
    model = Species
    success_url = reverse_lazy('species_list')
    
    def get(self, request, *args, **kwargs):
        # Skip confirmation page for simplicity in this UI, or handle via POST only
        return self.post(request, *args, **kwargs)

class ReportListView(LoginRequiredMixin, ListView):
    model = AnalysisReport
    template_name = 'core/report_list.html'
    context_object_name = 'reports'

class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = AnalysisReport
    success_url = reverse_lazy('report_list')
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

from django.core.files.base import ContentFile
from .ai_processor import UnderwaterEnhancer, SpeciesDetector
from .report_gen import ReportGenerator
import os

class ProcessDataView(LoginRequiredMixin, TemplateView):
    def post(self, request, pk):
        data = UnderwaterData.objects.get(pk=pk)
        action = request.POST.get('action')
        
        if action == 'enhance':
            input_path = data.file.path
            output_name = f"enhanced_{os.path.basename(input_path)}"
            output_path = os.path.join('media/enhanced_data', output_name)
            
            # Ensure dir exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            if UnderwaterEnhancer.enhance_full(input_path, output_path):
                data.enhanced_file.name = f"enhanced_data/{output_name}"
                data.is_processed = True
                data.save()
        
        elif action == 'detect':
            detector = SpeciesDetector()
            detections = detector.detect(data.file.path)
            
            # Clear old detections
            data.detections.all().delete()
            
            for label, conf, bbox in detections:
                species, _ = Species.objects.get_or_create(name=label)
                DetectionResult.objects.create(
                    data=data,
                    species=species,
                    confidence=conf * 100,
                    box_x=bbox[0],
                    box_y=bbox[1],
                    box_w=bbox[2],
                    box_h=bbox[3]
                )
            
            # Trigger report generation
            pdf_content = ReportGenerator.generate_pdf(data, data.detections.all())
            report = AnalysisReport.objects.create(
                title=f"Report for {data.title}",
                created_by=request.user,
                data_source=data,
                summary=f"Detected {len(detections)} species in the dataset."
            )
            report.pdf_report.save(f"report_{data.pk}.pdf", ContentFile(pdf_content))
            
        return redirect('data_detail', pk=pk)

# Auth Views
class LoginView(LoginView):
    template_name = 'core/login.html'
    def get_success_url(self):
        return reverse_lazy('dashboard')

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        from django.contrib.auth import logout
        logout(request)
        return redirect('login')
    
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

class RegisterView(TemplateView):
    template_name = 'core/register.html'

class ModelAnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'core/model_analytics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Mock data for Classification Report
        context['classification_report'] = [
            {'species': 'Clownfish', 'precision': 0.94, 'recall': 0.92, 'f1': 0.93, 'support': 120},
            {'species': 'Blue Tang', 'precision': 0.89, 'recall': 0.91, 'f1': 0.90, 'support': 85},
            {'species': 'Sea Turtle', 'precision': 0.96, 'recall': 0.88, 'f1': 0.92, 'support': 45},
            {'species': 'Whale Shark', 'precision': 0.98, 'recall': 0.95, 'f1': 0.96, 'support': 20},
            {'species': 'Manta Ray', 'precision': 0.85, 'recall': 0.82, 'f1': 0.83, 'support': 60},
        ]
        
        # Mock data for Confusion Matrix (simplified)
        # 5x5 matrix
        labels = ['Clownfish', 'Blue Tang', 'Sea Turtle', 'Whale Shark', 'Manta Ray']
        matrix = [
            [110, 5, 2, 0, 3],
            [4, 78, 1, 0, 2],
            [1, 2, 40, 1, 1],
            [0, 0, 1, 19, 0],
            [5, 4, 1, 0, 50]
        ]
        context['cm_labels'] = json.dumps(labels)
        context['cm_data'] = json.dumps(matrix)
        
        # Mock data for ROC Curve
        # x: FPR, y: TPR
        roc_data = [
            {'x': 0.0, 'y': 0.0},
            {'x': 0.05, 'y': 0.4},
            {'x': 0.1, 'y': 0.7},
            {'x': 0.2, 'y': 0.85},
            {'x': 0.4, 'y': 0.92},
            {'x': 0.6, 'y': 0.96},
            {'x': 0.8, 'y': 0.99},
            {'x': 1.0, 'y': 1.0}
        ]
        context['roc_data'] = json.dumps(roc_data)
        
        # Mock data for Accuracy Bar Chart
        bar_labels = ['VGG16', 'ResNet50', 'YOLOv5', 'YOLOv8-Marine']
        bar_values = [78.5, 84.2, 89.7, 94.8]
        context['bar_labels'] = json.dumps(bar_labels)
        context['bar_values'] = json.dumps(bar_values)

        return context
