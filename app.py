from flask import Flask, jsonify, request, render_template
from redis import Redis
import json

app = Flask(__name__)
# Konfiguracja połączenia z Redis
redis = Redis(host='redis', port=6379, db=0, decode_responses=True)

# Przechowuje listy zadań; klucze to nazwy list, a wartości to listy zadań
lists = {}

@app.route('/')
def home():
    # Renderowanie strony głównej z pliku templates/index.html
    return render_template('index.html')

@app.route('/lists', methods=['GET'])
def get_lists():
    # Zwraca listę dostępnych list zadań
    return jsonify(list(lists.keys()))

@app.route('/lists', methods=['POST'])
def create_list():
    list_name = request.json.get('name')
    if list_name in lists:
        return jsonify({'error': 'List already exists'}), 400
    lists[list_name] = []
    # Nie trzeba aktualizować Redis tutaj, ponieważ lista jest pusta
    return jsonify({'message': 'List created successfully'}), 201

@app.route('/tasks/<list_name>', methods=['GET'])
def get_tasks(list_name):
    # Sprawdza cache Redis dla listy zadań
    cached_tasks = redis.get(list_name)
    if cached_tasks:
        tasks = json.loads(cached_tasks)
    else:
        tasks = lists.get(list_name, [])
        redis.set(list_name, json.dumps(tasks), ex=60)  # Zapisuje do Redis z wygaśnięciem 60 sekund
    return jsonify({'tasks': tasks})

@app.route('/tasks/<list_name>', methods=['POST'])
def add_task(list_name):
    task_content = request.json.get('task')
    if list_name not in lists:
        return jsonify({'error': 'List not found'}), 404
    task = {
        'id': len(lists[list_name]),
        'task': task_content,
    }
    lists[list_name].append(task)
    # Aktualizuje listę w Redis po dodaniu zadania
    redis.set(list_name, json.dumps(lists[list_name]), ex=60)
    return jsonify(task), 201

@app.route('/tasks/<list_name>/<int:task_id>', methods=['DELETE'])
def delete_task(list_name, task_id):
    if list_name in lists and 0 <= task_id < len(lists[list_name]):
        del lists[list_name][task_id]
        # Aktualizuje listę w Redis po usunięciu zadania
        redis.set(list_name, json.dumps(lists[list_name]), ex=60)
        return jsonify({'message': 'Task deleted successfully'}), 200
    return jsonify({'error': 'Task or list not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
