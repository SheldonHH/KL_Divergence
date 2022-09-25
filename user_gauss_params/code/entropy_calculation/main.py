from flask import Flask, request
import json
from gauss_entropies import ga_entropy
from benchmark_entropies import be_entropy
app = Flask(__name__)



@app.route('/bgePercent', methods=['POST'])
async def index():
    if request.method == 'POST':
        task_content = request.data
        user_dict = json.loads(task_content)
        await db_bege(user_dict)
        return 1
     
async def db_bege(user_dict):
    be_entropy(user_dict)
    ga_entropy(user_dict)


# POD protocol client to specify the data rows belongs to each user
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5920)
