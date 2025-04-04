from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO
import base64
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_image = None
    
    if request.method == 'POST':
        # Get data from form
        data = request.form.get('data', '')
        box_size = int(request.form.get('box_size', 10))
        border = int(request.form.get('border', 4))
        fg_color = request.form.get('fg_color', '#000000')
        bg_color = request.form.get('bg_color', '#FFFFFF')
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color=fg_color, back_color=bg_color)
        
        # Save to BytesIO object
        buffered = BytesIO()
        img.save(buffered)
        
        # Convert to base64 for displaying in HTML
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        qr_image = f"data:image/png;base64,{img_str}"
    
    return render_template('index.html', qr_image=qr_image)

@app.route('/download', methods=['POST'])
def download():
    data = request.form.get('data', '')
    box_size = int(request.form.get('box_size', 10))
    border = int(request.form.get('border', 4))
    fg_color = request.form.get('fg_color', '#000000')
    bg_color = request.form.get('bg_color', '#FFFFFF')
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color=fg_color, back_color=bg_color)
    
    # Save to BytesIO object
    buffered = BytesIO()
    img.save(buffered)
    buffered.seek(0)
    
    return send_file(buffered, mimetype='image/png', as_attachment=True, download_name='qrcode.png')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)