import os
from flask import Flask, render_template, request
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def query_openai(prompt, max_tokens=300):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

@app.route("/", methods=["GET", "POST"])
def index():
    city = ""
    category = ""
    places_text = ""
    places = []
    selected_place = ""
    itinerary = ""

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        category = request.form.get("category", "").strip()
        selected_place = request.form.get("place", "").strip()

        if city and category and not selected_place:
            # Step 1: Generate places list from AI
            prompt = f"List 5 famous {category} places to visit in {city} as a numbered list."
            places_text = query_openai(prompt)
            places = [line.split(". ",1)[-1].strip() for line in places_text.split("\n") if "." in line]
        elif city and category and selected_place:
            # Step 2: Generate itinerary for selected place
            prompt = (
                f"Generate a detailed one-day travel itinerary for a tourist visiting "
                f"'{selected_place}' in {city}. Include popular nearby attractions, meal suggestions, and travel tips."
            )
            itinerary = query_openai(prompt, max_tokens=500)

    return render_template(
        "index.html",
        city=city,
        category=category,
        places=places,
        selected_place=selected_place,
        itinerary=itinerary,
    )

if __name__ == "__main__":
    app.run(debug=True)
