# app.py
from flask import Flask, render_template, request
from compute import compute_banzhaf, compute_shapley, is_winning

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    # show input form
    return render_template("index.html")

@app.route("/compute", methods=["POST"])
def compute():
    error = None
    # parse k
    try:
        k = int(request.form["k"])
        if k < 1:
            raise ValueError
    except Exception:
        error = "Invalid k. Please enter an integer ≥ 1."
        return render_template("index.html", error=error)

    # parse quotas
    quotas_raw = request.form.get("quotas", "").strip()
    quotas_split = [s.strip() for s in quotas_raw.split(",") if s.strip() != ""]
    if len(quotas_split) != k:
        error = f"Quotas: expected {k} comma-separated integers."
        return render_template("index.html", error=error)
    try:
        quotas = [int(x) for x in quotas_split]
        if any(q < 0 for q in quotas):
            raise ValueError
    except Exception:
        error = "Quotas must be nonnegative integers."
        return render_template("index.html", error=error)

    # parse weights
    weights_lines = request.form.get("weights", "").strip().splitlines()
    if len(weights_lines) != k:
        error = f"Weight vectors: expected {k} lines (one per dimension)."
        return render_template("index.html", error=error)
    weight_matrix = []
    n = None
    for line in weights_lines:
        row_split = [s.strip() for s in line.split(",") if s.strip() != ""]
        if n is None:
            n = len(row_split)
            if n < 1:
                error = "Each weight vector must have at least one entry."
                return render_template("index.html", error=error)
        elif len(row_split) != n:
            error = "All weight‐vector rows must have the same number of players."
            return render_template("index.html", error=error)
        try:
            row = [int(x) for x in row_split]
            if any(w < 0 for w in row):
                raise ValueError
            weight_matrix.append(row)
        except Exception:
            error = "Weights must be nonnegative integers."
            return render_template("index.html", error=error)

    # index type
    index_type = request.form.get("index_type", "shapley").lower()
    if index_type not in ("shapley", "banzhaf"):
        error = "Please select either Shapley or Banzhaf."
        return render_template("index.html", error=error)

    # compute value
    if index_type == "shapley":
        power = compute_shapley(k, quotas, weight_matrix)
    else:
        power = compute_banzhaf(k, quotas, weight_matrix)

    # render results
    return render_template(
        "results.html",
        n_players=n,
        k_dims=k,
        quotas=quotas,
        weights=weight_matrix,
        index_type=index_type.capitalize(),
        power=power
    )

if __name__ == "__main__":
    app.run(debug=True)