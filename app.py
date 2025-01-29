from flask import Flask, render_template, request, jsonify, logging, send_file
import requests
import qrcode
import base64
from io import BytesIO
import logging
import random
import time
from urllib.parse import urlparse

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def shorten_url(url):
    if not is_valid_url(url):
        raise ValueError("Invalid URL format")

    shorteners = [
        {
            'name': 'tinyurl',
            'function': lambda u: requests.get(f"http://tinyurl.com/api-create.php?url={u}", timeout=5).text,
            'validator': lambda r: r and len(r) < 30
        },
        {
            'name': 'is.gd',
            'function': lambda u: requests.get(f"https://is.gd/create.php?format=simple&url={u}", timeout=5).text,
            'validator': lambda r: r and r.startswith('https://is.gd/')
        },
        {
            'name': 'v.gd',
            'function': lambda u: requests.get(f"https://v.gd/create.php?format=simple&url={u}", timeout=5).text,
            'validator': lambda r: r and r.startswith('https://v.gd/')
        },
        {
            'name': 'clck.ru',
            'function': lambda u: requests.get(f"https://clck.ru/--?url={u}", timeout=5).text,
            'validator': lambda r: r and r.startswith('https://clck.ru/')
        }
    ]
    
    errors = []
    for _ in range(3):  # Try up to 3 times
        random.shuffle(shorteners)  # Randomize the order of shorteners
        
        for shortener in shorteners:
            try:
                app.logger.info(f"Trying {shortener['name']} shortener...")
                short_url = shortener['function'](url)
                
                if shortener['validator'](short_url):
                    app.logger.info(f"Successfully shortened URL using {shortener['name']}: {short_url}")
                    return short_url
                else:
                    error_msg = f"{shortener['name']} returned invalid response"
                    app.logger.warning(error_msg)
                    errors.append(error_msg)
                    
            except requests.RequestException as e:
                error_msg = f"Error with {shortener['name']}: {str(e)}"
                app.logger.warning(error_msg)
                errors.append(error_msg)
                time.sleep(1)  # Wait before trying next service
                
    # If all attempts fail
    error_message = "Failed to shorten URL after multiple attempts. Services may be unavailable."
    app.logger.error(f"{error_message} Errors: {', '.join(errors)}")
    raise Exception(error_message)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['url']
        
        try:
            if not is_valid_url(long_url):
                raise ValueError("Please enter a valid URL including http:// or https://")

            start_time = time.time()
            short_url = shorten_url(long_url)
            end_time = time.time()
            
            if not is_valid_url(short_url):
                raise ValueError("Failed to generate valid shortened URL")
            
            app.logger.info(f"URL shortened: {long_url} -> {short_url} (Time: {end_time - start_time:.2f}s)")
            
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(short_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            qr_code = base64.b64encode(buffered.getvalue()).decode()
            
            return jsonify({
                'short_url': short_url, 
                'qr_code': qr_code,
                'original_url': long_url,
                'processing_time': f"{end_time - start_time:.2f}s"
            })
        except ValueError as e:
            app.logger.warning(f"Validation error for URL {long_url}: {str(e)}")
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            app.logger.error(f"Error processing URL {long_url}: {str(e)}")
            return jsonify({'error': "Unable to shorten URL. Please try again later."}), 400
    
    return send_file('index.html')

@app.route('/generate-qr', methods=['POST'])
def generate_qr():
    data = request.json
    content = data.get('content')
    color = data.get('color', '#000000')
    size = int(data.get('size', 250))

    if not content:
        return jsonify({'error': 'No content provided'}), 400

    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(content)
        qr.make(fit=True)
        
        fill_color = color
        back_color = 'white' if color != '#ffffff' else 'black'
        
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        
        # Resize the image
        img = img.resize((size, size))
        
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        qr_code = base64.b64encode(buffered.getvalue()).decode()
        
        app.logger.info(f"QR code generated: content length {len(content)}, color {color}, size {size}")
        return jsonify({
            'qr_code': qr_code,
            'content': content,
            'color': color,
            'size': size
        })
    except Exception as e:
        app.logger.error(f"Error generating QR code: {str(e)}")
        return jsonify({'error': str(e)}), 400


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)