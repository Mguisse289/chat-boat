from flask import Flask, request, jsonify

app = Flask(__name__)

# Données simulées de disponibilité
disponibilities = {
    "gavina": {
        "chalet": {
            "2025-07-15": {
                "2025-07-29": True
            }
        }
    }
}

# Fonction pour vérifier si les dates fournies sont égales aux dates de disponibilité
def is_date_in_range(start_date, end_date, check_start, check_end):
    return (check_start == start_date) and (check_end == end_date)

# Route pour vérifier la disponibilité
@app.route('/check_availability', methods=['POST'])
def get_disponibility():
    data = request.json
    logement_type = data.get('logement_type')
    date_d_arrivee = data.get('date_d_arrivee')
    date_de_depart = data.get('date_de_depart')
    village = data.get('village')

    # Initialisation de la disponibilité
    result = False

    try:
        available_date = disponibilities[village][logement_type]
        for start_date, end_dates in available_date.items():
            for end_date, is_available in end_dates.items():
                # Vérification avec la fonction is_date_in_range
                if is_date_in_range(start_date, end_date, date_d_arrivee, date_de_depart):
                    result = is_available  # En sortie un booléen
                    break
            if result:  # Permet d'arrêter la boucle si jamais la dispo est trouvée
                break
    except KeyError:
        result = False  # Dans le cas où il n'est pas égal à la plage de date dispo
        
    # Si le nom du village est différent des valeurs spécifiées
    villages_acceptes = {"gavina", "lous seurrots", "domaine de drancourt", "rindin", "en champagne"}
    logements_acceptes = {"chalet", "camping", "tentes", "cabanes", "cottage"}
    
    if village not in villages_acceptes:
        return jsonify({"error": "Village not found"}), 404
    elif logement_type not in logements_acceptes:
        return jsonify({"error": "Logement type not found"}), 404
    elif village not in villages_acceptes and logement_type not in logements_acceptes :
        return jsonify({"error": "logement and village not found"}), 404

    response = {
        "disponibilitie": result,
        "logement_type": logement_type,
        "date_d_arrivee": date_d_arrivee,
        "date_de_depart": date_de_depart,
        "village": village,
    }
   
    # Lui renvoyer la réponse en JSON
    return jsonify(response)

# Fonction main
if __name__ == '__main__':
    app.run(port=5000)
