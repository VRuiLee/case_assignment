# Case Assignment

## How to run the application locally
- Clone the repository into your preferred directory: `git clone <repository-url>`
- Create a `.env` file in the root folder containing:
    - `DB_HOST = "mydb.xxxxxx.region.rds.amazonaws.com"`
    - `DB_USER = "your_username"`
    - `DB_PASSWORD = "your_password"`
    - `DB_NAME = "your_database_name"`
    - `DB_PORT = "5432"` (or the port configured for your PostgreSQL instance)
- Install the required dependencies by executing: `pip install -r requirements.txt`
- Start the application: `python app.py`
- Open your browser and navigate to `http://localhost:5000` (or the configured port for your application).

---

## The validation rules and their implementation
The application enforces the following validation rules:
1. **Password Length:** Must be between 8 and 20 characters.
2. **Uppercase Character:** Must include at least one uppercase letter.
3. **Lowercase Character:** Must include at least one lowercase letter.
4. **Number Character:** Must include at least one digit.
5. **Special Character:** Must include at least one special character (e.g., `@`, `#`, `$`).
6. **No Whitespace:** Passwords cannot contain any spaces.
7. **Banned Words:** Passwords cannot be any of the following:
   - `password`, `admin`, `12345678`, `letmein`, `welcome`.
8. **No Duplicates:** Passwords must not already exist in the database.

### **Implementation Details:**

- Validation is handled in the backend using the `validate_input` function, which checks if the input meets all the rules.
- Duplicates are checked in the database before saving the new input.
- Validation failures are returned to the frontend with detailed error messages.

---

## Any design decisions made


Backend Framework:



The app is designed in a way that makes it easy to move to a cloud service like AWS in the future, if needed.

1. **Backend Framework:** 
   - Flask was chosen because it’s simple and works well for smaller projects like this one.

2. **Database:** 
   - PostgreSQL was selected because it’s reliable and makes it easy to check for duplicates.

3. **Validation Logic:**
   - All validation happens in the backend to make sure the input rules are always followed, no matter how the user interacts with the app.

4. **Frontend:**
   - The frontend is basic, using just HTML and JavaScript, to keep things simple and focus on the backend.

5. **Error Handling:**
   - The app has error handling to deal with problems like database issues or validation processes to provide clear feedback to users.

6. **Scalability:**
   - Although not deployed, the app is designed in a way that makes it easy to host the application on AWS if needed.

---

## Future Improvements
- **Enhanced Frontend:** Add a more interactive UI with real-time password strength indicators.
- **Security Enhancements:** Implement rate limiting and IP-based restrictions to prevent abuse.
- **Logging and Monitoring:** Add logging for debugging and potential integration with AWS CloudWatch for live monitoring.
