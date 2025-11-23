#!/usr/bin/env python3
"""
Quick demo script to showcase the evaluation tool.
This can be run without command-line arguments.
"""

from student_evaluator.main import StudentEvaluator


def main():
    """Run a demo evaluation."""
    
    # Sample transcript (from case study)
    sample_transcript = """Hello everyone, myself Muskan, studying in class 8th B section from Christ Public School. 
I am 13 years old. I live with my family. There are 3 people in my family, me, my mother and my father.
One special thing about my family is that they are very kind hearted to everyone and soft spoken. One thing I really enjoy is play, playing cricket and taking wickets.
A fun fact about me is that I see in mirror and talk by myself. One thing people don't know about me is that I once stole a toy from one of my cousin.
My favorite subject is science because it is very interesting. Through science I can explore the whole world and make the discoveries and improve the lives of others. 
Thank you for listening."""
    
    # Duration in seconds
    duration = 52
    
    print("🎓 Student Introduction Evaluation Tool - Demo")
    print("=" * 60)
    print("\n📄 Sample Transcript:")
    print("-" * 60)
    print(sample_transcript)
    print("-" * 60)
    print(f"\n⏱️  Duration: {duration} seconds\n")
    
    # Create evaluator
    evaluator = StudentEvaluator()
    
    # Run evaluation
    results = evaluator.evaluate(sample_transcript, duration)
    
    # Print summary
    evaluator.print_summary(results)
    
    # Show JSON snippet
    print("\n📊 Sample JSON Output (key metrics):")
    print("-" * 60)
    print(f"Final Score: {results['final_score']}/{results['max_score']}")
    print(f"Percentage: {results['percentage']}%")
    print(f"Grade: {results['grade']}")
    print(f"Word Count: {results['metadata']['word_count']}")
    print(f"WPM: {results['metadata']['wpm']}")
    print("-" * 60)


if __name__ == '__main__':
    main()
