document.addEventListener('DOMContentLoaded', () => {
    // 1. Timer Logic
    const timerElement = document.getElementById('timer');
    const quizForm = document.getElementById('quiz-form');
    
    if (timerElement && quizForm) {
        let timeLeft = parseInt(timerElement.innerText);
        
        const timerInterval = setInterval(() => {
            timeLeft--;
            timerElement.innerText = timeLeft;
            
            if (timeLeft <= 10) {
                timerElement.classList.add('warning');
            }
            
            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                // Time's up, submit the form automatically
                quizForm.submit();
            }
        }, 1000);
        
        // Clear interval on form submit
        quizForm.addEventListener('submit', () => {
            clearInterval(timerInterval);
        });
    }

    // 2. Confetti Logic
    const resultCard = document.querySelector('.result-card');
    if (resultCard) {
        const passed = resultCard.getAttribute('data-passed') === 'true';
        if (passed && typeof confetti === 'function') {
            // Trigger confetti
            var duration = 3 * 1000;
            var end = Date.now() + duration;

            (function frame() {
                confetti({
                    particleCount: 5,
                    angle: 60,
                    spread: 55,
                    origin: { x: 0 },
                    colors: ['#00E5FF', '#39FF14', '#FFFFFF']
                });
                confetti({
                    particleCount: 5,
                    angle: 120,
                    spread: 55,
                    origin: { x: 1 },
                    colors: ['#00E5FF', '#39FF14', '#FFFFFF']
                });

                if (Date.now() < end) {
                    requestAnimationFrame(frame);
                }
            }());
        }
    }
});
