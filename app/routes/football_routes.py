from flask import Blueprint, request, jsonify
from app.services.football_service import (
    create_football_clubs,
    get_all_footballs
)

football_bp = Blueprint("football", __name__)

@football_bp.route("/", methods=["GET"])
def index():
    return "API telah berjalan! Dibuat oleh Abdullah Ubaid"
    

@football_bp.route("/footballs/generate", methods=["POST"])
def generate():
    data = request.get_json()
    league = data.get("league") # Mengganti 'league' menjadi 'league'
    total = data.get("total")

    if not league:
        return jsonify({"error": "Theme is required"}), 400
    
    if not total:
        return jsonify({"error": "Total is required"}), 400
    
    if total <= 0:
        return jsonify({"error": "Total harus besar dari 0"}), 400
    
    if total > 10:
        return jsonify({"error": "Total maksimal harus 10"}), 400

    try:
        result = create_football_clubs(league, total)

        return jsonify({
            "league": league,
            "total": len(result),
            "data": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@football_bp.route("/footballs", methods=["GET"])
def get_all():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=100, type=int)

    data = get_all_footballs(page=page, per_page=per_page)

    return jsonify(data)