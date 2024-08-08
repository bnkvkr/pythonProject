import subprocess
import json
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    stock_name = request.form.get('stock_name')

    # Run the Scrapy spider with the provided stock name
    try:
        result = subprocess.run(
            ['scrapy', 'crawl', 'news_spider', '-a', f'stock_name={stock_name}'],
            capture_output=True, text=True, check=True
        )
        print(result.stdout)  # Debug output
        print(result.stderr)  # Debug errors
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Scrapy process failed: {e}"}), 500

    # Read the results from the output file
    output_file = 'output.json'
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r') as file:
                results = json.load(file)
        except json.JSONDecodeError as e:
            return jsonify({"error": f"Error decoding JSON: {e}"}), 500
        except Exception as e:
            return jsonify({"error": f"Error reading output file: {e}"}), 500
    else:
        results = []

    # Clear the output file after reading
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
        except Exception as e:
            return jsonify({"error": f"Error removing output file: {e}"}), 500

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
