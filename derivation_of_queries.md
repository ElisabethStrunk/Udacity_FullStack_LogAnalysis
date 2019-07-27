# Derivation of queries

## Preparation for investigating popularity of articles and authors:
### create list with slugs, status and time from log table:
SELECT REPLACE(log.path, '/article/', ''), log.status, log.time
FROM log;

### from this list take only the entries where the slug corresponds to an article:
SELECT REPLACE(log.path, '/article/', ''), log.status, log.time
FROM log, articles
WHERE REPLACE(log.path, '/article/', '') = articles.slug;

### create a view from this:
CREATE VIEW article_log AS
SELECT log.id, REPLACE(log.path, '/article/', '') AS url, log.status, log.time
FROM log, articles
WHERE REPLACE(log.path, '/article/', '') = articles.slug;


## Investigate popularity of articles:
#### find top 3 (most viewed) articles - by url
SELECT url, count(*) AS num
FROM article_log
GROUP BY url
ORDER BY num DESC
LIMIT 3;

### find top 3 (most viewed) articles - by title
SELECT articles.title, count(*) AS num_views
FROM article_log
RIGHT JOIN articles
ON articles.slug = article_log.url
GROUP BY articles.title
ORDER BY num_views DESC
LIMIT 3;


## Investigate popularity of authors:
### find article views per author:
SELECT authors.name, count(*) AS num_views
FROM authors
LEFT JOIN articles
ON (authors.id = articles.author)
LEFT JOIN article_log
ON (articles.slug = article_log.url)
GROUP BY authors.name
ORDER BY num_views DESC;


## Investigate error-riddled days:
### Finding all errors and the date they occurred:
SELECT status, date(time)
FROM log
WHERE (status LIKE '4%') OR (status LIKE '5%');

### find out how many requests were made on each day:
SELECT date(time) AS day, count(*) AS num_total #
FROM log
GROUP BY day;

### find out how many errors occurred on each day:
SELECT day, count(*) AS num_errors
FROM (
    SELECT status, date(time) AS day
    FROM log
    WHERE (status LIKE '4%') OR (status LIKE '5%')
) AS error_log
GROUP BY day
ORDER BY day;

### shorter version of the above:
SELECT date(time) AS day, count(*) AS num_errors
FROM log
WHERE (status LIKE '4%') OR (status LIKE '5%')
GROUP BY day
ORDER BY day;

### find out percentage of requests that lead to errors:
SELECT request_query.day, (100.0*num_errors/(1.0*num_total)) AS error_percentage
FROM (
    SELECT date(time) AS day, count(*) AS num_total
    FROM log
    GROUP BY day
) AS request_query
LEFT JOIN (
    SELECT date(time) AS day, count(*) AS num_errors
    FROM log
    WHERE (status LIKE '4%') OR (status LIKE '5%')
    GROUP BY day
) AS error_query
ON request_query.day = error_query.day
ORDER BY request_query.day;

### find days with an error percentage > 1%:
SELECT day, error_percentage
FROM (
    SELECT request_query.day, (100.0*num_errors/(1.0*num_total)) AS error_percentage
    FROM (
        SELECT date(time) AS day, count(*) AS num_total
        FROM log
        GROUP BY day
    ) AS request_query
    LEFT JOIN (
        SELECT date(time) AS day, count(*) AS num_errors
        FROM log
        WHERE (status LIKE '4%') OR (status LIKE '5%')
        GROUP BY day
    ) AS error_query
    ON request_query.day = error_query.day
) AS percentage_query
WHERE error_percentage > 1.0
ORDER BY day;