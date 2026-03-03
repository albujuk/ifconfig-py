document.querySelectorAll('.command-block').forEach(block => {
    block.addEventListener('click', function () {
        const textToCopy = this.getAttribute('data-copy');
        const feedback = this.querySelector('.copy-feedback');

        navigator.clipboard.writeText(textToCopy).then(() => {
            feedback.classList.add('show');
            setTimeout(() => {
                feedback.classList.remove('show');
            }, 1500);
        }).catch(err => {
            console.error('Failed to copy:', err);
        });
    });
});

document.querySelectorAll('.command-block').forEach(block => {
    block.addEventListener('click', function () {
        const textToCopy = this.getAttribute('data-copy');
        const feedback = this.querySelector('.copy-feedback');

        navigator.clipboard.writeText(textToCopy).then(() => {
            feedback.classList.add('show');
            setTimeout(() => {
                feedback.classList.remove('show');
            }, 1500);
        }).catch(err => {
            console.error('Failed to copy:', err);
        });
    });
});

document.querySelectorAll('.info-value').forEach(value => {
    value.style.cursor = 'pointer';
    value.addEventListener('click', function () {
        const textToCopy = this.textContent.trim();

        navigator.clipboard.writeText(textToCopy).then(() => {
            const originalColor = this.style.color;
            this.style.color = '#98c379';
            setTimeout(() => {
                this.style.color = originalColor;
            }, 300);
        }).catch(err => {
            console.error('Failed to copy:', err);
        });
    });
});