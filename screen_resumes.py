#!/usr/bin/env python3
"""
Resume Screening Demo Script

This script demonstrates how to:
1. Extract text from PDF resumes
2. Send to Claude API for scoring
3. Generate structured evaluation reports

Usage:
    python screen_resumes.py                    # Process all PDFs in sample-resumes/
    python screen_resumes.py resume.pdf         # Process a single PDF
    python screen_resumes.py --help             # Show help

Requirements:
    pip install pdfplumber anthropic

Environment:
    Set ANTHROPIC_API_KEY environment variable
"""

import pdfplumber
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


def extract_resume_text(pdf_path: str) -> str:
    """Extract text content from a PDF resume."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def load_scoring_rubric(rubric_path: str = "skills/resume-scoring.md") -> str:
    """Load the scoring rubric from markdown file."""
    with open(rubric_path, 'r') as f:
        return f.read()


def create_scoring_prompt(resume_text: str, rubric: str) -> str:
    """Create the prompt for LLM scoring."""
    return f"""You are a scientific resume screening agent for a biomedical research organization focused on unlocking the fundamentals of biology and building an open, inclusive future for science.

Review the following resume and score it according to the rubric provided.

## SCORING RUBRIC
{rubric}

## RESUME CONTENT
{resume_text}

## YOUR TASK
Score this resume following the rubric exactly. For each category:
1. State the score (X/Y points)
2. Quote the specific evidence from the resume that justifies the score
3. Note any bonus points applied

Then provide:
- Total score (sum of all categories)
- Qualification tier (based on the tier table in the rubric)
- 2-3 key strengths
- Any concerns or gaps
- Brief recommendation for the hiring committee

Format your response as a clear, structured evaluation report.
"""


def score_resume_with_claude(prompt: str, api_key: str) -> str:
    """Send the prompt to Claude API and get the evaluation."""
    client = anthropic.Anthropic(api_key=api_key)
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text


def process_resume(pdf_path: str, output_dir: str = "evaluations", 
                   api_key: str = None, rubric_path: str = "skills/resume-scoring.md") -> dict:
    """Process a single resume and return evaluation."""
    
    print(f"\n{'='*60}")
    print(f"Processing: {pdf_path}")
    print('='*60)
    
    # Extract text from PDF
    print("  [1/4] Extracting text from PDF...")
    resume_text = extract_resume_text(pdf_path)
    print(f"        Extracted {len(resume_text)} characters")
    
    # Load rubric
    print("  [2/4] Loading scoring rubric...")
    rubric = load_scoring_rubric(rubric_path)
    
    # Create the prompt
    print("  [3/4] Creating evaluation prompt...")
    prompt = create_scoring_prompt(resume_text, rubric)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    basename = Path(pdf_path).stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save extracted text for reference
    extracted_file = f"{output_dir}/{basename}_extracted.txt"
    with open(extracted_file, 'w') as f:
        f.write(resume_text)
    
    # Score with Claude if API key provided
    if api_key:
        print("  [4/4] Sending to Claude for evaluation...")
        try:
            evaluation = score_resume_with_claude(prompt, api_key)
            
            # Save the evaluation
            eval_file = f"{output_dir}/{basename}_evaluation_{timestamp}.md"
            with open(eval_file, 'w') as f:
                f.write(f"# Resume Evaluation: {basename}\n")
                f.write(f"**Evaluated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Source:** {pdf_path}\n\n")
                f.write("---\n\n")
                f.write(evaluation)
            
            print(f"\n  ✓ Evaluation saved to: {eval_file}")
            
            return {
                "pdf_path": pdf_path,
                "status": "completed",
                "evaluation_file": eval_file,
                "extracted_text_file": extracted_file,
                "evaluation": evaluation
            }
            
        except anthropic.APIError as e:
            print(f"\n  ✗ API Error: {e}")
            return {
                "pdf_path": pdf_path,
                "status": "error",
                "error": str(e)
            }
    else:
        # No API key - just save the prompt for manual use
        prompt_file = f"{output_dir}/{basename}_prompt.txt"
        with open(prompt_file, 'w') as f:
            f.write(prompt)
        
        print("  [4/4] No API key provided - saving prompt for manual use")
        print(f"        Prompt saved to: {prompt_file}")
        
        return {
            "pdf_path": pdf_path,
            "status": "prompt_only",
            "prompt_file": prompt_file,
            "extracted_text_file": extracted_file
        }


def batch_process_resumes(resume_dir: str = "sample-resumes", 
                          output_dir: str = "evaluations",
                          api_key: str = None,
                          rubric_path: str = "skills/resume-scoring.md") -> list:
    """Process all PDF resumes in a directory."""
    
    pdf_files = sorted(Path(resume_dir).glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {resume_dir}/")
        return []
    
    print(f"\nFound {len(pdf_files)} PDF resume(s) to process")
    
    results = []
    for pdf_path in pdf_files:
        result = process_resume(
            str(pdf_path), 
            output_dir=output_dir,
            api_key=api_key,
            rubric_path=rubric_path
        )
        results.append(result)
    
    return results


def print_summary(results: list):
    """Print a summary of all processed resumes."""
    print("\n")
    print("=" * 60)
    print("PROCESSING SUMMARY")
    print("=" * 60)
    
    completed = [r for r in results if r.get("status") == "completed"]
    prompt_only = [r for r in results if r.get("status") == "prompt_only"]
    errors = [r for r in results if r.get("status") == "error"]
    
    print(f"\nTotal processed: {len(results)}")
    print(f"  ✓ Evaluated:    {len(completed)}")
    print(f"  ○ Prompt only:  {len(prompt_only)}")
    print(f"  ✗ Errors:       {len(errors)}")
    
    if completed:
        print("\n" + "-" * 60)
        print("COMPLETED EVALUATIONS:")
        print("-" * 60)
        for r in completed:
            print(f"\n  {Path(r['pdf_path']).name}")
            print(f"  → {r['evaluation_file']}")
    
    if prompt_only:
        print("\n" + "-" * 60)
        print("PROMPTS SAVED (no API key):")
        print("-" * 60)
        print("\nTo evaluate these resumes, either:")
        print("  1. Set ANTHROPIC_API_KEY and re-run")
        print("  2. Copy prompt contents to claude.ai manually")
        for r in prompt_only:
            print(f"\n  {Path(r['pdf_path']).name}")
            print(f"  → {r['prompt_file']}")
    
    if errors:
        print("\n" + "-" * 60)
        print("ERRORS:")
        print("-" * 60)
        for r in errors:
            print(f"\n  {Path(r['pdf_path']).name}")
            print(f"  → {r['error']}")


def main():
    parser = argparse.ArgumentParser(
        description="Screen scientific resumes using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python screen_resumes.py                          # Process all PDFs in sample-resumes/
  python screen_resumes.py my_resume.pdf            # Process a single resume
  python screen_resumes.py --dir applications/      # Process a different directory
  
Environment:
  ANTHROPIC_API_KEY    Your Claude API key (required for automated scoring)
  
Without an API key, the script extracts text and generates prompts you can 
paste into claude.ai manually.
        """
    )
    
    parser.add_argument(
        "resume", 
        nargs="?", 
        help="Path to a single PDF resume (optional)"
    )
    parser.add_argument(
        "--dir", "-d",
        default="sample-resumes",
        help="Directory containing PDF resumes (default: sample-resumes/)"
    )
    parser.add_argument(
        "--output", "-o",
        default="evaluations",
        help="Output directory for evaluations (default: evaluations/)"
    )
    parser.add_argument(
        "--rubric", "-r",
        default="skills/resume-scoring.md",
        help="Path to scoring rubric (default: skills/resume-scoring.md)"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="Anthropic API key (or set ANTHROPIC_API_KEY env var)"
    )
    
    args = parser.parse_args()
    
    # Get API key from args or environment
    api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY")
    
    # Check for anthropic library
    if api_key and not HAS_ANTHROPIC:
        print("Error: anthropic library not installed")
        print("Run: pip install anthropic")
        sys.exit(1)
    
    print("=" * 60)
    print("SCIENTIFIC RESUME SCREENING SYSTEM")
    print("=" * 60)
    print(f"Rubric: {args.rubric}")
    print(f"Output: {args.output}/")
    print(f"API:    {'Claude API (automated)' if api_key else 'None (prompt-only mode)'}")
    
    # Process single resume or batch
    if args.resume:
        if not os.path.exists(args.resume):
            print(f"\nError: File not found: {args.resume}")
            sys.exit(1)
        results = [process_resume(
            args.resume,
            output_dir=args.output,
            api_key=api_key,
            rubric_path=args.rubric
        )]
    else:
        if not os.path.exists(args.dir):
            print(f"\nError: Directory not found: {args.dir}")
            sys.exit(1)
        results = batch_process_resumes(
            resume_dir=args.dir,
            output_dir=args.output,
            api_key=api_key,
            rubric_path=args.rubric
        )
    
    # Print summary
    print_summary(results)
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()

