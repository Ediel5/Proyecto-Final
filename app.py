from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    Response,
)
from db import get_connection, init_db
import io
import csv

app = Flask(__name__)
app.secret_key = "cambia-esta-clave"
init_db()


@app.route("/")
def index():
    estado = request.args.get("estado", "").strip()
    tipo = request.args.get("tipo", "").strip()
    texto = request.args.get("texto", "").strip()

    query = "SELECT * FROM solicitudes WHERE 1=1"
    params = []

    if estado:
        query += " AND estado = ?"
        params.append(estado)

    if tipo:
        query += " AND tipo LIKE ?"
        params.append(f"%{tipo}%")

    if texto:
        query += " AND (folio LIKE ? OR solicitante LIKE ? OR descripcion LIKE ?)"
        texto_like = f"%{texto}%"
        params.extend([texto_like, texto_like, texto_like])

    with get_connection() as conn:
        cur = conn.execute(query + " ORDER BY fecha DESC, id DESC", params)
        solicitudes = cur.fetchall()

    return render_template(
        "index.html",
        solicitudes=solicitudes,
        filtro_estado=estado,
        filtro_tipo=tipo,
        filtro_texto=texto,
    )


@app.route("/nueva", methods=["GET", "POST"])
def nueva():
    if request.method == "POST":
        folio = request.form.get("folio", "").strip()
        fecha = request.form.get("fecha", "").strip()
        solicitante = request.form.get("solicitante", "").strip()
        tipo = request.form.get("tipo", "").strip()
        estado = request.form.get("estado", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        if not (folio and fecha and solicitante and tipo and estado):
            flash("Todos los campos marcados como obligatorios deben llenarse.", "danger")
            data = {
                "folio": folio,
                "fecha": fecha,
                "solicitante": solicitante,
                "tipo": tipo,
                "estado": estado,
                "descripcion": descripcion,
            }
            return render_template("form.html", solicitud=data, modo="nueva")

        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO solicitudes (folio, fecha, solicitante, tipo, estado, descripcion)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (folio, fecha, solicitante, tipo, estado, descripcion),
            )
            conn.commit()

        flash("Solicitud registrada correctamente.", "success")
        return redirect(url_for("index"))

    # GET
    return render_template("form.html", solicitud=None, modo="nueva")


@app.route("/editar/<int:solicitud_id>", methods=["GET", "POST"])
def editar(solicitud_id):
    if request.method == "POST":
        folio = request.form.get("folio", "").strip()
        fecha = request.form.get("fecha", "").strip()
        solicitante = request.form.get("solicitante", "").strip()
        tipo = request.form.get("tipo", "").strip()
        estado = request.form.get("estado", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        if not (folio and fecha and solicitante and tipo and estado):
            flash("Todos los campos marcados como obligatorios deben llenarse.", "danger")
            data = {
                "id": solicitud_id,
                "folio": folio,
                "fecha": fecha,
                "solicitante": solicitante,
                "tipo": tipo,
                "estado": estado,
                "descripcion": descripcion,
            }
            return render_template("form.html", solicitud=data, modo="editar")

        with get_connection() as conn:
            conn.execute(
                """
                UPDATE solicitudes
                SET folio = ?, fecha = ?, solicitante = ?, tipo = ?, estado = ?, descripcion = ?
                WHERE id = ?
                """,
                (folio, fecha, solicitante, tipo, estado, descripcion, solicitud_id),
            )
            conn.commit()

        flash("Solicitud actualizada correctamente.", "success")
        return redirect(url_for("index"))

    # GET
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM solicitudes WHERE id = ?", (solicitud_id,))
        solicitud = cur.fetchone()

    if solicitud is None:
        flash("La solicitud indicada no existe.", "warning")
        return redirect(url_for("index"))

    return render_template("form.html", solicitud=solicitud, modo="editar")


@app.route("/eliminar/<int:solicitud_id>", methods=["POST"])
def eliminar(solicitud_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM solicitudes WHERE id = ?", (solicitud_id,))
        conn.commit()

    flash("Solicitud eliminada correctamente.", "success")
    return redirect(url_for("index"))


@app.route("/exportar")
def exportar():
    estado = request.args.get("estado", "").strip()
    tipo = request.args.get("tipo", "").strip()
    texto = request.args.get("texto", "").strip()

    query = "SELECT * FROM solicitudes WHERE 1=1"
    params = []

    if estado:
        query += " AND estado = ?"
        params.append(estado)

    if tipo:
        query += " AND tipo LIKE ?"
        params.append(f"%{tipo}%")

    if texto:
        query += " AND (folio LIKE ? OR solicitante LIKE ? OR descripcion LIKE ?)"
        texto_like = f"%{texto}%"
        params.extend([texto_like, texto_like, texto_like])

    with get_connection() as conn:
        cur = conn.execute(query + " ORDER BY fecha DESC, id DESC", params)
        solicitudes = cur.fetchall()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        ["id", "folio", "fecha", "solicitante", "tipo", "estado", "descripcion"]
    )

    for s in solicitudes:
        writer.writerow(
            [
                s["id"],
                s["folio"],
                s["fecha"],
                s["solicitante"],
                s["tipo"],
                s["estado"],
                s["descripcion"] or "",
            ]
        )

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=solicitudes.csv"},
    )


if __name__ == "__main__":
    app.run(debug=True)
