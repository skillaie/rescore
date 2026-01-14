#!/usr/bin/env python3
"""Generate PDF resumes from resume data for demo purposes."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors

def create_resume_pdf(filename, resume_data):
    """Create a professional PDF resume."""
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    # Custom styles
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='Name',
        fontSize=18,
        fontName='Helvetica-Bold',
        spaceAfter=2,
        textColor=HexColor('#1a1a1a')
    ))
    
    styles.add(ParagraphStyle(
        name='ContactInfo',
        fontSize=10,
        fontName='Helvetica',
        spaceAfter=12,
        textColor=HexColor('#444444')
    ))
    
    styles.add(ParagraphStyle(
        name='SectionHeader',
        fontSize=11,
        fontName='Helvetica-Bold',
        spaceBefore=14,
        spaceAfter=6,
        textColor=HexColor('#2c5282')
    ))
    
    styles.add(ParagraphStyle(
        name='JobTitle',
        fontSize=11,
        fontName='Helvetica-Bold',
        spaceBefore=8,
        spaceAfter=2,
        textColor=HexColor('#1a1a1a')
    ))
    
    styles.add(ParagraphStyle(
        name='JobDetails',
        fontSize=10,
        fontName='Helvetica-Oblique',
        spaceAfter=4,
        textColor=HexColor('#666666')
    ))
    
    styles.add(ParagraphStyle(
        name='ResumeBody',
        fontSize=10,
        fontName='Helvetica',
        spaceAfter=3,
        leading=13,
        textColor=HexColor('#333333')
    ))
    
    styles.add(ParagraphStyle(
        name='BulletPoint',
        fontSize=10,
        fontName='Helvetica',
        leftIndent=15,
        spaceAfter=3,
        leading=13,
        textColor=HexColor('#333333')
    ))
    
    story = []
    
    # Header - Name and Contact
    story.append(Paragraph(resume_data['name'], styles['Name']))
    story.append(Paragraph(resume_data['contact'], styles['ContactInfo']))
    
    # Horizontal line
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#2c5282'), spaceAfter=10))
    
    # Process sections
    for section in resume_data['sections']:
        story.append(Paragraph(section['title'], styles['SectionHeader']))
        
        for item in section['items']:
            if 'position' in item:
                # Job/Education entry
                story.append(Paragraph(item['position'], styles['JobTitle']))
                story.append(Paragraph(item['details'], styles['JobDetails']))
                if 'bullets' in item:
                    for bullet in item['bullets']:
                        story.append(Paragraph(f"• {bullet}", styles['BulletPoint']))
            elif 'text' in item:
                # Simple text (skills, etc.)
                story.append(Paragraph(item['text'], styles['ResumeBody']))
            elif 'publications' in item:
                # Publication list
                for i, pub in enumerate(item['publications'], 1):
                    story.append(Paragraph(f"{i}. {pub}", styles['BulletPoint']))
    
    doc.build(story)
    print(f"Created: {filename}")

# Resume 1: Dr. Sarah Chen - Highly Qualified
sarah_chen = {
    'name': 'Dr. Sarah Chen, PhD',
    'contact': 'sarah.chen@email.com  |  linkedin.com/in/sarahchen-bio  |  Boston, MA',
    'sections': [
        {
            'title': 'CURRENT POSITION',
            'items': [{
                'position': 'Postdoctoral Research Fellow',
                'details': 'Broad Institute of MIT and Harvard  |  2021 – Present',
                'bullets': [
                    'Developing computational pipelines for multi-modal single-cell analysis in Alzheimer\'s disease models',
                    'Led collaborative project with 3 institutions studying glial cell heterogeneity',
                    'Secured K99/R00 Pathway to Independence Award ($800,000)',
                    'Mentored 2 graduate students and 1 undergraduate researcher'
                ]
            }]
        },
        {
            'title': 'EDUCATION',
            'items': [
                {
                    'position': 'PhD, Computational Biology',
                    'details': 'University of California, San Francisco  |  2016 – 2021',
                    'bullets': ['Dissertation: "Machine Learning Approaches to Single-Cell Transcriptomic Analysis in Neurodegenerative Disease"']
                },
                {
                    'position': 'BS, Biochemistry, Magna Cum Laude',
                    'details': 'University of Michigan  |  2012 – 2016',
                    'bullets': []
                }
            ]
        },
        {
            'title': 'PREVIOUS RESEARCH EXPERIENCE',
            'items': [{
                'position': 'Graduate Researcher',
                'details': 'UCSF Memory and Aging Center  |  2016 – 2021',
                'bullets': [
                    'Developed novel clustering algorithms for single-cell RNA-seq data',
                    'Established mouse colony and performed stereotaxic surgeries',
                    'Collaborated with clinicians on human brain tissue analysis'
                ]
            }]
        },
        {
            'title': 'PUBLICATIONS',
            'items': [{
                'publications': [
                    '<b>Chen S</b>, Martinez R, et al. (2024) "Single-cell atlas of the aging human brain." <i>Nature Neuroscience</i>. <b>First author.</b>',
                    '<b>Chen S</b>, Wong K, et al. (2023) "Computational methods for spatial transcriptomics." <i>Nature Methods</i>. <b>First author.</b>',
                    'Park J, <b>Chen S</b>, et al. (2023) "Microglial subtypes in neurodegeneration." <i>Cell</i>. Second author.',
                    '<b>Chen S</b>, et al. (2022) "Machine learning in single-cell biology." <i>Annual Review of Biomedical Data Science</i>. First author, review.',
                    'Liu M, <b>Chen S</b>, et al. (2021) "Astrocyte diversity in Alzheimer\'s disease." <i>Neuron</i>. Co-author.',
                    '<b>Chen S</b>, et al. (2020) "scBioCluster: A novel clustering approach." <i>Bioinformatics</i>. <b>First author.</b>'
                ]
            }]
        },
        {
            'title': 'TECHNICAL EXPERTISE',
            'items': [
                {'text': '<b>Computational:</b> Python, R, single-cell analysis (Scanpy, Seurat), machine learning (PyTorch, scikit-learn), cloud computing (AWS, GCP)'},
                {'text': '<b>Experimental:</b> Single-cell RNA-seq, spatial transcriptomics (10x Visium, MERFISH), CRISPR screening, mouse models, stereotaxic surgery'},
                {'text': '<b>Data:</b> Large-scale dataset integration, pipeline development, statistical analysis'}
            ]
        },
        {
            'title': 'AWARDS & FUNDING',
            'items': [
                {'text': '• NIH K99/R00 Pathway to Independence Award (2023)'},
                {'text': '• Broad Institute NextGen Award (2022)'},
                {'text': '• NSF Graduate Research Fellowship (2016–2021)'}
            ]
        },
        {
            'title': 'OPEN SCIENCE & COMMUNITY',
            'items': [
                {'text': '• All code and datasets publicly available on GitHub and GEO'},
                {'text': '• Contributor to Scanpy open-source project'},
                {'text': '• Organizer, Boston Single-Cell Analysis Meetup'},
                {'text': '• Volunteer, STEM outreach program for underrepresented high school students'}
            ]
        }
    ]
}

# Resume 2: Marcus Johnson - Entry Level
marcus_johnson = {
    'name': 'Marcus Johnson',
    'contact': 'm.johnson@university.edu  |  (555) 123-4567  |  Columbus, OH',
    'sections': [
        {
            'title': 'EDUCATION',
            'items': [
                {
                    'position': 'Master of Science, Biology',
                    'details': 'State University  |  2020 – 2022',
                    'bullets': ['Thesis: "Expression patterns of inflammatory markers in mouse tissue"']
                },
                {
                    'position': 'Bachelor of Science, Biology',
                    'details': 'Community College → State University (Transfer)  |  2016 – 2020',
                    'bullets': []
                }
            ]
        },
        {
            'title': 'EXPERIENCE',
            'items': [
                {
                    'position': 'Research Technician II',
                    'details': 'University Medical Center, Dept of Pathology  |  2022 – Present',
                    'bullets': [
                        'Maintain cell culture facility and support 3 research labs',
                        'Perform routine immunohistochemistry and Western blots',
                        'Assist graduate students with experimental protocols',
                        'Manage lab inventory and ordering'
                    ]
                },
                {
                    'position': 'Graduate Research Assistant',
                    'details': 'State University, Biology Dept  |  2020 – 2022',
                    'bullets': [
                        'Learned basic microscopy and image analysis',
                        'Presented poster at regional conference'
                    ]
                },
                {
                    'position': 'Undergraduate Research Assistant',
                    'details': 'State University  |  2019 – 2020',
                    'bullets': [
                        'Assisted with PCR and gel electrophoresis',
                        'Maintained lab notebooks'
                    ]
                }
            ]
        },
        {
            'title': 'PUBLICATIONS',
            'items': [{
                'publications': [
                    'Smith A, Williams B, <b>Johnson M</b>, et al. (2023) "Inflammatory markers in tissue repair." <i>Journal of Regional Biology</i>. Contributing author.'
                ]
            }]
        },
        {
            'title': 'SKILLS',
            'items': [
                {'text': '<b>Laboratory:</b> Cell culture (mammalian), Western blot, IHC, IF, basic microscopy, PCR, gel electrophoresis'},
                {'text': '<b>Software:</b> Microsoft Office, basic R, ImageJ'},
                {'text': '<b>Other:</b> Lab management, inventory systems'}
            ]
        },
        {
            'title': 'PROFESSIONAL DEVELOPMENT',
            'items': [
                {'text': '• Laboratory Safety Training (Completed)'},
                {'text': '• IACUC Animal Handling Certification (Completed)'},
                {'text': '• Bioinformatics Course - Coursera (In Progress)'}
            ]
        }
    ]
}

if __name__ == '__main__':
    import os
    os.makedirs('sample-resumes', exist_ok=True)
    create_resume_pdf('sample-resumes/sarah-chen.pdf', sarah_chen)
    create_resume_pdf('sample-resumes/marcus-johnson.pdf', marcus_johnson)
    print("\nPDF resumes created successfully!")
