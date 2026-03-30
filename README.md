# AI-Driven Marine Vision System

A high-performance, full-stack AI platform built with Django for underwater species detection, tracking, and shoal analysis.

## Features
- **Underwater Image Enhancement**: CLAHE, Retinex, and Color Correction to handle low-visibility environments.
- **AI Species Detection**: YOLO-based identification of marine life.
- **Spatio-Temporal Tracking**: Shoal behavior analysis and trajectory mapping.
- **Premium Dashboard**: Real-time analytics and mission monitoring.
- **Automated Reporting**: PDF generation for research documentation.

## Tech Stack
- **Backend**: Python 3.x, Django 5.x
- **AI/CV**: OpenCV, PyTorch, NumPy, Scikit-image
- **Frontend**: Vanilla CSS (Glassmorphism), Chart.js
- **Reports**: ReportLab, Pandas

## Getting Started

1. **Install Dependencies**:
   ```bash
   pip install django djangorestframework django-environ pillow opencv-python numpy scikit-image torch torchvision reportlab pandas matplotlib plotly
   ```

2. **Run Migrations**:
   ```bash
   python manage.py makemigrations core
   python manage.py migrate
   ```

3. **Seed Data (Optional)**:
   ```bash
   python scripts/seed_data.py
   ```
   *Creates superuser: `admin` / `admin123`*

4. **Start Server**:
   ```bash
   python manage.py runserver
   ```

## Mission Architecture
- `core/ai_processor.py`: Contains the CV enhancement and detection logic.
- `core/models.py`: Defines the oceanic database schema.
- `core/report_gen.py`: Handles PDF report compilation.
- `static/css/main.css`: The "Deep Sea" premium design system.
