---
name: resume-scoring
description: Score and evaluate scientific resumes for biomedical research positions. Use this skill when asked to review, screen, evaluate, or score CVs, resumes, or job applications for scientific or research roles. Applies a 100-point rubric covering education, research experience, publications, technical skills, and mission alignment.
---

# Scientific Resume Scoring

This skill evaluates scientific resumes/CVs for biomedical research positions using a structured 100-point rubric.

## When to Use This Skill

Use this skill when you need to:
- Review or screen scientific resumes or CVs
- Score candidates for research positions
- Compare qualifications across multiple applicants
- Generate structured evaluation reports for hiring committees

## Scoring Process

1. **Extract text** from the resume (PDF or other format)
2. **Parse sections**: Education, Experience, Publications, Skills
3. **Score each category** using the rubric below
4. **Document evidence** with quotes from the resume
5. **Calculate total** and assign qualification tier
6. **Generate report** with recommendation

## Scoring Rubric (100 points total)

### 1. Educational Background (25 points max)

| Criteria | Points |
|----------|--------|
| PhD in directly relevant field (biology, biochemistry, biomedical sciences) | 25 |
| PhD in related field (chemistry, physics, computational biology) | 20 |
| MD or MD/PhD | 25 |
| Master's in relevant field | 15 |
| Bachelor's with significant research experience | 10 |
| Degree from recognized research institution | +2 bonus |

### 2. Research Experience (30 points max)

| Criteria | Points |
|----------|--------|
| 5+ years post-doctoral/independent research | 30 |
| 3-5 years post-doctoral research | 25 |
| 1-3 years post-doctoral research | 20 |
| Graduate research only | 15 |
| Industry R&D experience in biomedical field | +5 bonus |

**Experience Quality Modifiers:**
- Led independent research projects: +3
- Secured research funding (grants, fellowships): +3
- Interdisciplinary collaboration demonstrated: +2

### 3. Publication Record (20 points max)

| Criteria | Points |
|----------|--------|
| 10+ peer-reviewed publications | 20 |
| 5-9 peer-reviewed publications | 15 |
| 2-4 peer-reviewed publications | 10 |
| 1 peer-reviewed publication | 5 |
| First/corresponding author on high-impact papers | +3 bonus |
| Preprints demonstrating current work | +1 bonus |

### 4. Technical Skills Alignment (15 points max)

| Alignment | Points |
|-----------|--------|
| Strong match (4+ required techniques/methods) | 15 |
| Good match (2-3 required techniques/methods) | 10 |
| Partial match (1 required technique/method) | 5 |
| Transferable skills only | 3 |

**High-Value Skills for Biomedical Research:**
- CRISPR/gene editing technologies
- Single-cell sequencing/analysis
- Computational biology/bioinformatics
- Microscopy (confocal, electron, super-resolution)
- Protein biochemistry
- Animal model experience
- Clinical research experience

### 5. Mission Alignment & Collaboration (10 points max)

| Criteria | Points |
|----------|--------|
| Open science contributions (open-source tools, public datasets) | 3 |
| Mentorship/teaching experience | 3 |
| Collaborative research (multi-institutional projects) | 2 |
| Community engagement (science communication, outreach) | 2 |

## Qualification Tiers

| Score Range | Tier | Action |
|-------------|------|--------|
| 80-100+ | **Highly Qualified** | Priority review, fast-track |
| 65-79 | **Qualified** | Standard review process |
| 50-64 | **Potentially Qualified** | Review if pool is limited |
| Below 50 | **Not Qualified** | Archive for future openings |

## Output Format

For each resume, produce a structured evaluation:

```markdown
## Candidate Summary
- **Name**: [extracted]
- **Current Role**: [extracted]  
- **Education**: [highest degree, institution, field]
- **Years of Experience**: [calculated]

## Scores

### Educational Background: X/25
- [Score justification]
- Evidence: "[quote from resume]"

### Research Experience: X/30
- [Score justification]
- Evidence: "[quote from resume]"

### Publication Record: X/20
- [Score justification]
- Evidence: "[quote from resume]"

### Technical Skills: X/15
- [Score justification]
- Evidence: "[quote from resume]"

### Mission Alignment: X/10
- [Score justification]
- Evidence: "[quote from resume]"

## Overall Assessment
- **Total Score**: X/100
- **Qualification Tier**: [tier]
- **Key Strengths**: [2-3 points]
- **Concerns**: [if any]

## Recommendation
[Brief recommendation for hiring committee]
```

## Red Flags to Note

- Gaps in timeline without explanation
- Claims that cannot be verified
- Mismatch between stated skills and publication record
- No evidence of collaboration or teamwork
- Retracted publications

## Bias Mitigation

Before finalizing, verify:
- Scoring based only on stated qualifications
- International credentials evaluated fairly
- Non-traditional career paths considered
- Part-time or career-break periods not penalized unfairly
- Scores consistent with similar candidates
