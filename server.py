from flask import Flask, request, jsonify
import subprocess
import os
import base64

app = Flask(__name__)

@app.route('/', methods=['POST'])
def process_image():
    data = request.get_json()

    if 'image' not in data:
        return jsonify({'error': 'No image provided'}), 400

    # Decode base64 image
    image_data = data['image']
    image_buffer = base64.b64decode(image_data)
    temp_image_path = os.path.join(os.getcwd(), 'temp_image.png')

    with open(temp_image_path, 'wb') as f:
        f.write(image_buffer)

    # Execute the process.py script
    command = f'python process.py --image "{temp_image_path}" --cuda'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
 
    if process.returncode != 0:
        return jsonify({'error': stderr.decode('utf-8')}), 500

    output_dir = '/seg/output'
    output_data = {}

    # Read and include 1.png, 2.png, and final_seg.png
    alpha_dir = os.path.join(output_dir, 'alpha')
    for file_name in os.listdir(alpha_dir):
        file_path = os.path.join(alpha_dir, file_name)
        with open(file_path, 'rb') as f:
            file_buffer = f.read()
            base64_string = base64.b64encode(file_buffer).decode('utf-8')
            output_data[file_name] = base64_string

    cloth_seg_dir = os.path.join(output_dir, 'cloth_seg')
    final_seg_path = os.path.join(cloth_seg_dir, 'final_seg.png')
    with open(final_seg_path, 'rb') as f:
        final_seg_buffer = f.read()
        final_seg_base64 = base64.b64encode(final_seg_buffer).decode('utf-8')
        output_data['final_seg.png'] = final_seg_base64

    return jsonify(output_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083)
