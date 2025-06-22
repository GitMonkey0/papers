from flask import Flask, render_template, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

def load_all_papers():
    all_papers = []
    data_dir = os.path.join(app.root_path, 'data')

    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            path = os.path.join(data_dir, filename)
            with open(path, 'r', encoding='utf-8') as f:
                try:
                    papers = json.load(f)
                    for paper in papers:
                        # 标准化时间字段
                        if isinstance(paper.get("published"), str):
                            paper["published_dt"] = datetime.fromisoformat(paper["published"])
                        else:
                            paper["published_dt"] = datetime.min
                        all_papers.append(paper)
                except Exception as e:
                    print(f"Error reading {filename}: {e}")

    # 按发布时间从新到旧排序
    all_papers.sort(key=lambda x: x["published_dt"], reverse=True)
    return all_papers

@app.route('/')
def index():
    papers = load_all_papers()
    return render_template('index.html', papers=papers)

@app.route('/api/papers')
def api_papers():
    papers = load_all_papers()
    return jsonify(papers)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
