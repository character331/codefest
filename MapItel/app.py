import json
from time import sleep
from flask import Flask, request, render_template, render_template_string, redirect
from search_engine import search, try_find_cached
import threading
import queue

app = Flask(__name__)
q = queue.Queue()
enqueued = set()

def worker():
    while True:
        if q.empty():
            # print("didn't find work to do, worker sleep 10 sec...")
            sleep(15)
            continue
        else:
            [location, keyword] = q.get()
            print(f'search: {location} - {keyword}')
            search(location, keyword)
            q.task_done()

@app.route('/')
def hello():
    return redirect("/mapintel/search", code=302)

@app.route('/mapintel/search')
def start():
    return render_template('./index.html')


@app.route('/mapintel/wait')
def wait():
    return render_template('./wait.html'), 200


@app.route('/mapintel/result')
def display():
    if request.method == 'GET':
        location = request.args.get('location').lower()
        keyword = request.args.get('keyword').lower()

        cache = try_find_cached(location, keyword)
        if cache:
            print("Render map with config...", cache)
            data = json.load(open(cache, "r"))
            add_content = f'<script>var target = {data["target"]};\n var locations = {data["locations"]}</script>\n'
            template = open('./templates/map.html', "r").read()
            return render_template_string(add_content + template), 200

        else:
            tag = f"{location}-{keyword}"
            if tag not in enqueued:
                print("enqueue!", tag)
                q.put([location, keyword])
                enqueued.add(tag)
            return "please wait. MapIntel is trying to find answer for you...", 400

app.config['DEBUG'] = True

if __name__ == '__main__':
    threading.Thread(target=worker, daemon=True).start()
    app.run(host='0.0.0.0', port=5005)