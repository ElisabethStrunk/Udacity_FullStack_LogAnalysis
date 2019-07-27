#!/usr/bin/env python3
"""
TODO: Write short description
"""

import psycopg2
import datetime


__author__ = "Elisabeth M. Strunk"
__version__ = 1.0
__maintainer__ = "Elisabeth M. Strunk"
__email__ = "elisabeth.maria.strunk@gmail.com"
__status__ = "Development"


def run_query(query):
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result


def find_top_three_articles():
    '''
    Investigate popularity of articles
    Find top 3 (most viewed) articles - by title
    :return: Query result containing title and number of views for the top 3 articles
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
    :return: Query result containing date and error percentage of all days with an error percentage > 1%
    '''
    query = "SELECT day, error_percentage " \
            "FROM (" \
            "    SELECT request_query.day, (100.0*num_errors/(1.0*num_total)) AS error_percentage " \
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


output_file = "report-{}.txt".format(datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S"))

print("\n\nReport is being created...")

with open(output_file, 'w') as f:
    print("------------------", file=f, end='\r\n')
    print("----- REPORT -----", file=f, end='\r\n')
    print("------------------", file=f, end='\r\n')
    print(datetime.datetime.now().strftime("%B %d, %Y - %H:%M:%S"), file=f, end='\r\n')
    print("\n", file=f, end='\r\n')
    print("...")  # output to terminal so signal process
    print("1. What are the most popular three articles of all time?", file=f, end='\r\n')
    for article in find_top_three_articles():
        print('    "{}" - {} views'.format(article[0], article[1]), file=f, end='\r\n')
    print("\n", file=f, end='\r\n')
    print("...")  # output to terminal so signal process
    print("2. Who are the most popular article authors of all time?", file=f, end='\r\n')
    for author in find_views_per_author():
        print('    "{}" -- {} views'.format(author[0], author[1]), file=f, end='\r\n')
    print("\n", file=f, end='\r\n')
    print("...")  # output to terminal so signal process
    print("3. On which days did more than 1% of requests lead to errors?", file=f, end='\r\n')
    for day in find_error_riddled_days():
        print('    {} -- {}% errors'.format(day[0].strftime("%B %d, %Y"), round(day[1], 1)), file=f, end='\r\n')
    print("\n", file=f, end='\r\n')
    f.close()

print("Report was created and stored in file {}\n\n".format(output_file))
