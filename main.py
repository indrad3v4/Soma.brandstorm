from flask import Flask, render_template, request
import os
import openai

app = Flask(__name__)

questions = [
    "Enter your name:",
    "Describe your journey from:",
    "Describe your journey to:",
    "Enter your brand name:",
    "Enter your brand's core values:",
    "Enter your brand vision:",
    "Enter your brand mission:",
    "Describe your brand personality:",
    "Enter your unique value:",
    "Describe your audience:",
    "Enter your audience insight:",
    "What's your brand's role?",
    "What's your big idea?",
    "Which media platforms will you use?",
    "Enter your budget:",
    "Enter your timeframe:",
]

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    question_index = int(request.form.get('question_index', 0))
    user_input = request.form.get('user_input', "")

    if request.method == 'POST':
        if user_input == "":
            # The user wants an AI-generated answer
            api_key = os.getenv('API_KEY')
            openai.api_key = api_key
            response = openai.Completion.create(engine="davinci", prompt=questions[question_index], max_tokens=60)
            user_input = response.choices[0].text.strip()
        
        result += f"{questions[question_index]} {user_input}\n"
        question_index += 1  # Move to the next question

    if question_index >= len(questions):
        # Construct the final prompt
        answers = result.split('\n')[:-1]  # Split the result into a list of answers
        answers = [answer.split(': ')[1] for answer in answers]  # Remove the question part from each answer
        final_prompt = f"""
        I, {answers[0]}, am on a journey from {answers[1]} to {answers[2]}. 
        My brand, {answers[3]}, is guided by our core values of {answers[4]}, and we envision a future where {answers[5]}.
        Our mission is to {answers[6]}, and our brand personality is {answers[7]}.
        With my unique value in {answers[8]}, I aim to serve {answers[9]}. 
        Their insight is {answers[10]}, and my proposition is to {answers[11]}, 
        which is present in the form of {answers[12]} in {answers[13]}. 
        With a budget of {answers[14]}, my goal is to achieve {answers[1]} by {answers[15]}.
        """

        # Generate the brand book
        api_key = os.getenv('API_KEY')
        openai.api_key = api_key
        response = openai.Completion.create(engine="davinci", prompt=final_prompt, max_tokens=500, temperature=0.5, top_p=1)
        result = response.choices[0].text.strip()
        return render_template('result.html', result=result)  # Render a different template to show the final result

    return render_template('index.html', result=result, question=questions[question_index], question_index=question_index)

if __name__ == "__main__":
    app.run(debug=True)
