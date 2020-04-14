# linkedin

This projects contains:

- A bot that extracts the data job details and creates a csv that saves that info

- A text analyzer to search specific key words in the text

To avoid anti-bot measures from linkedin the text job extraction is done with the user not signed in.
Due to this reason, a maximum of 1000 jobs can be extracted based on linekedin specifics at the same
time. 

The total amount of time 0.0375*number_of_jobs + 1.5  (minutes)