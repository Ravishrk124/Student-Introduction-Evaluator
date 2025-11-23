// Student Introduction Evaluator - Frontend JavaScript

// Global variable to store latest results
let latestResults = null;

/**
 * Handle file upload
 */
function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    // Update file name display
    document.getElementById('file-name').textContent = file.name;

    // Read file content
    const reader = new FileReader();
    reader.onload = function (e) {
        document.getElementById('transcript').value = e.target.result;
        showMessage(`File "${file.name}" loaded successfully!`, 'success');
    };
    reader.onerror = function () {
        showError('Failed to read file. Please try again.');
    };
    reader.readAsText(file);
}

/**
 * Clear all inputs
 */
function clearAll() {
    document.getElementById('transcript').value = '';
    document.getElementById('duration').value = '52';
    document.getElementById('file-upload').value = '';
    document.getElementById('file-name').textContent = 'Choose a file or drag & drop';
    hideResults();
    hideError();
}

/**
 * Load sample transcript for testing
 */
function loadSample() {
    fetch('/sample')
        .then(response => response.json())
        .then(data => {
            document.getElementById('transcript').value = data.transcript;
            document.getElementById('duration').value = data.duration;
            // showMessage('Sample transcript loaded!', 'success');
        })
        .catch(error => {
            showError('Failed to load sample: ' + error.message);
        });
}

/**
 * Evaluate the transcript
 */
function evaluateTranscript() {
    const transcript = document.getElementById('transcript').value.trim();
    const duration = parseInt(document.getElementById('duration').value);

    // Validation
    if (!transcript) {
        showError('Please enter a transcript text.');
        return;
    }

    if (!duration || duration <= 0) {
        showError('Please enter a valid duration in seconds.');
        return;
    }

    // Hide previous results and errors
    hideResults();
    hideError();
    showLoading();

    // Make API call
    fetch('/evaluate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            transcript: transcript,
            duration: duration
        })
    })
        .then(response => response.json())
        .then(data => {
            hideLoading();

            if (data.success) {
                latestResults = data.results; // Store for export
                displayResults(data.results);
            } else {
                showError(data.error || 'Evaluation failed.');
            }
        })
        .catch(error => {
            hideLoading();
            showError('Network error: ' + error.message);
        });
}

/**
 * Display evaluation results
 */
function displayResults(results) {
    // Show results section
    document.getElementById('results-section').style.display = 'block';

    // Scroll to results
    document.getElementById('results-section').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });

    // Final Score & Grade
    document.getElementById('final-score').textContent =
        `${results.final_score}/${results.max_score}`;
    document.getElementById('grade-badge').textContent = results.grade;

    // Metadata
    document.getElementById('word-count').textContent = results.metadata.word_count;
    document.getElementById('wpm').textContent = results.metadata.wpm;
    document.getElementById('sentence-count').textContent = results.metadata.sentence_count;

    // Content & Structure
    const content = results.scores.content_and_structure;
    updateScoreCard('content', content.total, content.max, content.percentage);
    document.getElementById('salutation-score').textContent =
        `${content.salutation_score}/${content.details.salutation.max_score}`;
    document.getElementById('keywords-score').textContent =
        `${content.keywords_score}/${content.details.keywords.max_score}`;
    document.getElementById('flow-score').textContent =
        `${content.flow_score}/${content.details.flow.max_score}`;

    // Speech Rate
    const speech = results.scores.speech_rate;
    updateScoreCard('speech', speech.score, speech.max);
    document.getElementById('speech-label').textContent =
        `${speech.wpm} WPM (${speech.label})`;

    // Language & Grammar
    const grammar = results.scores.language_and_grammar;
    updateScoreCard('grammar', grammar.total, grammar.max, grammar.percentage);
    document.getElementById('grammar-subscore').textContent =
        `${grammar.grammar_score}/${grammar.details.grammar.max_score}`;
    document.getElementById('vocab-score').textContent =
        `${grammar.vocabulary_score}/${grammar.details.vocabulary.max_score}`;

    // Clarity
    const clarity = results.scores.clarity;
    updateScoreCard('clarity', clarity.score, clarity.max);
    document.getElementById('filler-info').textContent =
        `${clarity.filler_count} fillers (${clarity.filler_rate}%)`;

    // Engagement
    const engagement = results.scores.engagement;
    updateScoreCard('engagement', engagement.score, engagement.max);
    document.getElementById('sentiment-label').textContent = engagement.interpretation;
}

/**
 * Update a score card with values and progress bar
 */
function updateScoreCard(prefix, score, max, percentage = null) {
    document.getElementById(`${prefix}-score`).textContent = `${score}/${max}`;

    if (percentage !== null) {
        document.getElementById(`${prefix}-percent`).textContent = `${percentage}%`;
    }

    // Update progress bar
    const fillElement = document.getElementById(`${prefix}-fill`);
    const percent = (score / max) * 100;
    fillElement.style.width = `${percent}%`;

    // Color based on percentage
    if (percent >= 80) {
        fillElement.style.background = 'linear-gradient(90deg, #10b981, #34d399)';
    } else if (percent >= 60) {
        fillElement.style.background = 'linear-gradient(90deg, #f59e0b, #fbbf24)';
    } else {
        fillElement.style.background = 'linear-gradient(90deg, #ef4444, #f87171)';
    }
}

/**
 * Show loading spinner
 */
function showLoading() {
    document.getElementById('loading').style.display = 'block';
}

/**
 * Hide loading spinner
 */
function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

/**
 * Show error message
 */
function showError(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

/**
 * Hide error message
 */
function hideError() {
    document.getElementById('error-message').style.display = 'none';
}

/**
 * Hide results section
 */
function hideResults() {
    document.getElementById('results-section').style.display = 'none';
}

/**
 * Show temporary message
 */
function showMessage(message, type = 'info') {
    // Simple alert for now - could be enhanced with toast notifications
    console.log(`[${type}] ${message}`);
}

// Add keyboard shortcut: Ctrl+Enter to evaluate
document.getElementById('transcript')?.addEventListener('keydown', function (e) {
    if (e.ctrlKey && e.key === 'Enter') {
        evaluateTranscript();
    }
});
