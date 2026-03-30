from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import pandas as pd
from django.core.files.base import ContentFile
import csv

class ReportGenerator:
    @staticmethod
    def generate_pdf(data_obj, detections):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 750, f"MarineVision Analysis Report: {data_obj.title}")
        
        p.setFont("Helvetica", 12)
        p.drawString(100, 720, f"Captured at: {data_obj.location or 'Unknown'}")
        p.drawString(100, 700, f"Depth: {data_obj.depth or 'N/A'}m")
        p.drawString(100, 680, f"Device: {data_obj.device_info or 'N/A'}")
        
        p.drawString(100, 650, "--------------------------------------------------")
        p.drawString(100, 630, "Species Detection Results:")
        
        y = 610
        for det in detections:
            p.drawString(120, y, f"- {det.species.name}: {det.confidence:.2f}% confidence")
            y -= 20
            if y < 100:
                p.showPage()
                y = 750
        
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer.read()

    @staticmethod
    def generate_csv(detections):
        buffer = BytesIO()
        # Reportlab doesn't handle CSV, but we can use standard csv
        pass # I'll do this directly in the view or here
