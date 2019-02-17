import os
import pytest
from src.simulation import FacilityAssignment

YIELD_FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'output/yield.csv')
ASSIGNMENT_FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'output/assignments.csv')


@pytest.fixture
def loan_csv():
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'small', 'loans.csv'), 'r') as loan_data:
        lines = loan_data.read().split('\n')
    return lines


def test_simualtion(loan_csv):
    assignment = FacilityAssignment()
    for line in loan_csv[1:-1]:
        interest_rate, amount, id, default_likelihood, state = line.split(',')
        assignment.simulation(float(interest_rate), int(amount), id, float(default_likelihood), state)
    assert False


