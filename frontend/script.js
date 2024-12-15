// Fetch relevant elements from the DOM
const inputElement = document.querySelector('input');
const buttonElement = document.querySelector('button');
const resultElement = document.querySelector('.result');

// Sends input to the backend and updates the result in the HTML
async function handleInput() {
    try {
        // Send input data to the backend
        const response = await fetch('http://localhost:5000/validate', {
            method: 'POST', 
            headers: {
              'Content-Type': 'application/json', 
            },
            body: JSON.stringify({ input: inputElement.value }),
        });

        // Handle non-OK responses from the backend
        if (!response.ok) {
            const errorData = await response.json();
            resultElement.innerHTML = `Error: ${errorData.error || 'Something went wrong'}`;
            return;
        }

        // Parse the backend response as JSON
        const data = await response.json();

        // Update the result in the HTML
        resultElement.innerHTML = data.message; 
        
    } catch (error) { 
        console.error(error);
    }
}

// Initiate validation when pressing Enter
inputElement.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        handleInput();
    }
});

// Initiate validation when button is clicked
buttonElement.addEventListener('click', handleInput);
