from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

import adv

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/adv', methods=['GET', 'POST'])
def dispose_adv():
    input1 = request.form.get("input1")
    input2 = request.form.get("input2")
    print('input start')
    print(input1)
    result = {}
    output = adv.main(input1, input2)
    result['status'] = 1
    result['data'] = output

    # try:
    #     output = adv.main(input1, input2)
    # except:
    #     result['status'] = 0
    #     result['data'] = ''
    # else:
    #     result['status'] = 1
    #     result['data'] = output

    return jsonify(result)


@app.route('/')
def index():
    return 'hello'


if __name__ == '__main__':
    app.run(debug=True)
