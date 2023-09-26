from flask import Flask, render_template_string, request
import numpy as np
import pandas as pd
import datetime

app = Flask(__name__)

# Extract data from Excel file
sheets = pd.read_excel("file_names_surnames.xlsx", sheet_name=None)
surnames_data = sheets["Priimki"]
male_names_data = sheets["Moška imena"]
female_names_data = sheets["Ženska imena"]

surnames_list = surnames_data.iloc[1:, 0].values
surnames_freq = surnames_data.iloc[1:, 1].astype(int).values

male_names_list = male_names_data.iloc[1:, 0].values
male_names_freq = male_names_data.iloc[1:, 1].astype(int).values

female_names_list = female_names_data.iloc[1:, 0].values
female_names_freq = female_names_data.iloc[1:, 1].astype(int).values

@app.route('/', methods=['GET', 'POST'])
def index():
    gender = "male"  # default selection
    num_names = 1  # default number of names to generate
    names = []

    if request.method == 'POST':
        gender = request.form.get('gender', 'male')
        num_names = int(request.form.get('num_names', 1))
        
        for _ in range(num_names):
            if gender == "male":
                name = generate_random_name(male_names_list, male_names_freq)
            else:
                name = generate_random_name(female_names_list, female_names_freq)
            surname = generate_random_name(surnames_list, surnames_freq)
            full_name = f"{name} {surname}"
            names.append(full_name)

        # Save to text file
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"generated_names_{gender}_{timestamp}.txt"
        with open(filename, 'w') as f:
            for name in names:
                f.write(name + '\n')

    return render_template_string("""
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            form { background-color: #f2f2f2; padding: 20px; border-radius: 5px; }
            ul { list-style-type: none; padding: 0; }
            li { margin: 10px 0; }
            h1 { color: #333; }
        </style>

        <h1>Random Name and Surname Generator</h1>
        <form method="post">
            <label for="gender">Choose Gender:</label>
            <select name="gender" id="gender">
                <option value="male" {{ 'selected' if gender == 'male' else '' }}>Male</option>
                <option value="female" {{ 'selected' if gender == 'female' else '' }}>Female</option>
            </select>
            <br><br>
            <label for="num_names">Number of Names:</label>
            <input type="number" name="num_names" id="num_names" value="{{ num_names }}" min="1">
            <br><br>
            <input type="submit" value="Generate">
        </form>
        <h2>Generated Names:</h2>
        <ul>
            {% for name in names %}
                <li>{{ name }}</li>
            {% endfor %}
        </ul>
    """, names=names, gender=gender, num_names=num_names)

def generate_random_name(names_list, names_freq):
    """Generate a random name based on its frequency."""
    frequencies_array = np.array(names_freq)  # Convert to NumPy array
    return np.random.choice(names_list, p=frequencies_array/frequencies_array.sum())

if __name__ == '__main__':
    app.run(debug=True)