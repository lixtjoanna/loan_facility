import os
import pytest
from src.simulation import FacilityAssignment

YIELD_FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'output/yields.csv')
ASSIGNMENT_FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'output/assignments.csv')

TARGET_YIELD_FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'small/yields.csv')
TARGET_ASSIGNMENT_FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'small/assignments.csv')

@pytest.fixture
def loan_csv():
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'small', 'loans.csv'), 'r') as loan_data:
        lines = loan_data.read().split('\n')
    return lines[:-1]


def test_simualtion(loan_csv):
    if 'DEV_PLAN' not in os.environ:
        assert False, 'Please run pytest with export DEV_PLAN'
    assignment = FacilityAssignment()
    for line in loan_csv[1:]:
        interest_rate, amount, id, default_likelihood, state = line.split(',')
        assignment.simulation(float(interest_rate), int(amount), id, float(default_likelihood), state)

    with open(YIELD_FILE_PATH, 'r') as data:
        lines = data.read()
        with open(TARGET_YIELD_FILE_PATH,'r') as target:
            target_lines = target.read()
            assert lines[:-1] == target_lines

    with open(ASSIGNMENT_FILE_PATH, 'r') as data:
        lines = data.read()
        with open(TARGET_ASSIGNMENT_FILE_PATH,'r') as target:
            target_lines = target.read()
            assert lines == target_lines
