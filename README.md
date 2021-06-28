# Zillow Clustering Project
#### Tyler Applegate, Florence Cohort
#### 2021_06_28

### Project Summary

#### Project Description:

What variables are driving logerror in the Zillow Zestimates?

For this project, I am working with the 2017 Zillow dataset, focusing on single unit / single-family homes.

This notebook will be a continuation of initial regression modeling. We are adding clustering to see what kind of improvements we can make.

#### Project Goals:
- Use clustering methodologies to identif drivers of logerror in Zillow Zestimates
- Create modules storing functions of each step of the data pipeline
- Thoroughly document each step
- Construct at least 4 models, 1 of which must outperform the baseline
- Make sure project is reproduceable

#### Project Deliverables:
- Final Report Notebook detailing all of my findings and methodologies
- Modules commented out with appropriate functions to replicate each stage of the DS pipeline
- README file that details the project specs, planning, key findings, and steps to reproduce

#### Project Planning:
- Write a SQL query, and put in function to acquire data from Zillow dataset on Codeup database
- Create a prepare.py module complete with all necessary functions to clean the data
- Use visualizations and statistical testing to explore relationships between variables and logerror
- Use key variables to create clusters, and perform statistical testing on clusters to see if they are useful
- Establish a baseline model, and compute its RMSE
- Use key variables and clusters to create 4 models, with the aim of outperforming the baseline
- Use best model on test data
- draw conclusions at each step of the pipeline
- Include next steps / if I had more time...

#### Project Context:
- This data came from the Zillow dataset in the Codeup Database

#### Data Dictionary:

|Target|Datatype|Definition|
|:-------|:-------|:----------|
|logerror|51897 non-null: float64|How far over/under the Zestimate is from assessed value|

|Feature|Datatype|Definition|
|:-------|:-------|:----------|
|bathroomcnt|float64|Number of bathrooms|
|bedroomcnt|float64|Number of bedrooms|
|calculatedbathnbr|float64|Number of bathrooms and bedrooms|
|calculatedfinishedsquarefeet|float64|structure size in sqft|
|fips|float64|Federal Information Processing Standards, unique county code|
|fullbathcnt|float64|Whole number of bathrooms|
|latitude|float64|Property latitudinal location|
|longitude|float64|Property longitudinal location|
||lostsizesquarefeet|float64|Size of entire property in sqft|
|roomcnt|float64|Number of rooms in structure|
|taxamount|float64|Taxes assessed in Dollars|
|LA|uint8|Identifies if property is in LA County|
|Orange|uint8|Identifies if property is in Orange County|
|Ventura|uint8|Identifies if property is in Ventura County|
|age|float64|How old the home is in years|
|taxrate|float64|taxamount / assessed value|
|acres|float64|Size of entire property in acres|
|bath_bed_ratio|float64|Ratio of bathrooms to bedrooms|

#### Initial Hypothoses:
- Hypothosis 1 - We fail to reject the null hypothesis
- ${H_O}$: There is no difference in mean logerror between bathroomcnt <=1, and mean logerror of all bathroom counts.
- ${H_a}$: There is a difference in mean logerror between bathroomcnt <=1, and mean logerror of all bathroom counts.
- alpha = 0.05

- Hypothosis 2 - We reject the null hypothesis
- ${H_O}$: There is no difference in mean logerror between bedroomcnt <=3, and mean logerror of bedroomcnt > 3
- ${H_a}$: There is a difference in mean logerror between bedroomcnt <=3, and mean logerror of bedroomcnt > 3
- alpha = 0.05

- Hypothosis 3 - We reject the null hypothesis
- ${H_O}$: There is no relationship between latitude and logerror, (they are independent variables.)
- ${H_a}$: There is a relationship between latitude and logerror, (they are dependent variables.)
- alpha = 0.05

- Hypothosis 4 - We reject the null hypothesis
- ${H_O}$: There is no relationship between longitude and logerror, (they are independent variables.)
- ${H_a}$: There is a relationship between longitude and logerror, (they are dependent variables.)
- alpha = 0.05

#### Key Findings & Takeaways:
- Many variables appear to play a role in logerror
- Have yet to find a single 'smoking gun' variable

#### How to Reproduce:
You will need your own env file with database credentials to pull the Zillow dataset from the Codeup Database

-[] Read this README.md
-[] download acquire.py, prepare.py, explore.py, and final_report.ipynb into your working directory
-[] Run the final_report.ipynb Jupyter Notebook




