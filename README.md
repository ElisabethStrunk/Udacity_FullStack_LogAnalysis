# Udacity_FullStack_LogAnalysis
Log analysis project of the Udacity Full Stack Web Developer Nanodegree Program
___
Scenario:
You've been hired onto a team working on a newspaper site. The user-facing newspaper site frontend itself, and the database behind it, are already built and running. You've been asked to build an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like.
___

Elisabeth Maria Strunk, 07-27-2019

# Reporting Tool
<span style="color:red">FOR INTERNAL USE ONLY!</span>

This is a tool to create reports concerning our newspaper website.
Each report is saved in a new text file.
## Prerequisites
### System
This tool is designed to run on a system with the following characteristics:
+ Linux operating system
+ python 3 installed
+ postgreSQL running
+ containing our _news_ database
### Preparation
Before using the tool for the first time, please run the following SQL statement on our _news_ database to create necessary views.
```
CREATE VIEW article_log AS
SELECT log.id, REPLACE(log.path, '/article/', '') AS url, log.status, log.time
FROM log, articles
WHERE REPLACE(log.path, '/article/', '') = articles.slug;
```
Note that the reporting tool will not function properly, if this view has not been created!
## How To Use The Reporting Tool
To run the reporting tool...
1. Transfer the python script _reporting_tool.py_ to the directory you want to store the reports in (_reporting directory_ in the following).
2. Open a bash session.
3. Navigate to the reporting directory.
4. Run _reporting_tool.py_ with
    ```
    $>  ./reporting_tool.py
    ```
5. Observe the progress; the tool will print a notification once the report has been successfully created.
6. Find the report in the reporting directory in the text file with the name _report-[date]-[time]_.
## For Maintainers
The following provides a short description of the program's design.

There are 4 functions:
+ run_query
+ find_top_three_articles
+ find_views_per_author
+ find_error_riddled_days

For each function a function header with detailed information is provided in-code. This header also contains a description of the query design.

The report file is generated and populated using print() and the results of calling the fore-mentioned functions successively.
