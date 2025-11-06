from flask import Flask, render_template, request, redirect, url_for, session
import base64

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ✅ Create admin user (ID 0) for the IDOR challenge
USERS = {
    0: {"username": "admin", "id": 0, "display": "Admin User"}
}
FLAG1 = "kmutnbCTF{b4s364_enc}"
FLAG2 = "kmutnbCTF{1nsp3c7_th3_p4g3}"
FLAG3 = "kmutnbCTF{IDOR_Br0k3n_4cc3s5_c0ntr0l}"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username:
            error = "Username is required"
            return render_template("login.html", error=error)

        if username.lower() == "admin":
            error = "Invalid credentials"
            return render_template("login.html", error=error)

        expected = base64.b64encode(username.encode()).decode()
        if password == expected:
            # Find existing user ID or create new one
            found_id = None
            for uid, u in USERS.items():
                if u.get("username") == username:
                    found_id = uid
                    break

            if found_id is None:
                max_existing = max([k for k in USERS.keys() if isinstance(k, int) and k >= 1], default=0)
                new_id = max_existing + 1
                USERS[new_id] = {"username": username, "id": new_id, "display": f"{username} User"}
                found_id = new_id

            session["logged_in"] = True
            session["username"] = username
            session["user_id"] = found_id
            return redirect(url_for("dashboard"))

        error = "Invalid credentials"
        return render_template("login.html", error=error, flag2=FLAG2)

    return render_template("login.html")


def login_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper


@app.route("/dashboard")
@login_required
def dashboard():
    username = session.get("username")
    uid = session.get("user_id")
    return render_template("dashboard.html", username=username, uid=uid, flag1=FLAG1)


@app.route("/profile")
@login_required
def profile():
    id_param = request.args.get("id", "")
    try:
        user_id = int(id_param)
    except (ValueError, TypeError):
        return "invalid id", 400

    user = USERS.get(user_id)
    if user is None:
        return "user not found", 404

    is_admin = (user_id == 0)
    return render_template("profile.html", user=user, is_admin=is_admin, flag3=FLAG3)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
