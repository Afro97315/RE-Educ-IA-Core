from flask import Flask, request, jsonify

app = Flask(__name__)

# Base de données simple (en mémoire) pour contextAdder
context_db = {
    "histoire coloniale": "Cette information doit être replacée dans le contexte de la colonisation et de ses effets.",
    "économie esclavagiste": "Le commerce des esclaves a profondément marqué cette région et ses sociétés.",
    "Afrique de l'Ouest": "L’Afrique de l’Ouest a été un centre économique et culturel majeur bien avant la colonisation."
}

# Liste de biais à détecter (simplifiée)
biases_list = {
    "eurocentrisme": ["découverte", "arriéré", "non civilisé"],
    "racisme structurel": ["violence", "pauvreté", "instabilité"],
    "invisibilisation": ["n’a pas existé", "sans histoire", "sans culture"]
}

@app.route('/biasScanner', methods=['POST'])
def bias_scanner():
    data = request.get_json()
    text = data.get('text', '')
    target_perspective = data.get('target_perspective', 'afrocentré')

    detected_biases = []

    for bias, keywords in biases_list.items():
        for keyword in keywords:
            if keyword.lower() in text.lower():
                detected_biases.append(bias)

    # Reformulation simplifiée
    reformulated = text
    if "découverte" in text.lower():
        reformulated = "Les Européens ont pris contact avec une région qui existait depuis des millénaires."

    return jsonify({
        "original_text": text,
        "detected_biases": detected_biases,
        "suggested_reformulation": reformulated
    })


@app.route('/contextAdder', methods=['POST'])
def context_adder():
    data = request.get_json()
    text = data.get('text', '')
    add_context = data.get('add_context', [])

    added_context = []
    for key in add_context:
        if key in context_db:
            added_context.append(context_db[key])

    return jsonify({
        "original_text": text,
        "added_context": added_context
    })


@app.route('/roleSwitch', methods=['POST'])
def role_switch():
    data = request.get_json()
    text = data.get('text', '')
    new_perspective = data.get('new_perspective', 'afrocentré')

    # Reformulation basique
    if "missionnaires" in text.lower():
        reformulated = "Les populations locales disposaient de savoirs ancestraux avant l’arrivée des missionnaires."
    else:
        reformulated = f"[Vue {new_perspective}] " + text

    return jsonify({
        "original_text": text,
        "rephrased_text": reformulated
    })


@app.route('/promptInjector', methods=['GET'])
def prompt_injector():
    topic = request.args.get('topic', 'Histoire')
    desired_perspective = request.args.get('desired_perspective', 'afrocentré')
    use_case = request.args.get('use_case', 'formation')

    generated_prompt = f"Explique {topic} en prenant en compte une perspective {desired_perspective}, avec une approche {use_case}."

    return jsonify({
        "generated_prompt": generated_prompt
    })


@app.route('/')
def home():
    return jsonify({
        "message": "Bienvenue sur RE-Educ'-IA Core",
        "available_endpoints": [
            "/biasScanner",
            "/contextAdder",
            "/roleSwitch",
            "/promptInjector"
        ]
    })


if __name__ == '__main__':
    app.run(debug=True)
