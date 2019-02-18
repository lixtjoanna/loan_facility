## Basic Info
### Env setup

1. Download Miniconda
2. run `conda env create -f environment.yaml`
3. `source activate loan-simu`

### To replay the output files
`PYTHONPATH=.:src/ python src/simulation.py`
The answer files will be generated into output folder

### Run testcases

`DEV_PLAN=1 PYTHONPATH=.:src/:test/ pytest test -vv -x`

Note: if the app does not sence the env variable 'DEV_PLAN' 
this program will load data from 'large' folder

### Run demo app
`PYTHONPATH=.:src/ python app.py`

SAMPLE_RESPONSE
```json
{
    "facility_id": "1",
    "message": "",
    "new_capacity": "1912604.0",
    "new_expect": "4239",
    "status": "SUCCESS"
}
```


## About the exam

**1. How long did you spend working on the problem? What did you find to be the most difficult part?**
    
I spend nearly 3 hrs for my first version running the sample data set(small). 
Data exploration and use case understanding took me a lot of time. 
As well as a lot of details includes 
    
  - data operation(join, merge, groupby)
  - python: int(round(float))
  - oop
  - ..
  
each of these all needs to be very carefully processed.

**2. How would you modify your data model or code to account for an eventual introduction of new, as-of-yet unknown types of covenants, beyond just maximum default likelihood and state restrictions?**
    
To add a new covenant, I think it might be a good idea to use python's functional programing,
which the selection of the code could be changed to a function and pass to the simulation method as a input.  

**3. How would you architect your solution as a production service wherein new facilities can be introduced at arbitrary points in time. Assume these facilities become available by the finance team emailing your team and describing the addition with a new set of CSVs.**
    
I need to introduce a new method inorder to add information of new facility. 
Luckily, i designed this class with a class varilabe `bank_and_facility_df` and this variable will be editable
through a new method.  

As for the production level improvement, the whole dataframe was kept in memory, which could be too heavy. 
This can be replaced with a Radius like in memory data storage with good performace.
  
**4. Your solution most likely simulates the streaming process by directly calling a method in your code to process the loans inside of a for loop. What would a REST API look like for this same service? Stakeholders using the API will need, at a minimum, to be able to request a loan be assigned to a facility, and read the funding status of a loan, as well as query the capacities remaining in facilities.**

Suppose: All the loans are submitted one by one (not stored anyway, stream process)
    
- submit loan:  `POST` /newloan (included in this version)
- get loan status: `GET` /loan/<loan-id>
- get all loan status: `GET` /loan
- add facility: `POST` /facility
- get facility status: `GET` /facility/<facility-id>
- get all facility status: `GET` /facility

**5. How might you improve your assignment algorithm if you were permitted to assign loans in batch rather than streaming? We are not looking for code here, but pseudo code or description of a revised algorithm appreciated.**

- We can save the facility table using heap(index = interest_rate)
- Group loans by states and sort by default_likelihood and secondly by descending intereste rate
- when calculating the expected_yield, the number does not have to be calculated everytime

**6. Discuss your solution’s runtime complexity.**
My current logic's runtime is slowed down by heavily writing into the output files. 
Expect the i/o time consumption, here is my runtime complexity analyze.

- pre_process method:
  - groupby: O(n)
  - left_join: O(m+n) (m, n number of rows in left and right)
  - selections: O(n)
  - over_all : O(m+n)
- simulation method:
   - sort: O(mlogm) (m is smaller than the whole dataset) -> O(1)
   - selections: O(n) (n is the number of qualified facilities)
   - over_all: O(n)
   