import csv
import os

from quart import Quart, jsonify, send_from_directory
import httpx

app = Quart(__name__, static_folder='home/build')

@app.route("/data")
async def data_route():
    async with httpx.AsyncClient() as client:
        data = await client.get("https://docs.google.com/spreadsheets/d/e/2PACX-1vQCHQh-DwbQf1-rAq_zk77I5-0LpBidpkuYW8LbP0JxYwFxMV6YHD4NNSTlclWIUE7tHNY9O-fSU-mb/pub?gid=0&single=true&output=csv")

    split_data = csv.reader(data.text.split("\n"))
    
    ret_data = {"data": []}
    ret_data["data"] = [ {"id": row[1], "date": row[0], "src": row[2]} for row in split_data]

    return jsonify(ret_data)

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
async def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return await send_from_directory(app.static_folder, path)
    else:
        return await send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run()