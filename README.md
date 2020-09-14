# linkedin

This projects contains:

- A bot that extracts the data job details and creates a csv that saves that info

- A text analyzer to search specific key words in the text

To avoid anti-bot measures from linkedin the text job extraction is done with the user not signed in.
Due to this reason, a maximum of 1000 jobs can be extracted based on linekedin specifics at the same
time. 

The total amount of time 0.0375*number_of_jobs + 1.5  (minutes)

Command to activate mongo /c/Users/Sectorea/mongodb/bin/mongod.exe --dbpath=/c/Users/Sectorea/mongodb-data/

Command to make a backup /c/Users/Sectorea/mongodb/bin/mongoexport.exe --uri="mongodb+srv://jobs:f4Uo1b3ziIAhpPMf@cluster0-79fkx.mongodb.net/jobs?retryWrites=true&w=majority"  --collection=linkedins  --out=back-up_2.json 

The node.js data science scraping task is launch like 
node data_science.js node --max-old-space-size=2048 datasciences.js --key_words="data science" --location="Switzerland" --time_range="Past Month" . T
The flag of --max-old-space-size is necessary only in case the memory in that task is below the capacities, for example, in a virtual machine maybe its necessary to increase the ram memory. This issue is based on the default memory use by any node task of 1024mb as ram, so in case the task requires more it fails. 

When 30000 jobs are reached, due to memory limitations, some process from the .py tasks cannot be performed. In the mongo.ipynb there is a task that saves as csv some part of the dataset and deletes that part to enable keep working.
