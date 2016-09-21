import codecs
import os

import pymysql
from datetime import *
from email.utils import parseaddr

from config import connection

excluded_domains = [
    'domainsbyproxy.com',
    'buydomains.com',
    'networksolutionsprivateregistration.com',
    'contactprivacy.com',
    'nameadmininc.com',
    'protecteddomainservices.com',
    'whoisguard.com',
    'domaindiscreet.com',
    'whoisprivacyservices.com.au',
    'namefind.com',
    'secureserver.net',
    'whoisprivacyprotect.com',
    'contact.gandi.net',
    'protopixel.com',
    '1and1.com',
    'privacy-link.com',
    'whoisprivacyprotection.info',
    'ename.com',
    'privacyprotect.org',
    'worldnic.com',
    'comcast.net',
    'proxy.dreamhost.com',
    'domainprivacygroup.com',
    'yinsibaohu.aliyun.com',
    'whoisfoundation.com',
    'whoisprotectservice.com',
    'hugedomains.com',
    'contactprivacy.email',
    'sbcglobal.net',
    'privacyguardian.org',
    'earthlink.net',
    'enamewhois.com',
    'newvcorp.com',
    'gmx.net',
    'godaddy.com',
    'linkz.com',
    'skynet.be',
    'value-domain.com',
    'domains.namespace4you.com',
    'bluehost.com',
    'whois.gkg.net',
    'private-contact.com',
    'domainassetholdings.com',
    'domainnameproxyservice.com',
    'linkuwant.com',
    'namecheap.com',
    'dotcomagency.com',
    'emailaddressprotection.com',
    'whoisprotection.biz',
    'spamfree.bookmyname.com',
    'yummynames.com',
    'enom.value-domain.com',
    'customers.whoisprivacycorp.com',
    'opensrs.namespace4you.com',
    'privacyid.com',
    'whoisprivacy.com',
    'leftfielddomains.com',
    'spamprotection.email',
    'myprivateregistration.com',
    'hostmonster.com',
    'domainnamez.com',
    'privacyadvocate.org',
    'domainregistriesfoundation.com',
    'whoisprotectservice.net',
    'domainlistingagent.com',
    'domainproducts.com',
    'whoisblind.com',
    'yourwhoisprivacy.com',
    'privacy.above.com',
    'identity-protect.org',
    'namesbeyond.com',
    'proxy-privacy.com',
    'freenom.com',
    '1und1.de'
]


def parse_email(s):
    s = s.strip().lower()
    ems = set([])
    arr = s.split('","')
    if len(arr) >= 63:
        em = arr[2]
        if is_email_valid(em):
            ems.add(em)
        em = arr[14]
        if is_email_valid(em):
            ems.add(em)
        em = arr[30]
        if is_email_valid(em):
            ems.add(em)
        em = arr[62]
        if is_email_valid(em):
            ems.add(em)
    if len(ems) == 0:
        return False
    return ems


def is_email_valid(s):
    if '%' in s or '@' not in parseaddr(s)[1]:
        return False
    if s.endswith('.ru') or s.endswith('.jp') or s.endswith('.de') or s.endswith('.fr'):
        return False
    if s.endswith('whoisprivacycorp.com') or s.endswith('whoisproxy.org') or s.endswith('o-w-o.info'):
        return False
    email_arr = s.split('@')
    if len(email_arr) != 2:
        return False
    if email_arr[1] in excluded_domains:
        return False
    return True


def get_table_name(m):
    first = m[:1]
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z']
    if first in alphabet:
        return 'people_' + first
    return 'people_0'


count = 0
success_count = 0
batch = 10000
priority = 6
data_path = '/home/forge/email_list_extract/regular/'

with connection.cursor() as cursor:
    for folder in os.listdir(data_path):
        folder_path = os.path.join(data_path, folder)
        print folder_path
        for fn in os.listdir(folder_path):
            if not fn.endswith('.csv'):
                continue
            file_path = os.path.join(folder_path, fn)
            print file_path
            f = codecs.open(file_path, 'r', encoding='utf-8')
            for line in f:
                count += 1
                if count <= 0:
                    continue
                emails = parse_email(line)
                if emails:
                    for email in emails:
                        table_name = get_table_name(email)
                        try:
                            sql = "INSERT INTO `{0}` VALUE (0, '{1}','', 0, '', '', '' ,0, {2})".format(table_name,
                                                                                                        email,
                                                                                                        priority)
                            cursor.execute(sql)
                            success_count += 1
                        except pymysql.err.IntegrityError:
                            pass
                        except pymysql.err.ProgrammingError:
                            pass
                        except Exception, e:
                            print e
                            pass
                if count % batch == 0:
                    connection.commit()
                    print '{0} commit success , count : {1} , insert : {2}'.format(datetime.now(), count, success_count)
                    connection.begin()
connection.commit()
connection.close()
print '{0} commit success , count : {1}, insert : {2}'.format(datetime.now(), count, success_count)
