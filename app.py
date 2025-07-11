import json
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = 'secret_key'
schedule_list = []  # 予定を一時的に保存するリスト

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        title = request.form['title']
        place = request.form['place']
        note = request.form['note']
        schedule_list.append({'date': date, 'start_time': start_time , 'end_time': end_time, 'title': title, 'place': place, 'note': note})
        return redirect(url_for('index'))
    return render_template('index.html', schedules=schedule_list)

@app.route('/edit/<int:schedule_id>', methods=['GET', 'POST'])
def edit(schedule_id):
    schedule = schedule_list[schedule_id]
    if request.method == 'POST':
        schedule['date'] = request.form['date']
        schedule['start_time'] = request.form['start_time']
        schedule['end_time'] = request.form['end_time']
        schedule['title'] = request.form['title']
        schedule['place'] = request.form['place']
        schedule['note'] = request.form['note']
        return redirect(url_for('index'))
    return render_template('edit.html', schedule=schedule, schedule_id=schedule_id)

@app.route('/calendar')
def calendar():
    events = []
    for i, s in enumerate(schedule_list):
        events.append({
            "id": i,
            "title": s["title"],
            "start": f"{s['date']}T{s['start_time']}",
            "end": f"{s['date']}T{s['end_time']}",
            "description": f"{s['place']} | {s['note']}"
        })
    return render_template('calendar.html', events=events)

if __name__ == '__main__':
    app.run(debug=True, port=3333)