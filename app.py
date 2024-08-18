from flask import Flask, render_template, request, send_file
import instaloader
import os
import shutil

app = Flask(__name__)

# Direktori tempat menyimpan video yang diunduh
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Inisialisasi Instaloader
loader = instaloader.Instaloader()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            # Mendapatkan shortcode dari URL
            shortcode = url.split('/')[-2]

            # Mendapatkan post dari shortcode
            post = instaloader.Post.from_shortcode(loader.context, shortcode)

            # Mendapatkan file video dengan Instaloader
            filename = f'{shortcode}.mp4'
            filepath = os.path.join(DOWNLOAD_FOLDER, filename)
            
            # Download video dengan Instaloader
            loader.download_post(post, target=DOWNLOAD_FOLDER)

            # Pindahkan file video ke nama yang benar
            for filename in os.listdir(DOWNLOAD_FOLDER):
                if filename.endswith('.mp4'):
                    shutil.move(os.path.join(DOWNLOAD_FOLDER, filename), filepath)
                    break

            return send_file(filepath, as_attachment=True)
        except Exception as e:
            return f'Error: {str(e)}'
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
