# logs

This is a project I created to analyze data from access logs. It displays several things from the log, such as: 
* an adress with the highest number of requests
* an dress that requested the largest amount of data
* an adress with the largest number of requests per unit of time
* the most requested page
* the page that haven't been requested longer than any, but still exist
* pages that were requested but don't exist


## Launch

To run the programm, you need to copy the log file to your current working directory and type in the command line
```
python 3 main.py filename 
```

Additionally, if you want to analyze files outside of your current working directory, you need to type 
```
python 3 main.py filename -D directory
```
By default this project displays the first 10 non-existing pages. If you want to see more (or less) pages, you need to type
```
python 3 main.py filename -n number
```
