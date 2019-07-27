#!/usr/bin/python3

"""
TODO: Write short description
"""

import psycopg2

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


def find_top_three_articles():
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
