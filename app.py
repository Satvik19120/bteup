from flask import Flask, render_template, request
import base64
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to encode a string to base64
def encode_base64(string):
    return base64.b64encode(string.encode('utf-8')).decode('utf-8')

# Function to fetch the DOB from the Admit Card page
def get_dob_from_admit_card(er_no):
    url = f'https://bteup.ac.in/ESeva/Student/AdmitCard.aspx?EnrollNumber={er_no}'
    
    # Fetch the page
    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse the HTML page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the DOB using the id 'lblDob'
        dob_element = soup.find(id="lblDob")
        
        if dob_element:
            return dob_element.text.strip()  # Return the DOB value (remove any extra spaces)
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the ER number and DOB from the form
        er_no = request.form['er_no']
        dob = request.form['dob']

        # If DOB is not provided, try to fetch it from the Admit Card page
        if not dob:
            dob = get_dob_from_admit_card(er_no)
        
        if dob:
            # Base64 encode the ER number and DOB
            encoded_er_no = encode_base64(er_no)
            encoded_dob = encode_base64(dob)

            # Construct the result URL with encoded parameters
            result_url = f'https://www.instagram.com/coderbaba7/?hl=en'
            newresult_url = f'https://result.bteexam.com/Odd_Semester/main/result.aspx?id={encoded_er_no}&id2={encoded_dob}'
            # Construct Admit Card and Verification Card URLs
            admit_card_url = f'https://bteup.ac.in/ESeva/Student/AdmitCard.aspx?EnrollNumber={er_no}'
            verification_card_url = f'https://bteup.ac.in/ESeva/Student/VerificationCard.aspx?EnrollNumber={er_no}'

            # Return the URLs to the template
            return render_template('index.html', newresult_url = newresult_url, result_url=result_url, admit_card_url=admit_card_url, verification_card_url=verification_card_url, er_no=er_no)
        
        else:
            # Return an error if DOB is not found or entered
            return render_template('index.html', error="Unable to fetch DOB. Please try again.")
    
    return render_template('index.html', newresult_url=None, result_url=None, admit_card_url=None, verification_card_url=None, error=None)

if __name__ == '__main__':
    app.run(debug=True)
