"""
Flask Web Application for Student Introduction Evaluation Tool
Provides a web interface accessible via Chrome browser.
"""

from flask import Flask, render_template, request, jsonify
from student_evaluator.main import StudentEvaluator
import os

app = Flask(__name__)

# Initialize evaluator
# Semantic analysis disabled for deployment (reduces build time from 10min to 2min, memory from 1.5GB to 300MB)
# To enable semantic similarity scoring locally, change to: use_semantic=True
evaluator = StudentEvaluator(use_semantic=False)


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/evaluate', methods=['POST'])
def evaluate():
    """
    Evaluate endpoint - receives transcript and duration, returns scores.
    """
    try:
        data = request.get_json()
        transcript = data.get('transcript', '').strip()
        duration = data.get('duration', 0)
        
        # Validation
        if not transcript:
            return jsonify({
                'success': False,
                'error': 'Please provide a transcript text.'
            }), 400
        
        if duration <= 0:
            return jsonify({
                'success': False,
                'error': 'Please provide a valid duration (in seconds).'
            }), 400
        
        # Run evaluation
        results = evaluator.evaluate(transcript, int(duration))
        
        return jsonify({
            'success': True,
            'results': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/sample', methods=['GET'])
def get_sample():
    """Return sample transcript for testing."""
    sample_transcript = """Hello everyone, myself Muskan, studying in class 8th B section from Christ Public School. 
I am 13 years old. I live with my family. There are 3 people in my family, me, my mother and my father.
One special thing about my family is that they are very kind hearted to everyone and soft spoken. One thing I really enjoy is play, playing cricket and taking wickets.
A fun fact about me is that I see in mirror and talk by myself. One thing people don't know about me is that I once stole a toy from one of my cousin.
My favorite subject is science because it is very interesting. Through science I can explore the whole world and make the discoveries and improve the lives of others. 
Thank you for listening."""
    
    return jsonify({
        'transcript': sample_transcript,
        'duration': 52
    })


if __name__ == '__main__':
    print("🚀 Starting Student Introduction Evaluation Web App...")
    print("📱 Open in Chrome: http://localhost:5000")
    print("Press Ctrl+C to stop the server.")
    app.run(debug=True, host='0.0.0.0', port=5000)
