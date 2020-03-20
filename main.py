import csv
import os
from collections import defaultdict

from quart import Quart, jsonify, send_from_directory, render_template
import httpx

app = Quart(__name__, static_folder='home/build/static', template_folder="home/build")

@app.route("/data")
async def data_route():
    async with httpx.AsyncClient() as client:
        data = await client.get("https://docs.google.com/spreadsheets/d/e/2PACX-1vQCHQh-DwbQf1-rAq_zk77I5-0LpBidpkuYW8LbP0JxYwFxMV6YHD4NNSTlclWIUE7tHNY9O-fSU-mb/pub?gid=0&single=true&output=csv")

    split_data = csv.reader(data.text.split("\n"))
    
    ret_data = {"data": []}
    ret_data["data"] = [ {"id": row[1], "date": row[0], "src": row[2]} for row in split_data]

    return jsonify(ret_data)

@app.route("/data/new_cases")
async def data_new_cases_route():
    async with httpx.AsyncClient() as client:
        data = await client.get("https://docs.google.com/spreadsheets/d/e/2PACX-1vQCHQh-DwbQf1-rAq_zk77I5-0LpBidpkuYW8LbP0JxYwFxMV6YHD4NNSTlclWIUE7tHNY9O-fSU-mb/pub?gid=0&single=true&output=csv")

    split_data = csv.reader(data.text.split("\n"))

    proc_data = defaultdict(int)

    for row in split_data:
        if row[0] == "date":
            continue
        proc_data[row[0]] = proc_data[row[0]] + 1

    ret_data = [{"date": key, "new_cases": proc_data[key]} for key in proc_data.keys()]

    print(ret_data)

    return jsonify(ret_data)

@app.route("/data/cases")
async def data_cases_route():
    async with httpx.AsyncClient() as client:
        data = await client.get("https://docs.google.com/spreadsheets/d/e/2PACX-1vQCHQh-DwbQf1-rAq_zk77I5-0LpBidpkuYW8LbP0JxYwFxMV6YHD4NNSTlclWIUE7tHNY9O-fSU-mb/pub?gid=0&single=true&output=csv")

    split_data = csv.reader(data.text.split("\n"))

    proc_data = defaultdict(int)

    total = 0

    for row in split_data:
        if row[0] == "date":
            continue
        proc_data[row[0]] = proc_data[row[0]] + 1
    
    ret_data = []

    for key in proc_data.keys():
        total += proc_data[key]
        ret_data.append({"date": key, "cases": total})

    print(ret_data)

    return jsonify(ret_data)

# Serve React App
@app.route("/")
async def serve():
    return await render_template("index.html")

if __name__ == "__main__":
    app.run()