# Vanguard Data Analysis of Web New Portal

### By Alex Lopez


## Project Overview
In 2017, Vanguard (investment firm) performed an A/B experiment to test their new website design.
Over the course of 3 months from March 15 to June 20th, they collected data, giving clients instructions
to complete 4 steps and reach a confirmation page.

Now in IronHack data analytics bootcamp for Spring 2024, I needed to analyze their data from the experiment
and find out whether or not the new web design did actually perform better than the old one.


## DATASETS
Data was split into 3 key parts
- Client Profiles (df_final_demo): Demographics like age, gender, and account details of our clients.
- Digital Footprints (df_final_web_data): A detailed trace of client interactions online, divided into two parts: pt_1 and pt_2.
- Experiment Roster (df_final_experiment_clients): A list revealing which clients were part of the grand experiment

The untouched data is in the datasets folder, with cleaned csv versions in the cleaned dataset folder

## FINDINGS
You can view my full findings in my powerpoint presentation located at the presentation folder

To summarize:

- Found that while there was a statistically significant increase in completion rates for the test group, 
it wasn't enough of an increase to justify cost of maintenance(didn't reach cost threshold diff of 5 %)

- Also found that overall the test group took longer to complete each step and made more errors in the process 
than the control group

- Found issues with the experiment regarding client age across the groups and gender breakdown for their age and tenure.
  This indicates that a repeat of the experiment would've been necessary and try to minimize these biases.
  
- Repeat of the experiment will need more context data in terms of how clients interacted with the website design,
  and measurable aggregated feedback from a feedback survey.
 

## CODE
You can view my code regarding my findings and visualizations in the final data python notebook with utility
functions in the util functions folder.

## TABLEAU
Also included some visualizations regarding my analysis in the packaged tableau workbook under the tableau folder

## Trello
Link to my board:
https://trello.com/invite/b/L0ZDIqbi/ATTIc9f40e4bfef9eb7a11da6a6464f4a693C44894AD/week-5-da-ironhack-alone



  



