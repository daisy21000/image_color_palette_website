from flask import Flask, render_template, request, redirect, url_for
from colorthief import ColorThief
import os
import pyperclip

palette = None
alert = 'False'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/'


@app.route('/')
def home():
    return render_template('index.html', palette=palette, alert=alert)


@app.route('/get_palette', methods=['POST'])
def get_palette():
    global palette
    img = request.files['img']
    img.save(os.path.join(app.config['UPLOAD_FOLDER'], img.filename))
    img_path = f'static/{img.filename}'
    color_thief = ColorThief(img_path)
    palette = color_thief.get_palette(color_count=11)
    os.remove(img_path)
    return redirect(url_for('home'))


@app.route('/copy')
def copy_color():
    global alert
    color = f"rgb({request.args.get('r')}, {request.args.get('g')}, {request.args.get('b')})"
    pyperclip.copy(color)
    alert = 'True'
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
