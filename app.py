from flask import Flask, request, render_template, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Set the upload folder
UPLOAD_FOLDER = 'static/uploads'  # Remove leading '/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def index():
    return render_template('menu.html')

@app.route('/order', methods=['POST'])
def order():
    data = request.form
    if not data:
        return jsonify({'error': 'No data provided'})

    orders = []
    item_count = int(data.get('item_count', 1))
    for i in range(item_count):
        item_type = data.getlist('item_type[]')[i]
        name = data.getlist('name[]')[i]
        size = data.getlist('size[]')[i]
        toppings = request.form.getlist(f'toppings_{i}[]')
        address = data.getlist('address[]')[i]
        phone = data.getlist('phone[]')[i]
        image = request.files.get(f'image_{i}')

        if image.filename == '':
            return jsonify({'error': f'No image selected for item {i + 1}'})

        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        orders.append({
            'item_type': item_type,
            'name': name,
            'size': size,
            'toppings': toppings,
            'address': address,
            'phone': phone,
            'image_filename': filename
        })

    response = {
        'orders': orders,
        'message': 'Order received successfully'
    }
    return jsonify(response)

@app.route('/order/pizza', methods=['GET', 'POST'])
def order_pizza():
    if request.method == 'POST':
        return order()  # Call the shared order function for POST requests

    return render_template('order_pizza.html')

@app.route('/order/sandwich', methods=['GET', 'POST'])
def order_sandwich():
    if request.method == 'POST':
        return order()  # Call the shared order function for POST requests

    return render_template('order_sandwich.html')

if __name__ == '__main__':
    app.run(debug=True)
