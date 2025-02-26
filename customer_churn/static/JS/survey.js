// survey.js
document.addEventListener('DOMContentLoaded', () => {
    fetch('/static/Asset/survey_quiz.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            getSurveyQA(data);
        })
        .catch(error => console.error('Error loading the survey data:', error));
});

const getSurveyQA = (data) => {
    const surveyContainer = document.querySelector('.qa-card'); // Use the existing section or a new container
    const survey = data['survey'];

    // Clear existing content (optional, remove if you want to append)
    surveyContainer.innerHTML = '';

    // Loop through each question in the survey
    survey.forEach((item, index) => {
        // Create a new section for each question
        const qaCard = document.createElement('section');
        qaCard.className = 'qa-card';

        // Add the question
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question';
        questionDiv.textContent = `Q${index + 1}: ${item.question}`; // e.g., "Q1: How satisfied..."
        qaCard.appendChild(questionDiv);

        // Add the answers container
        const answersCard = document.createElement('div');
        answersCard.className = 'answers-card';

        // Loop through answers and create radio buttons
        item.answers.forEach((answer, answerIndex) => {
            const answerDiv = document.createElement('div');
            answerDiv.className = 'answer';

            const input = document.createElement('input');
            input.type = 'radio';
            input.name = `reason_q${index}`; // Unique name per question
            input.id = `q${index}_a${answerIndex}`; // Unique ID
            input.value = answer;

            const label = document.createElement('label');
            label.htmlFor = `q${index}_a${answerIndex}`; // Matches input ID
            label.className = 'dt_value';
            label.textContent = answer;

            answerDiv.appendChild(input);
            answerDiv.appendChild(label);
            answersCard.appendChild(answerDiv);
        });

        qaCard.appendChild(answersCard);
        surveyContainer.parentNode.insertBefore(qaCard, surveyContainer.nextSibling);
    });
};