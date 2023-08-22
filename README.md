# Hypothesis testing project on YouTube football fan channels
A project to investigate if football fan channels profit from team failure. A link to the medium article is available [here](https://medium.com/@dare15802/do-football-fan-channels-profit-from-team-losses-cf385d14cc94)

### Data Extraction files
- main.py: main file for retrieving data from YT API.
- etl/extract.py: gets data from API and ouputs json files in data folder.
- etl/transform.py: output csv with title, date, likes, comments, etc.
- data folder: contains raw json files from api and csvs output by transform.py.

### Data analysis files
Files contained in the analyse folder
- preprocess.py: gets scores and formats data. Stores csv output in data folder.
- data_analysis.ipynb: create plots of views and likes over time, look at summary statistics.
- ab_test.ipynb: create distribution plots. Perform A/B test.
