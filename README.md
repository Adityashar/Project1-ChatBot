# Project 1

### Problem Statement : 
The current project have data available in different sources like confluence, excels, emails, Jira and off course database. The idea is to train the model from the data available in each of these sources. You will be provided with some sample data from each of these data sources which you will use to train the model. You are free to choose any ML algorithm. The algorithm should give a very low error rate. The following is expected from the system:
 
1. The system should be capable enough to train itself from different type of data source formats e.g. JSON, excel, txt etc.
2. When the end user ask any specific question the system should be able to identify its source and display the result accordingly
3. The system should also be able to interact with the DB if required.
4. The system should be able handle contextual questions i.e. questions asked from the previous answer.
5. Accept new dataset files and dynamically train the model

### Solution Approach:
Development of a chatbot which can handle intellectual user queries, context based conversations, query retrievals from a database, dynamic training on provision of new data and is integrated with a webapp for final submission.

#### Technology used for the development:
For the development of the bot-system, we used Pandas, Numpy, Spacy, Tensorflow and Rasa with a Flask backend.
>Rasa is an open source conversational AI used for building assistants and chatbots in text and voice with machine learning backend.

## Installation

Clone the repository. (We are assuming you have python version 3.6.x and pip & anaconda are installed on your linux system)
(Optional)If not, please use the below command, this will create a new environment using conda.

```sh
conda create -n env python=3.6
conda activate env
```
All dependencies can be installed via:
```sh
pip install -r requirements.txt
```
NOTE: If you have MemoryError in the install try to use:
```
pip3 install -r requirements.txt --no-cache-dir
```
In order to run the system, in three separate terminals execute the following commands::
1. Run the Flash server.
```
cd Project1-ChatBot/citibot/
python Backend/app.py
```
2. Activate the Shell.
```
cd Project1-ChatBot/citibot/
conda activate env
rasa run -m models --enable-api --cors "*" --debug 
```
3. Activate the action server.
```
cd Project1-ChatBot/citibot/
conda activate env
rasa run actions
```
#### Once done, on a browser open *localhost:5000*. Chatbot appears at the bottom right corner, Ask your queries as needed!
