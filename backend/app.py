from flask import Flask, request, jsonify
from flask_cors import CORS
import string
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch database credentials from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

# Funktion för att ansluta till databasen
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,
        port=DB_PORT,
        cursor_factory=RealDictCursor
    )


app = Flask(__name__) #Skapa en server
CORS(app) #Tillåter att alla portar kan kommunicera med backend

def validate_input(data):

    banned_words = {"password", "admin", "12345678", "letmein", "welcome"}
    special_characters = string.punctuation

    validations = {
        "Password length": 8 <= len(data) <= 20,
        "Uppercase character": any(char.isupper() for char in data),
        "Lowercase character": any(char.islower() for char in data),
        "Number character": any(char.isdigit() for char in data),
        "Special character": any(char in special_characters for char in data),
        "No whitespace": not any(char.isspace() for char in data),
        "No banned words": data.lower() not in banned_words,
    }

   
    try:
        # Anslut till databasen och kontrollera duplicat
        conn = get_db_connection() # Öppnar till databasen

        with conn.cursor() as cursor: #Automatisk stägning av cursorn
            # Kontrollera om strängen redan finns
            cursor.execute("SELECT 1 FROM validated_inputs WHERE input_text = %s", (data,)) #SQL fråga, retunerar 1 om det finns
            is_duplicate = cursor.fetchone() is not None
            validations["No duplicates"] = not is_duplicate

            # Om strängen är validerad, spara i databasen
            if all(validations.values()):
                cursor.execute("INSERT INTO validated_inputs (input_text) VALUES (%s)", (data,))
                conn.commit()

        conn.close()

    except Exception as e:
        validations["Database error"] = False
        print(f"Database error: {e}")


    # Store failed keys in failed
    failed = [key for key, value in validations.items() if not value]

    return {
        "success": all(validations.values()),
        "failed": failed,
    }

#Funktionen validate() kommer att köras när /validate anropas med en POST-förfrågan

@app.route('/validate', methods=['POST'])
def validate():
    try:
        #Ändrar imput från json format till sträng
        input_data = request.json.get('input', '')

        #TODO funkar ej:
        if not input_data:
            return jsonify({"error": "Input data is missing"}), 400

        # Får tillbaka om succsess och vilka som är failed
        validation_result = validate_input(input_data)

        if validation_result["success"]:
            return jsonify({
                "message": f"Validation passed"
            }) #Konverterar till JSON format
        else:
            return jsonify({
                "message": f"Validation failed! Check if fulfilled: <br> {'<br>'.join(validation_result['failed'])}",
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)


