document.addEventListener('DOMContentLoaded', function() {
    const germanWordElement = document.getElementById('german-word');
    const greekWordElement = document.getElementById('greek-word');
    const showTranslationButton = document.getElementById('show-translation');
    const nextWordButton = document.getElementById('next-word');

    let currentWord = null;

    function getNewWord() {
        fetch('/get_word')
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    germanWordElement.textContent = data.error;
                } else {
                    currentWord = data;
                    germanWordElement.textContent = currentWord.german;
                    greekWordElement.textContent = currentWord.greek;
                    germanWordElement.style.display = 'block';
                    greekWordElement.style.display = 'none';
                }
            });
    }

    showTranslationButton.addEventListener('click', function() {
        if (currentWord) {
            greekWordElement.style.display = 'block';
        }
    });

    nextWordButton.addEventListener('click', function() {
        getNewWord();
    });

    // Load the first word
    getNewWord();
});
