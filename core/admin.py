from django.contrib import admin
from .models import Species, UnderwaterData, DetectionResult, ShoalAnalysis, AnalysisReport

@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'scientific_name', 'category', 'conservation_status')
    search_fields = ('name', 'scientific_name', 'category')
    list_filter = ('category', 'conservation_status')

@admin.register(UnderwaterData)
class UnderwaterDataAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_type', 'uploader', 'upload_date', 'location', 'depth', 'is_processed')
    list_filter = ('file_type', 'is_processed', 'upload_date')
    search_fields = ('title', 'location', 'uploader__username')

@admin.register(DetectionResult)
class DetectionResultAdmin(admin.ModelAdmin):
    list_display = ('data', 'species', 'confidence', 'frame_number')
    list_filter = ('species',)
    search_fields = ('data__title', 'species__name')

@admin.register(ShoalAnalysis)
class ShoalAnalysisAdmin(admin.ModelAdmin):
    list_display = ('data', 'shoal_id', 'species_count', 'average_speed', 'movement_pattern', 'analysis_date')
    list_filter = ('movement_pattern',)
    search_fields = ('shoal_id', 'data__title')

@admin.register(AnalysisReport)
class AnalysisReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'data_source')
    list_filter = ('created_at', 'created_by')
    search_fields = ('title', 'summary', 'data_source__title')
