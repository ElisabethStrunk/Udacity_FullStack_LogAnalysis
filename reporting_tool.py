#!/usr/bin/env python3
"""
Reporting Tool

This is a tool to create reports concerning our newspaper website.
Each report is saved in a new text file.

FOR INTERNAL USE ONLY!
"""

import psycopg2
import datetime
import sys


__author__ = "Elisabeth M. Strunk"
__version__ = 1.1
__maintainer__ = "Elisabeth M. Strunk"
__email__ = "elisabeth.maria.strunk@gmail.com"
__status__ = "Development"


def run_query(query):
    '''
    Run a query on the "news" database
    :param query: string containing the query's SQL statement
    :return: Query result
    '''
    try:
        db = psycopg2.connect("dbname=news")
    except psycopg2.Error as e:
        print("Unable to connect to news database!")
        print(e.pgerror)
        print(e.diag.message_detail)
        sys.exit(1)
    else:
        cursor = db.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        db.close()
        return result


def find_top_three_articles():
    '''
    Investigate popularity of articles
    Find top 3 (most viewed) articles - by title
    Query design:
        1) Join the articles table with the article_log view to get the
           connection between url and article title
        2) Count the number of log entries for each article and sort by the
           number of entries/views
        3) Select only the 3 highest-ranking articles
    :return: Query result containing title and number of views for the top
             3 articles
    '''
    query = "SELECT articles.title, count(*) AS num_views " \
            "FROM article_log " \
            "RIGHT JOIN articles " \
            "ON articles.slug = article_log.url " \
            "GROUP BY articles.title " \
            "ORDER BY num_views DESC " \
            "LIMIT 3;"
    return run_query(query)


def find_views_per_author():
    '''
    Investigate popularity of authors
    Find number of article views per author
    Query design:
        1) Join the authors table with the articles table to get the
           connection which author wrote which article
        2) Add the article_log view to the join where the article's slug
           matches the log entry's url to get the
           connection which log entry belongs to which author
        3) Count the number of log entries for each author and sort by the
           number of entries/views
    :return: Query result containing name and number of views for all authors
    '''
    query = "SELECT authors.name, count(*) AS num_views " \
            "FROM authors " \
            "LEFT JOIN articles " \
            "ON (authors.id = articles.author) " \
            "LEFT JOIN article_log " \
            "ON (articles.slug = article_log.url) " \
            "GROUP BY authors.name " \
            "ORDER BY num_views DESC;"
    return run_query(query)


def find_error_riddled_days():
    '''
    Investigate error-riddled days
    Find days with an error percentage > 1%
    Query design:
        1) Get a table containing all days with their total number of
           requests (request_query)
        2) Get a table containing all days with their number of errors
           (error_query)
        3) Join these two table to derive a list containing all days with
           their error percentage (percentage_query)
        4) Select only those entries in the percentage_query table where the
           error percentage is > 1 and sort by day
    :return: Query result containing date and error percentage of all days
             with an error percentage > 1%
    '''
    query = "SELECT day, error_percentage " \
            "FROM (" \
            "    SELECT request_query.day, " \
            "           (100.0*num_errors/(1.0*num_total)) " \
            "           AS error_percentage " \
            "    FROM ( " \
            "        SELECT date(time) AS day, count(*) AS num_total " \
            "        FROM log " \
            "        GROUP BY day " \
            "    ) AS request_query " \
            "    LEFT JOIN ( " \
            "        SELECT date(time) AS day, count(*) AS num_errors " \
            "        FROM log " \
            "        WHERE (status LIKE '4%') OR (status LIKE '5%') " \
            "        GROUP BY day " \
            "    ) AS error_query " \
            "    ON request_query.day = error_query.day " \
            ") AS percentage_query " \
            "WHERE error_percentage > 1.0 " \
            "ORDER BY day;"
    return run_query(query)


if __name__ == '__main__':
    output_file = "report-{}.txt".format(datetime.datetime.now().
                                         strftime("%m-%d-%Y-%H-%M-%S"))

    print("\n\nReport is being created...")

    with open(output_file, 'w') as f:
        print("------------------", file=f, end='\r\n')
        print("----- REPORT -----", file=f, end='\r\n')
        print("------------------", file=f, end='\r\n')
        print(datetime.datetime.now().strftime("%B %d, %Y - %H:%M:%S"),
              file=f, end='\r\n')
        print("\n", file=f, end='\r\n')
        print("...")  # output to terminal so signal process
        print("1. What are the most popular three articles of all time?",
              file=f, end='\r\n')
        for article in find_top_three_articles():
            print('    "{}" - {} views'.format(article[0], article[1]),
                  file=f, end='\r\n')
        print("\n", file=f, end='\r\n')
        print("...")  # output to terminal so signal process
        print("2. Who are the most popular article authors of all time?",
              file=f, end='\r\n')
        for author in find_views_per_author():
            print('    {} -- {} views'.format(author[0], author[1]),
                  file=f, end='\r\n')
        print("\n", file=f, end='\r\n')
        print("...")  # output to terminal so signal process
        print("3. On which days did more than 1% of requests lead to errors?",
              file=f, end='\r\n')
        for day in find_error_riddled_days():
            print('    {} -- {}% errors'.format(day[0].strftime("%B %d, %Y"),
                                                round(day[1], 1)),
                  file=f, end='\r\n')
        print("\n", file=f, end='\r\n')
        f.close()

    print("Report was created and stored in file {}\n\n".format(output_file))
else:
    print("reporting_tool is imported by another module.")
