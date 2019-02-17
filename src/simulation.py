import pandas as pd
import os
import logging
DEV_PLAN = True if 'DEV_PLAN' in os.environ else False
file_source = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'small' if DEV_PLAN else 'large')
YIELD_FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'output/yield.csv')
ASSIGNMENT_FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'output/assignments.csv')


class FacilityAssignment(object):
    bank_and_facility_df = None

    def __init__(self):
        self.pre_process()
        self.__create_file()

    def __create_file(self):
        output_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'output')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(YIELD_FILE_PATH, 'w') as yield_data:
            yield_data.write('facility_id,expected_yield\n')
        with open(ASSIGNMENT_FILE_PATH, 'w') as assignment_data:
            assignment_data.write('loan_id,facility_id\n')

    def pre_process(self):
        """join bank, facility and covenat table"""
        facilities_df = pd.read_csv('{}/facilities.csv'.format(file_source))
        banks_df = pd.read_csv('{}/banks.csv'.format(file_source))
        covenants_df = pd.read_csv('{}/covenants.csv'.format(file_source))

        # groupby facility id
        covenants_df = covenants_df.groupby('facility_id').agg({
            'max_default_likelihood': 'sum',
            'banned_state': lambda x: tuple(x)
        })

        # inner join facility table and covenant table with facility id
        self.bank_and_facility_df = facilities_df.join(covenants_df, on=['id'])

        # join the data frame with bank name
        # also rename some columns for better human understanding
        self.bank_and_facility_df = self.bank_and_facility_df \
            .join(banks_df.set_index(['id']), on=['bank_id']) \
            .rename(columns={'name': 'bank_name', 'id': 'facility_id'})
        self.bank_and_facility_df['banned_state'] = self.bank_and_facility_df.banned_state
        return self.bank_and_facility_df

    def simulation(self, loan_interest_rate, amount, id, default_likelihood, state):
        """
        This selection is based on the rule of :
            facility has more than amount of capacity
            not in list(tuple) of banned state
            default likelihood is smaller than max
            Affirm will make money from the difference of interest
        """
        df_cur = self.bank_and_facility_df[(self.bank_and_facility_df.amount >= amount) &
                                           (self.bank_and_facility_df.max_default_likelihood > default_likelihood) &
                                           (self.bank_and_facility_df.interest_rate < loan_interest_rate) &
                                           (self.bank_and_facility_df.banned_state.apply(lambda y: state not in y))]
        if not df_cur.empty:
            facility = df_cur.sort_values(by=['interest_rate']).iloc[0]
            facility_id, facility_interest_rate = facility['facility_id'], facility['interest_rate']
            expected_yield = int((1 - default_likelihood) * loan_interest_rate * amount - \
                             default_likelihood * amount - \
                             facility_interest_rate * amount)

            self.__write_to_file(str(facility_id), str(id), str(expected_yield))
            self.__reduce_amount_from_facility(facility_id, int(amount))
        else:
            logging.warning('No facility found')

    def __write_to_file(self, facility_id, loan_id, expected_yield):
        with open(YIELD_FILE_PATH, 'a') as yield_data:
            yield_data.write(facility_id + ',' + expected_yield + '\n')
        with open(ASSIGNMENT_FILE_PATH, 'a') as assignment_data:
            assignment_data.write(loan_id + ',' + facility_id + '\n')

    def __reduce_amount_from_facility(self, facility_id,  value):
        self.bank_and_facility_df[self.bank_and_facility_df.facility_id == facility_id]['amount'] = self.bank_and_facility_df[self.bank_and_facility_df.facility_id == facility_id]['amount'] - value
