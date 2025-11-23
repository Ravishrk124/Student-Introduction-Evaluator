# 🚀 QUICK START GUIDE

## Installation (One-Time Setup)

```bash
cd "/Users/ravishkumar/Desktop/Case Study"
pip3 install -r requirements.txt
```

## Run the Tool

### Option 1: Quick Demo (Easiest!)
```bash
python3 demo.py
```

### Option 2: CLI with Custom Transcript
```bash
python3 -m student_evaluator.main \
    --transcript "path/to/your/transcript.txt" \
    --duration 60 \
    --output results.json
```

### Option 3: Use as Python Module
```python
from student_evaluator.main import StudentEvaluator

evaluator = StudentEvaluator()
results = evaluator.evaluate("Your transcript here", duration_seconds=52)
evaluator.print_summary(results)
```

## What You'll Get

1. **Console Output**: Beautiful formatted report
2. **JSON File**: Detailed scores (if --output specified)
3. **Score**: X/100 with letter grade

## Files Overview

- `demo.py` - Quick demo script
- `README.md` - Full documentation
- `CASE_STUDY_SUMMARY.md` - Executive summary
- `student_evaluator/` - Main package
- `requirements.txt` - Dependencies
- `evaluation_report.json` - Sample output

## Expected Score

Sample transcript achieves **85/100 (Grade: A)**

## Need Help?

Check `README.md` for full documentation!
