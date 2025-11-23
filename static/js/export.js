// Export and Share Functions

/**
 * Download results as JSON
 */
function downloadJSON() {
    if (!latestResults) {
        alert('No results to download. Please evaluate a transcript first.');
        return;
    }

    const dataStr = JSON.stringify(latestResults, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });

    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `evaluation_results_${Date.now()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    showNotification('JSON downloaded successfully! 💾');
}

/**
 * Export results as PDF
 */
function exportPDF() {
    if (!latestResults) {
        alert('No results to export. Please evaluate a transcript first.');
        return;
    }

    // Create printable content
    const printWindow = window.open('', '_blank');
    const html = generatePDFContent(latestResults);

    printWindow.document.write(html);
    printWindow.document.close();

    // Wait for content to load then trigger print
    setTimeout(() => {
        printWindow.print();
        showNotification('Print dialog opened! Save as PDF 📄');
    }, 500);
}

/**
 * Generate HTML content for PDF
 */
function generatePDFContent(results) {
    return `
<!DOCTYPE html>
<html>
<head>
    <title>Evaluation Report - ${results.grade}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            color: #333;
        }
        h1 {
            color: #6366f1;
            border-bottom: 3px solid #6366f1;
            padding-bottom: 10px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .score-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin: 20px 0;
        }
        .final-score {
            font-size: 48px;
            font-weight: bold;
        }
        .grade {
            font-size: 36px;
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 8px;
            display: inline-block;
            margin-top: 10px;
        }
        .metadata {
            background: #f9fafb;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .criterion {
            margin: 20px 0;
            padding: 15px;
            border-left: 4px solid #6366f1;
            background: #f9fafb;
        }
        .criterion h3 {
            margin-top: 0;
            color: #6366f1;
        }
        .score-bar {
            background: #e5e7eb;
            height: 20px;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }
        .score-fill {
            background: linear-gradient(90deg, #6366f1, #8b5cf6);
            height: 100%;
            border-radius: 10px;
        }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            text-align: center;
            font-size: 12px;
            color: #6b7280;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎓 Student Introduction Evaluation Report</h1>
        <p>Generated on ${new Date().toLocaleString()}</p>
    </div>
    
    <div class="score-box">
        <div class="final-score">${results.final_score}/100</div>
        <div class="grade">Grade: ${results.grade}</div>
    </div>
    
    <div class="metadata">
        <h3>📊 Metadata</h3>
        <p><strong>Word Count:</strong> ${results.metadata.word_count}</p>
        <p><strong>Sentence Count:</strong> ${results.metadata.sentence_count}</p>
        <p><strong>Duration:</strong> ${results.metadata.duration_seconds} seconds</p>
        <p><strong>Speech Rate:</strong> ${results.metadata.wpm} WPM</p>
    </div>
    
    <h2>Detailed Scores</h2>
    
    <div class="criterion">
        <h3>📝 Content & Structure</h3>
        <div class="score-bar">
            <div class="score-fill" style="width: ${(results.scores.content_and_structure.total / results.scores.content_and_structure.max * 100)}%"></div>
        </div>
        <p><strong>Score:</strong> ${results.scores.content_and_structure.total}/${results.scores.content_and_structure.max} (${results.scores.content_and_structure.percentage}%)</p>
        <p>• Salutation: ${results.scores.content_and_structure.salutation_score}/5</p>
        <p>• Keywords: ${results.scores.content_and_structure.keywords_score}/30</p>
        <p>• Flow: ${results.scores.content_and_structure.flow_score}/5</p>
    </div>
    
    <div class="criterion">
        <h3>⚡ Speech Rate</h3>
        <div class="score-bar">
            <div class="score-fill" style="width: ${(results.scores.speech_rate.score / results.scores.speech_rate.max * 100)}%"></div>
        </div>
        <p><strong>Score:</strong> ${results.scores.speech_rate.score}/${results.scores.speech_rate.max}</p>
        <p>• ${results.scores.speech_rate.wpm} WPM (${results.scores.speech_rate.label})</p>
    </div>
    
    <div class="criterion">
        <h3>📖 Language & Grammar</h3>
        <div class="score-bar">
            <div class="score-fill" style="width: ${(results.scores.language_and_grammar.total / results.scores.language_and_grammar.max * 100)}%"></div>
        </div>
        <p><strong>Score:</strong> ${results.scores.language_and_grammar.total}/${results.scores.language_and_grammar.max} (${results.scores.language_and_grammar.percentage}%)</p>
        <p>• Grammar: ${results.scores.language_and_grammar.grammar_score}/10</p>
        <p>• Vocabulary: ${results.scores.language_and_grammar.vocabulary_score}/10</p>
    </div>
    
    <div class="criterion">
        <h3>✨ Clarity</h3>
        <div class="score-bar">
            <div class="score-fill" style="width: ${(results.scores.clarity.score / results.scores.clarity.max * 100)}%"></div>
        </div>
        <p><strong>Score:</strong> ${results.scores.clarity.score}/${results.scores.clarity.max}</p>
        <p>• Filler Words: ${results.scores.clarity.filler_count} (${results.scores.clarity.filler_rate}%)</p>
    </div>
    
    <div class="criterion">
        <h3>💫 Engagement</h3>
        <div class="score-bar">
            <div class="score-fill" style="width: ${(results.scores.engagement.score / results.scores.engagement.max * 100)}%"></div>
        </div>
        <p><strong>Score:</strong> ${results.scores.engagement.score}/${results.scores.engagement.max}</p>
        <p>• ${results.scores.engagement.interpretation}</p>
    </div>
    
    <div class="footer">
        <p>Generated by Student Introduction Evaluator v2.0</p>
        <p>Powered by AI • sentence-transformers • VADER • LanguageTool</p>
    </div>
</body>
</html>
    `;
}

/**
 * Share results via link
 */
function shareResults() {
    if (!latestResults) {
        alert('No results to share. Please evaluate a transcript first.');
        return;
    }

    // Create shareable summary
    const summary = `
🎓 Student Introduction Evaluation Results

📊 Final Score: ${latestResults.final_score}/100 (Grade: ${latestResults.grade})

Breakdown:
• Content & Structure: ${latestResults.scores.content_and_structure.total}/40
• Speech Rate: ${latestResults.scores.speech_rate.score}/10
• Language & Grammar: ${latestResults.scores.language_and_grammar.total}/20
• Clarity: ${latestResults.scores.clarity.score}/15
• Engagement: ${latestResults.scores.engagement.score}/15

📝 Word Count: ${latestResults.metadata.word_count}
⚡ WPM: ${latestResults.metadata.wpm}
    `.trim();

    // Copy to clipboard
    navigator.clipboard.writeText(summary).then(() => {
        showNotification('Results copied to clipboard! Ready to share 🔗');
    }).catch(() => {
        // Fallback: show in alert
        alert(summary);
        showNotification('Results displayed. Copy manually to share.');
    });
}

/**
 * Evaluate another transcript
 */
function evaluateAgain() {
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Clear results but keep transcript for re-evaluation
    hideResults();

    // Focus on transcript
    document.getElementById('transcript').focus();
}

/**
 * Show notification message
 */
function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease;
        font-weight: 600;
    `;

    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
