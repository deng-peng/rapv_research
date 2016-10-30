import json
import re
import pymysql
from datetime import *
from config import connection, cnt_people

people_count = 0
email_count = 0
insert_count = 0
update_count = 0
batch = 5
priority = 6


def get_table_name(m):
    first = m[:1]
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z']
    if first in alphabet:
        return 'people_' + first
    return 'people_0'


def get_profile_url(url):
    url = url.strip().lower()
    if 'linkedin.com/in/' in url:
        return url
    return False


# Returns the string without non ASCII characters
def clean_name_string(s):
    pattern = re.compile(r'[^a-z0-9.]')
    return pattern.sub('', s)


def update_exist_email(table_name, email, profile_url):
    try:
        with cnt_people.cursor() as cursor:
            # print '### update {}, {}'.format(email, profile_url)
            cursor.execute('select * from {0} where email = "{1}"'.format(table_name, email))
            row = cursor.fetchone()
            # print row
            update_sql = False
            if row['status'] == 201 or row['status'] == 403:
                update_sql = 'update {0} set status = 200 , message = "mockup" ,profile_url = "{1}" ' \
                             'where email = "{2}" and profile_url = "" '
            elif row['status'] == 404 and row['level'] == 10:
                update_sql = 'update {0} set status = 0 , message = "mockup" ,profile_url = "{1}" ' \
                             'where email = "{2}" and profile_url = "" '
            if update_sql:
                return cursor.execute(update_sql.format(table_name, profile_url, email))
            else:
                return 0
    except Exception, e:
        print e
        return 0


def get_vanity(url):
    arr = url.split('/')
    return arr[4]


def get_mockup_emails(full_name, domain_name, company_size):
    name_arr = full_name.lower().split(' ')
    first_name = name_arr[0]
    last_name = name_arr[-1]
    domain = domain_name.lower()
    mock_emails = [
        '{}{}@{}'.format(first_name, last_name, domain),
        '{}.{}@{}'.format(first_name, last_name, domain)
    ]
    if company_size == '1-10 employees' or company_size == 'Myself Only':
        mock_emails.append('{}@{}'.format(first_name, domain))
    return mock_emails


batch_start_id = 0
with connection.cursor() as cur:
    while True:
        sql = "select id, email, person_name, linkedin_profile_url,company_website,size from aus_recruiters " \
              "where email is null and id > {} order by id limit {}".format(batch_start_id, batch)
        print sql
        cur.execute(sql)
        people = cur.fetchall()
        if len(people) == 0:
            break
        for p in people:
            print p
            people_count += 1
            batch_start_id = p['id']
            profile_url = p['linkedin_profile_url']
            li_vanity = get_vanity(profile_url)
            print li_vanity
            if not li_vanity:
                print profile_url
                continue
            with cnt_people.cursor() as cursor:
                cursor.execute('select * from people where li_vanity = %s', li_vanity)
                found = cursor.fetchone()
                print found
                if found:
                    cur.execute('update aus_recruiters set email = %s where id = %s', (found['email'], p['id']))
                else:
                    insert_emails = get_mockup_emails(p['person_name'], p['company_website'], p['size'])
                    print insert_emails
                    if len(insert_emails) > 0:
                        for email in insert_emails:
                            email_count += 1
                            table_name = get_table_name(email)
                            try:
                                si = "INSERT INTO `{0}` VALUE (0, '{1}','', 0, 'mockup', '{2}', '', '', '', 0, {3})".format(
                                    table_name, email, profile_url, priority)
                                print si
                                cursor.execute(si)
                                insert_count += 1
                            except pymysql.err.IntegrityError, ei:
                                print ei
                                update_count += update_exist_email(table_name, email, profile_url)
                            except pymysql.err.ProgrammingError, ep:
                                # print ep
                                pass
                            except Exception, e:
                                print e

        cnt_people.commit()
        print '{0} commit success , people : {1} , emails : {2} , insert : {3} , update : {4}'.format(
            datetime.now(),
            people_count,
            email_count,
            insert_count,
            update_count)
        cnt_people.begin()
cnt_people.commit()
connection.close()
print 'finished , people : {0} , emails : {1} , insert : {2} , update : {3}'.format(people_count, email_count,
                                                                                    insert_count, update_count)
