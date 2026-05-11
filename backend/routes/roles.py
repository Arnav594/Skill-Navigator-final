"""GET /roles — list all roles available in skills.csv."""
from flask import Blueprint, jsonify
from services.data_service import load_all_roles

bp = Blueprint("roles", __name__)


@bp.route("/roles", methods=["GET"])
def get_roles():
    return jsonify(load_all_roles())
