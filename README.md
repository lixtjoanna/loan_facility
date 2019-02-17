## Basic Info
### Env setup

1. Download Miniconda
2. run `conda env create -f environment.yaml`
3. `source activate loan-simu`

### To replay the output files
`PYTHONPATH=.:src/:test/ python src/simulation.py`

### Run testcases

`DEV_PLAN=1 PYTHONPATH=.:src/:test/ pytest test -vv -x`

Note: if the app does not sence the env variable 'DEV_PLAN' 
this program will load data from 'large' folder

## About the exam

Thank you for this incredible exam, it was the best interview i've take so ever. 
However I have to admit that after a lot of debugging the yields.csv value for facility 1 is still not matching with the answer.
I hope that the answer was wrong. `1,16375` should be changed to `1,16373`



