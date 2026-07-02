from flask import Flask, render_template, request, send_file, jsonify
import os
from conversion_modules import (
    ImageToPDF,
    ImageToJPG,
    ImageToPNG,
    ImageToTXT,
    ImageToDOCX,
    txtToDocx,
    txtToPdf,
    pdfToTxt,
    pdfTDocx,
    docxToTxt,
    pdfToImage,
    txtToImage,
)

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024


@app.route("/", methods=["GET", "POST"])
def dashboard():
    file = request.files.get("file")
    try:
        if request.method == "POST":
            if not file:
                msg = "Please select a file."
                # return render_template("dashboard.html", msg=msg, msg_type="warning")
                return (
                    jsonify({"success": False, "message": msg, "type": "warning"}),
                    400,
                )
            format = request.form.get("format")
            filename = file.filename
            ext = os.path.splitext(filename)[1].lower().replace(".", "")
            if ext == format:
                msg = f"File is Alredy in {format} format"
                # return render_template("dashboard.html", msg=msg, msg_type="warning")
                return (
                    jsonify({"success": False, "message": msg, "type": "warning"}),
                    400,
                )
            if ext in ["png", "jpg", "jpeg"]:
                conversion_map = {
                    "pdf": ImageToPDF,
                    "docx": ImageToDOCX,
                    "png": ImageToPNG,
                    "jpg": ImageToJPG,
                    "txt": ImageToTXT,
                }
                get_format = conversion_map.get(format)
                try:
                    # if 10 /0:
                    #     print("hello")
                    if get_format:
                        output, filename, mimetype = get_format(file, ext)
                        
                    else:
                        msg = "Please select the Format"
                        return (
                            jsonify(
                                {"success": False, "message": msg, "type": "warning"}
                            ),
                            400,
                        )
                except:
                    msg = "Conversion failed."
                    return (
                        jsonify({"success": False, "message": msg, "type": "error"}),
                        500,
                    )
                return send_file(
                    output,
                    as_attachment=True,
                    download_name=filename,
                    mimetype=mimetype,
                )
            elif ext in ["pdf", "txt", "docx"]:
                conversion_map = {
                    ("txt", "docx"): txtToDocx,
                    ("txt", "pdf"): txtToPdf,
                    ("pdf", "txt"): pdfToTxt,
                    ("pdf", "docx"): pdfTDocx,
                    ("docx", "txt"): docxToTxt,
                    ("pdf", "png"): pdfToImage,
                    ("pdf", "jpg"): pdfToImage,
                    ("txt", "png"): txtToImage,
                    ("txt", "jpg"): txtToImage,
                }
                key = (ext, format)
                if key[0] == "docx" and key[1] in ["jpg", "png", "pdf"]:
                    msg = f"DOCX to {key[1]} conversion is currently not supported"
                    return (
                        jsonify({"success": False, "message": msg, "type": "info"}),
                        400,
                    )

                get_format = conversion_map.get(key)
                try:
                    if get_format:
                        if key[0] in ["pdf", "txt"] and key[1] in ["jpg", "png"]:
                            output, filename, mimetype = get_format(file, key[1])
                        else:
                            output, filename, mimetype = get_format(file)
                    else:
                        msg = "Please select the Format"
                        return (
                            jsonify(
                                {"success": False, "message": msg, "type": "warning"}
                            ),
                            400,
                        )
                except:
                    msg = "Conversion failed."
                    return (
                        jsonify({"success": False, "message": msg, "type": "error"}),
                        500,
                    )
                return send_file(
                    output,
                    as_attachment=True,
                    download_name=filename,
                    mimetype=mimetype,
                )
            else:
                msg = "Unsupported file format"
                return (
                    jsonify({"success": False, "message": msg, "type": "warning"}),
                    400,
                )
        return render_template("dashboard.html")
    except Exception as e:
        msg = "Conversion failed."
        # return render_template("dashboard.html", msg = msg,msg_type = "error")
        return jsonify({"success": False, "message": msg, "type": "error"})


if __name__ == "__main__":
    app.run(debug=True)
