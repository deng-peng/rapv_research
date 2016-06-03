from retrying import retry


def get_search_bar():
    print 'get_search_bar'
    try:
        res = __find_search_bar()
    except Exception:
        res = ''
    return res


@retry(wait_fixed=1500, stop_max_attempt_number=3)
def __find_search_bar():
    print '__find_search_bar'
    raise Exception('retry')
    return 1


if __name__ == '__main__':
    print get_search_bar()
