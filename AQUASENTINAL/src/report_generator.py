from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from pathlib import Path
from datetime import datetime
from config import BASE_DIR

def generate_pdf_report(risk_df, filename="aquasentinel_report.pdf"):
    out_path = BASE_DIR / filename
    doc = SimpleDocTemplate(str(out_path), pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor("#0B1630"),
        spaceAfter=20
    )
    
    elements = []
    
    # Header
    elements.append(Paragraph("AquaSentinel: Official Risk Report", title_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Summary
    high_risk_count = len(risk_df[risk_df['risk_level'] == 'High'])
    elements.append(Paragraph(f"Summary", styles['Heading2']))
    elements.append(Paragraph(f"There are currently {high_risk_count} areas classified as High Risk for waterborne disease outbreaks.", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Table Data
    data = [["Area", "WQI", "Risk Level", "Score"]]
    for _, row in risk_df.iterrows():
        data.append([
            row['area'], 
            f"{row.get('avg_wqi', 0):.1f}", 
            row.get('risk_level', 'Unknown'), 
            f"{row.get('risk_score', 0):.1f}"
        ])
        
    # Table Style
    t = Table(data, colWidths=[150, 100, 100, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0B1630")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    
    elements.append(t)
    doc.build(elements)
    
    return out_path
