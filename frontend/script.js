// Sätta variabler
const inputElement = document.querySelector('input');
const buttonElement = document.querySelector('button');
const resultElement = document.querySelector('.result');

//Skickar till backend och tillbaka till html
async function handleInput() { // Funktionen kan pausa med "await" utan att blockera resten av programmet
    try {
        const response = await fetch('http://localhost:5000/validate', {
            method: 'POST', 
            headers: {
              'Content-Type': 'application/json', 
            },
            body: JSON.stringify({ input: inputElement.value }), 
        });  //All den här informationen skickas till backend och vi får tillbaka det i response

        if (!response.ok) {
            const errorData = await response.json();
            resultElement.innerHTML = `Error: ${errorData.error || 'Something went wrong'}`;
            return;
        }

        const data = await response.json(); // Gör respons (i json format) till en javascript objekt

        resultElement.innerHTML = data.message; //Sparar i resultElement        
        
    } catch (error) { 
        console.error(error);
    }
}

//Kör funktionen om man trycker enter
inputElement.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        handleInput();
    }
});

//Kör funktionen om man trycker på knappen
buttonElement.addEventListener('click', handleInput);