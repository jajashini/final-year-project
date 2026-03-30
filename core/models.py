from django.db import models
from django.contrib.auth.models import User

class Species(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=150, blank=True, null=True)
    category = models.CharField(max_length=50) # e.g., Fish, Crustacean, Mammal
    description = models.TextField(blank=True)
    conservation_status = models.CharField(max_length=50, blank=True)
    image_sample = models.ImageField(upload_to='species_samples/', blank=True, null=True)

    def __str__(self):
        return self.name

class UnderwaterData(models.Model):
    DATA_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='underwater_data/')
    file_type = models.CharField(max_length=10, choices=DATA_TYPES)
    upload_date = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True)
    depth = models.FloatField(help_text="Depth in meters", null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    device_info = models.CharField(max_length=255, blank=True)
    
    # Processed states
    enhanced_file = models.FileField(upload_to='enhanced_data/', blank=True, null=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.file_type})"

class DetectionResult(models.Model):
    data = models.ForeignKey(UnderwaterData, on_delete=models.CASCADE, related_name='detections')
    species = models.ForeignKey(Species, on_delete=models.SET_NULL, null=True)
    confidence = models.FloatField()
    box_x = models.FloatField()
    box_y = models.FloatField()
    box_w = models.FloatField()
    box_h = models.FloatField()
    frame_number = models.IntegerField(default=0) # For videos
    timestamp_offset = models.FloatField(default=0.0)

class ShoalAnalysis(models.Model):
    data = models.ForeignKey(UnderwaterData, on_delete=models.CASCADE, related_name='shoal_analyses')
    shoal_id = models.CharField(max_length=100)
    species_count = models.IntegerField()
    average_speed = models.FloatField()
    movement_pattern = models.CharField(max_length=100) # e.g., Linear, Circular, Erratic
    analysis_date = models.DateTimeField(auto_now_add=True)
    trajectory_data = models.JSONField(null=True, blank=True) # Store coordinates over time

class AnalysisReport(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    data_source = models.ForeignKey(UnderwaterData, on_delete=models.CASCADE)
    summary = models.TextField()
    pdf_report = models.FileField(upload_to='reports/', blank=True, null=True)
    csv_report = models.FileField(upload_to='reports/', blank=True, null=True)

    def __str__(self):
        return self.title
