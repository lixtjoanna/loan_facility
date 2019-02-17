from flask import Flask
from flask import json,request
from src.simulation import FacilityAssignment

simulation = FacilityAssignment()

app = Flask(__name__)


@app.route("/newloan", methods=['POST'])
def new_loan():
    if request.method == 'GET':
        response = app.response_class(
            response=json.dumps({
                'status':'FAILED',
                'message': 'Only allows get response'
            }),
            status=405,
            mimetype='application/json'
        )
        return response

    for item in ['interest_rate', 'amount', 'id', 'default_likelihood', 'state']:
        if item not in request.headers:
            response = app.response_class(
                response=json.dumps({
                    'status': 'FAILED',
                    'message': '%s is missing in the request' % item
                }),
                status=400,
                mimetype='application/json'
            )
            return response
    interest_rate = request.headers['interest_rate']
    amount = request.headers['amount']
    id = request.headers['id']
    default_likelihood = request.headers['default_likelihood']
    state = request.headers['state']
    res = simulation.simulation(float(interest_rate), int(amount), id, float(default_likelihood), state)

    if res:
        facility_id, new_expect, new_capacity = res
        response = app.response_class(
            response=json.dumps({
                'status': 'SUCCESS',
                'message': '',
                'facility_id': facility_id,
                'new_expect': new_expect,
                'new_capacity': new_capacity
            }),
            status=200,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=json.dumps({
                'status': 'FAILED',
                'message': 'Insufficient data'
            }),
            status=500,
            mimetype='application/json'
        )
    return response


if __name__ == '__main__':
    app.run()