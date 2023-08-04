from flask import Flask, render_template, request, session
import os
import openai

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

questions = [
    "What's your name?",
    "Describe your journey so far (e.g., 'I started as a designer and evolved into a creative strategist.'):",
    "Where do you see your journey taking you (e.g., 'I aim to become a leading figure in AI-powered creative strategy.'):",
    "What is the name of your brand?",
    "What are the core values that guide your brand (e.g., 'Innovation, Authenticity, Impact')?",
    "How do you envision the future with your brand (e.g., 'Creating a world where AI and creativity merge to bring unprecedented value.')?",
    "What is the mission your brand is on (e.g., 'To redefine creative strategy with the power of AI.')?",
    "Can you describe your brand's personality (e.g., 'Innovative, Bold, Empathetic')?",
    "What is the unique value that you bring to your audience (e.g., 'I combine my skills in design, strategy, and AI to deliver unique solutions.')?",
    "Can you describe your target audience (e.g., 'Tech startups looking for a unique, impactful brand strategy.')?",
    "What key insight do you have about your audience (e.g., 'They struggle with standing out in the crowded tech startup space.')?",
    "What role does your brand play for your audience (e.g., 'We act as their creative ally, helping them carve out a unique brand identity.')?",
    "What is the big idea that your brand stands for (e.g., 'Merging creativity and technology for breakthrough brand strategies.')?",
    "Which media platforms will you use to reach your audience (e.g., 'LinkedIn, Medium, YouTube')?",
    "What is your budget for achieving your brand goals?",
    "What is your timeframe for achieving your brand goals?",
]


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'process' not in session:
        session['process'] = []

    question_index = int(request.form.get('question_index', 0))
    user_input = request.form.get('user_input', "")

    if request.method == 'POST':
        if user_input == "":
            api_key = os.getenv('API_KEY')
            openai.api_key = api_key
            prompt = '\n'.join(session['process'] + [questions[question_index]])
            response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=60)
            user_input = response.choices[0].text.strip()

        session['process'] += [questions[question_index], user_input]
        question_index += 1

    if question_index >= len(questions):
        session.clear()
        answers = session['process'][1::2]
        final_prompt = f"""
        I, {answers[0]}, am on a journey from {answers[1]} to {answers[2]}. 
        My brand, {answers[3]}, is guided by our core values of {answers[4]}, and we envision a future where {answers[5]}.
        Our mission is to {answers[6]}, and our brand personality is {answers[7]}.
        With my unique value in {answers[8]}, I aim to serve {answers[9]}. 
        Their insight is {answers[10]}, and my proposition is to {answers[11]}, 
        which is present in the form of {answers[12]} in {answers[13]}. 
        With a budget of {answers[14]}, my goal is to achieve {answers[1]} by {answers[15]}.
        """

        api_key = os.getenv('API_KEY')
        openai.api_key = api_key
        response = openai.Completion.create(engine="davinci", prompt=final_prompt, max_tokens=500, temperature=0.5, top_p=1)
        result = response.choices[0].text.strip()
        return render_template('result.html', result=result)

    process = '\n'.join(session['process'])
    return render_template('index.html', process=process, question=questions[question_index], question_index=question_index)


if __name__ == "__main__":
    app.run(debug=True)
