import pandas as pd
import os

DEV_PLAN = True if 'DEV_PLAN' in os.environ else False
file_source = 'small' if DEV_PLAN else 'large'
YIELD_FILE_PATH = 'output/yield.csv'
ASSIGNMENT_FILE_PATH = 'output/assignments.csv'


class FacilityAssignment(object):
    bank_and_facility_df = None

    def __init__(self):
        self.pre_process()
        self.__create_file()

    def __create_file(self):
        with open(YIELD_FILE_PATH, 'w') as yield_data:
            yield_data.write('facility_id,expected_yield')
        with open(ASSIGNMENT_FILE_PATH, 'w') as assignment_data:
            assignment_data.write('loan_id,facility_id')

    def pre_process(self):
        """join bank, facility and covenat table"""
        facilities_df = pd.read_csv('{}/facilities.csv'.format(file_source))
        banks_df = pd.read_csv('{}/banks.csv'.format(file_source))
        covenants_df = pd.read_csv('{}/covenants.csv'.format(file_source))

        # inner join facility table and covenant table with facility id
        self.bank_and_facility_df = facilities_df.join(covenants_df.set_index(['facility_id']),
                                                       on=['id'], lsuffix='_f', rsuffix='_c')

        # remove lines where bank id doesn't match
        # (in case there are errors in the input)
        self.bank_and_facility_df = self.bank_and_facility_df[
            self.bank_and_facility_df.bank_id_c == self.bank_and_facility_df.bank_id_f]

        # join the data frame with bank name
        # also rename some columns for better human understanding
        self.bank_and_facility_df = self.bank_and_facility_df \
            .join(banks_df.set_index(['id']), on=['bank_id_c']) \
            .rename(columns={'name': 'bank_name', 'id': 'facility_id'})
        self.bank_and_facility_df = self.bank_and_facility_df.drop(columns=['bank_id_f', 'bank_id_c'])

        return self.bank_and_facility_df

    def simulation(self, loan_interest_rate, amount, id, default_likelihood, state):
        """
        This selection is based on the rule of :
            facility has more than amount of capacity
            not in list of banned state
            default likelihood is smaller than max
            Affirm will make money from the difference of interest
        """

        df_cur = self.bank_and_facility_df[(self.bank_and_facility_df.amount >= amount) &
                                           (self.bank_and_facility_df.banned_state != state) &
                                           (self.bank_and_facility_df.max_default_likelihood > default_likelihood) &
                                           (self.bank_and_facility_df.interest_rate < loan_interest_rate)]

        if df_cur:
            facility = df_cur.sort_values(by=['interest_rate']).iloc[0]
            facility_id, facility_interest_rate = facility['facility_id'], facility['interest_rate']

            expected_yield = (1 - default_likelihood) * loan_interest_rate * amount - \
                             default_likelihood * amount - \
                             facility_interest_rate * amount

            self.write_to_file(facility_id, id, expected_yield)

    def write_to_file(self, facility_id, loan_id, expected_yield):
        with open(YIELD_FILE_PATH, 'w+') as yield_data:
            yield_data.write(facility_id, expected_yield)
        with open(ASSIGNMENT_FILE_PATH, 'w+') as assignment_data:
            assignment_data.write(loan_id, facility_id)

    def __reduce_amount_from_facility(self, value):
        self.bank_and_facility_df['facility_id']['amount'] -= value
