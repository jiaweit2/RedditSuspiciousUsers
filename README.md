## Reddit Suspicious User Account Detection

### Approach
The random forest algorithm is used here. Based on this [reddit report](https://www.reddit.com/r/announcements/comments/8bb85p/reddits_2017_transparency_report_and_suspect/), a list of suspicious accounts that are marked by Reddit can be found [here](https://www.reddit.com/wiki/suspiciousaccounts). After training this suspicious accounts along side with some normal user accounts(training set size ≈ 1000), we then can generate a random forest which can be used to predict whether a user account is suspicious or not.

### Features
The features used in the random forest is as follows:
1. Average Link Karma per day (float)
1. Average Comment Karma per day (float)
1. if Email Verified (boolean)
1. if gold (boolean)

### Usage
To use, you need to feed your reddit developer information in config.py.
Then you can run
```
python classifier.py [username]
```

