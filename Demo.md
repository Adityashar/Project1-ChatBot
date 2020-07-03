# Demo 

### As a part of the demo, I'll be demonstrating the following three queries :

##### 1. Question / Answer based queries with contextual follow ups
```
Give me the payment status for the agreement with id 105102

what is the pending amount ? 

what was the payment date ?

Tell me the source for info ?
```

##### 2. Timeframe based query retrieval
```
Give me the clients whose payments got rejected in the last month

Show me more info.
```

##### 3. Dynamic Updation - First upload new data, model trains, query over new data

First a table is created in database thtough dataload.py
Then Files - domain.yml, actions.py, stories.md, nlu.md are updated
Finally the model is trained through train.py and the backend needs to be restarted

```
For the id AGFS, whats the ipo year?

And the establishment associated?
```
