from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

site_ids = ['BRA010', 'BRA011', 'BRA012', 'CAM010', 'CAM011', 'CAM030', 'JEF009', 'JEF012', 'JEF013', 'GAL036', 'GAL037', 'GAL038', 'NUE014', 'NUE015', 'NUE016']

@app.route('/fetch-data/')
def fetch_csv_data():
    base_url = "https://enterococcus.today/waf/nowcast/TX/"
    station = request.args.get('station', default='all').lower()
    data = {}

    if station == 'all':
        for site in site_ids:
            csv_url = f"{base_url}{site}.csv"
            try:
                response = requests.get(csv_url)
                response.raise_for_status()
                data[site] = response.text
            except requests.HTTPError:
                data[site] = 'Failed to fetch CSV file.'
        return jsonify(data)
    else:
        site_id = station.upper()  # Assuming site IDs are in uppercase
        if site_id in site_ids:
            csv_url = f"{base_url}{site_id}.csv"
            try:
                response = requests.get(csv_url)
                response.raise_for_status()
                return response.text
            except requests.HTTPError as e:
                return jsonify({'error': 'Failed to fetch CSV file.', 'details': str(e)})
        else:
            return jsonify({'error': 'Invalid station ID or station not found.'})

if __name__ == '__main__':
    app.run(debug=True)
