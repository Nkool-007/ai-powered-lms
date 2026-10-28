from flask import jsonify


def success(data=None, status=200):
    return jsonify({"data": data}), status


def error(code, message, status=400, details=None):
    return jsonify({
        "error": code,
        "message": message,
        "details": details,
    }), status
