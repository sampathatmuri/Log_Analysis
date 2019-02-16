#!/usr/bin/env python3
import psycopg2


def main():
    database = psycopg2.connect("dbname=news")
    # Trying to connect to our database
    cursor = database.cursor()
    #  Query to find the most popular three articles of all time
    query = """
            select articles.title,count(title) from log,articles where
            log.path = '/article/' || articles.slug group by articles.title
            order by count(title) DESC limit 3;
        """
    cursor.execute(query)
    #  executing our query to find the solution
    r = cursor.fetchall()
    print('The Three most popular articles of all time')
    print('=======================================')
    for r in r:
        print('"{title}" - {count} views'.format(title=r[0], count=r[1]))
        '''  format identifiers help if you want to provide non-default
             formatting for your values.'''
    #  Query to find the most populor author of all time
    query = """
            select authors.name,count(name) from log,articles,authors where
            log.path = '/article/' || articles.slug
            AND articles.author = authors.id group by authors.name
            order by count(name) DESC;
        """
    cursor.execute(query)
    r = cursor.fetchall()
    print("\n")
    print('The Most popular authors of all time')
    print('================================')
    for r in r:
        print('{author} - {count} views'.format(author=r[0], count=r[1]))

    #  To print a day which has more than 1% of requests are errors
    '''  'WITH' clause lets you store the result of a query in a
    temporary table using an alias'''
    #  per_day_requests - it is store how many requests are doing per day
    #  per_day_error - It is store how many requests are errors per day
    #  count_rate_error - It is to store the rate of error for a particular day
    query = """
            with per_day_requests AS(
                select time::date AS day, count(*)
                from log
                group by time::date
                order by time::date
              ), per_day_error AS(
                select time::date AS day, count(*)
                from log
                where status != '200 OK'
                group by time::date
                order by time::date
              ), count_rate_error AS(
                select per_day_requests.day,
                  per_day_error.count*1.0/per_day_requests.count*100.0
                  AS rate_error_day
                from per_day_requests, per_day_error
                where per_day_requests.day = per_day_error.day
              )
            select * from count_rate_error where rate_error_day > 1;
        """
    cursor.execute(query)
    results = cursor.fetchall()
    print("\n")
    print('Days with more than 1% of requests leads to errors')
    print('================================')
    for result in results:
        print('{date:%B %d, %Y} - {count_rate_error:.1f}% errors'
              .format(date=result[0], count_rate_error=result[1]))
    '''  format identifiers help if you want to provide non-default formatting
    for your values.'''
    '''  for displaying the date '2016-07-17' in the form of july 17,2016
    we need to use the %B-month %D-date %Y-year'''
    database.close()
#  once a database is opened we need to close that database after our usage.


if __name__ == "__main__":
    main()
