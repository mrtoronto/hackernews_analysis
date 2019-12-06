# hackernews_analysis

![](https://i.imgur.com/OUUrie3.png)

## Program Goal

As a HackerNews reader, I was thinking about how I could extract information from Hackernews more efficiently than simply reading. 

To help me do this, I wrote a scraper to gather articles and associated meta-data from the [HackerNews API](https://github.com/HackerNews/API). 

## Current Function

The scraper is functional and has been used to pull ~100,000 "items" which included ~25,000 posts and ~75,000 comments.

The current analysis notebook was built using only these first 100,000 events so the results are heavily skewed toward early HackerNews posts. 

## To Do

### Data
  - Pull the remainder of the ~20,000,000 items
    - This [API call](https://hacker-news.firebaseio.com/v0/maxitem.json?print=pretty) will return the current maxitem number. 
  - Pull other types of items. 
    - Other item types include polls, poll options and jobs.
    - Currently ignoring items that aren't stories or comments but all three of the other options could lead to interesting analyses. 

### Analysis
  - Identify long-term popular users and plot their scores over time. 
  - See if you can identifier YC Alum's YC tenure using their Hackernews posts. 
  - Track linked sites origin's over time.
  - Analyze post titles and comments more thoroughly.
    - Common N-Grams
    - TF-IDF values
    - Correlation between certain N-Grams and score? 
  - Pulling jobs data could open up a whole new area of analysis.
    - Find N-Grams correlated with a highly scored job posting to help make better job posts in the future.
