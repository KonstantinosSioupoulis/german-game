document.addEventListener('DOMContentLoaded', function() {
    const germanWordElement = document.getElementById('german-word');
    const greekWordElement = document.getElementById('greek-word');
    const showTranslationButton = document.getElementById('show-translation');
    const prevWordButton = document.getElementById('prev-word');
    const nextWordButton = document.getElementById('next-word');
    const toggleModeButton = document.getElementById('toggle-mode');
    const modeTextElement = document.getElementById('mode-text');
    const serialSearchContainer = document.getElementById('serial-search');
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');

    let currentWord = null;
    let gameMode = 'random';
    let serialIndex = 0;
    let wordCount = 0;

    function getWordCount() {
        fetch('/get_word_count')
            .then(response => response.json())
            .then(data => {
                wordCount = data.count;
            });
    }

    function getNewWord(getPrev = false) {
        let url = '/get_word';
        if (gameMode === 'serial') {
            if (getPrev) {
                // Decrement index to get the previous word
                serialIndex = (serialIndex - 2 + wordCount) % wordCount;
            }
            url += `?mode=serial&index=${serialIndex}`;
            // Increment for the next word
            serialIndex = (serialIndex + 1) % wordCount;
        }

        fetch(url)
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

    prevWordButton.addEventListener('click', function() {
        getNewWord(true);
    });

    nextWordButton.addEventListener('click', function() {
        getNewWord();
    });

    toggleModeButton.addEventListener('click', function() {
        if (gameMode === 'random') {
            gameMode = 'serial';
            modeTextElement.textContent = 'Serial';
            serialSearchContainer.style.display = 'flex'; // Use flex to align items
            serialIndex = 0; // Reset index when switching to serial
        } else {
            gameMode = 'random';
            modeTextElement.textContent = 'Random';
            serialSearchContainer.style.display = 'none';
        }
        getNewWord(); // Get a new word in the new mode
    });

    searchButton.addEventListener('click', function() {
        const searchTerm = searchInput.value;
        if (searchTerm) {
            fetch(`/find_word?term=${encodeURIComponent(searchTerm)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.index !== -1) {
                        serialIndex = data.index;
                        getNewWord();
                    } else {
                        alert('Word not found!');
                    }
                });
        }
    });

    // Load the word count and then the first word
    getWordCount();
    getNewWord();
});
