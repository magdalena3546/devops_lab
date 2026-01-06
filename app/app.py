from flask import Flask, request, jsonify

app = Flask(__name__)


@app.get("/")
def home():
    return "DevOps Flask Calculator API"


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/info")
def info():
    return jsonify(
        name="DevOps Flask Calculator API",
        version="1.0.0",
        endpoints=[
            "GET /add?a=..&b=..",
            "GET /sub?a=..&b=..",
            "GET /mul?a=..&b=..",
            "GET /div?a=..&b=..",
            "POST /calc",
        ],
    )


def parse_float(name: str):
    """
    Reads query param and converts to float.
    Returns (value, error_message).
    """
    raw = request.args.get(name)
    if raw is None:
        return None, f"Missing query parameter: '{name}'"

    try:
        return float(raw), None
    except ValueError:
        return None, f"Invalid number for '{name}': '{raw}'"


@app.get("/add")
def add():
    a, err = parse_float("a")
    if err:
        return jsonify(error=err), 400

    b, err = parse_float("b")
    if err:
        return jsonify(error=err), 400

    return jsonify(operation="add", a=a, b=b, result=a + b)


@app.get("/sub")
def sub():
    a, err = parse_float("a")
    if err:
        return jsonify(error=err), 400

    b, err = parse_float("b")
    if err:
        return jsonify(error=err), 400

    return jsonify(operation="sub", a=a, b=b, result=a - b)


@app.get("/mul")
def mul():
    a, err = parse_float("a")
    if err:
        return jsonify(error=err), 400

    b, err = parse_float("b")
    if err:
        return jsonify(error=err), 400

    return jsonify(operation="mul", a=a, b=b, result=a * b)


@app.get("/div")
def div():
    a, err = parse_float("a")
    if err:
        return jsonify(error=err), 400

    b, err = parse_float("b")
    if err:
        return jsonify(error=err), 400

    if b == 0:
        return jsonify(error="Division by zero is not allowed"), 400

    return jsonify(operation="div", a=a, b=b, result=a / b)


@app.post("/calc")
def calc():
    """
    Example POST endpoint:
    Linux/macOS:
      curl -X POST http://localhost:5000/calc \
        -H "Content-Type: application/json" \
        -d '{"op":"add","a":2,"b":3}'

    Windows (cmd):
      curl -X POST "http://localhost:5000/calc" ^
        -H "Content-Type: application/json" ^
        -d "{\"op\":\"add\",\"a\":2,\"b\":3}"
    """
    data = request.get_json(silent=True) or {}
    op = data.get("op")
    a = data.get("a")
    b = data.get("b")

    if op not in {"add", "sub", "mul", "div"}:
        return jsonify(error="Invalid or missing 'op'. Use: add/sub/mul/div"), 400

    try:
        a = float(a)
        b = float(b)
    except (TypeError, ValueError):
        return jsonify(error="Fields 'a' and 'b' must be numbers"), 400

    if op == "add":
        result = a + b
    elif op == "sub":
        result = a - b
    elif op == "mul":
        result = a * b
    else:  # div
        if b == 0:
            return jsonify(error="Division by zero is not allowed"), 400
        result = a / b

    return jsonify(operation=op, a=a, b=b, result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

