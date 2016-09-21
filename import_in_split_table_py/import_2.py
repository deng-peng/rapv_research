import codecs
import os
import json
import re
import pymysql
from datetime import *
from email.utils import parseaddr
from config import connection, cnt_company

people_count = 0
email_count = 0
insert_count = 0
update_count = 0
batch = 1000
priority = 6
data_path = '/home/forge/email_list_extract/regular/com/'


def get_table_name(m):
    first = m[:1]
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z']
    if first in alphabet:
        return 'people_' + first
    return 'people_0'


def get_company_url_identifie(u):
    arr = u.split('/')
    return arr[-1]


def build_sql_from_identifies(ids):
    idf = ids.pop()
    sql = 'select * from company where ' + build_part_sql_for_identifie(idf)
    if len(ids) > 0:
        for idf in ids:
            sql += ' or ' + build_part_sql_for_identifie(idf)
    return sql


def build_part_sql_for_identifie(id):
    if id.isdigit():
        return ' linkedin_id = {} '.format(id)
    else:
        return ' linkedin_url = "{}" '.format(id)


def get_profile_url(url):
    url = url.strip().lower()
    if 'linkedin.com/in/' in url:
        return url
    return False


def is_email_valid(s):
    if '%' in s or '@' not in parseaddr(s)[1]:
        return False
    if s.endswith('.ru') or s.endswith('.jp') or s.endswith('.de') or s.endswith('.fr'):
        return False
    email_arr = s.split('@')
    if len(email_arr) != 2:
        return False
    return True


# Returns the string without non ASCII characters
def clean_name_string(s):
    pattern = re.compile(r'[^a-z0-9.]')
    return pattern.sub('', s)


def update_exist_email(table_name, email, profile_url):
    try:
        with connection.cursor() as cursor:
            print '### update {}, {}'.format(email, profile_url)
            cursor.execute('select * from {0} where email = "{1}"'.format(table_name, email))
            row = cursor.fetchone()
            print row
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


file_path = '/home/forge/linkedin/linkedin/people/2016-01/ds_dump_AU_1.jl'
with connection.cursor() as cur:
    f = codecs.open(file_path, 'r', encoding='utf-8')
    for line in f:
        people_count += 1
        # if people_count > 1500:
        #     break
        try:
            js = json.loads(line)
            if 'experience' not in js:
                continue
            profile_url = get_profile_url(js['url'])
            if not profile_url:
                continue
            first_name = clean_name_string(js['given_name'].strip().lower())
            last_name = clean_name_string(js['family_name'].strip().lower())
            ids = set([])
            for exp in js['experience']:
                if 'organization' not in exp:
                    continue
                for org in exp['organization']:
                    if 'profile_url' in org:
                        identifie = get_company_url_identifie(org['profile_url'])
                        ids.add(identifie)
            if len(ids) > 0:
                sql = build_sql_from_identifies(ids)
                with cnt_company.cursor() as cursor:
                    cursor.execute(sql)
                    comps = cursor.fetchall()
                    insert_emails = []
                    for comp in comps:
                        domain = comp['website'].strip().lower()
                        if domain == '':
                            continue
                        insert_emails.append('{}{}@{}'.format(first_name, last_name, domain))
                        insert_emails.append('{}.{}@{}'.format(first_name, last_name, domain))
                        if comp['size'] == '1-10 employees' or comp['size'] == 'Myself Only':
                            insert_emails.append('{}@{}'.format(first_name, domain))
                    if len(insert_emails) > 0:
                        for email in insert_emails:
                            email_count += 1
                            if not is_email_valid(email):
                                continue
                            table_name = get_table_name(email)
                            try:
                                si = "INSERT INTO `{0}` VALUE (0, '{1}','', 0, 'mockup', '{2}', '' ,0, {3})".format(
                                    table_name, email, profile_url, priority)
                                # print si
                                cur.execute(si)
                                insert_count += 1
                            except pymysql.err.IntegrityError, ei:
                                # print ei
                                update_count += update_exist_email(table_name, email, profile_url)
                            except pymysql.err.ProgrammingError, ep:
                                # print ep
                                pass
                            except Exception, e:
                                print e
                    if people_count % batch == 0:
                        connection.commit()
                        print '{0} commit success , people : {1} , emails : {2} , insert : {3} , update : {4}'.format(
                            datetime.now(),
                            people_count,
                            email_count,
                            insert_count,
                            update_count)
                        connection.begin()
        except Exception:
            pass
        print '------------------------------'
connection.commit()
connection.close()
print 'finished , people : {0} , emails : {1} , insert : {2} , update : {3}'.format(people_count, email_count,
                                                                                    insert_count, update_count)
