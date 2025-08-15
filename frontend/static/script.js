document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const resultsDiv = document.getElementById('results');
    const severityResultDiv = document.getElementById('severityResult');
    let chart = null;

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Collect form data
        const formData = {
            AGE: parseInt(document.getElementById('age').value),
            PackHistory: parseInt(document.getElementById('packHistory').value),
            MWT1Best: parseInt(document.getElementById('mwt1Best').value),
            FEV1: parseFloat(document.getElementById('fev1').value),
            FEV1PRED: parseInt(document.getElementById('fev1pred').value),
            FVC: parseFloat(document.getElementById('fvc').value),
            FVCPRED: parseInt(document.getElementById('fvcpred').value),
            CAT: parseInt(document.getElementById('cat').value),
            HAD: parseInt(document.getElementById('had').value),
            SGRQ: parseInt(document.getElementById('sgrq').value),
            AGEquartiles: Math.ceil(parseInt(document.getElementById('age').value) / 25), // Simplified quartile calculation
            gender: parseInt(document.getElementById('gender').value),
            smoking: 2, // Default value as it's not in the form
            Diabetes: document.getElementById('diabetes').checked ? 1 : 0,
            muscular: document.getElementById('muscular').checked ? 1 : 0,
            hypertension: document.getElementById('hypertension').checked ? 1 : 0,
            AtrialFib: document.getElementById('atrialFib').checked ? 1 : 0,
            IHD: document.getElementById('ihd').checked ? 1 : 0
        };

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error:', error);
            if (error.name === 'SyntaxError') {
                window.location.href = '/login';
                return;
            }
            alert('Error: ' + error.message);
        }
    });

    function displayResults(data) {
        // Display severity
        severityResultDiv.innerHTML = `<h3>Predicted COPD Severity: ${data.severity}</h3>`;
        
        // Display probability chart
        const ctx = document.getElementById('probabilityChart');
        
        // Destroy existing chart if it exists
        if (chart) {
            chart.destroy();
        }

        // Create new chart
        chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(data.probabilities),
                datasets: [{
                    label: 'Probability',
                    data: Object.values(data.probabilities),
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1,
                        title: {
                            display: true,
                            text: 'Probability'
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'COPD Severity Probabilities'
                    }
                }
            }
        });

        // Show results
        resultsDiv.classList.remove('hidden');
    }
}); 