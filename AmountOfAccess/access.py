import requests
from requests.exceptions import RequestException
from multiprocessing.pool import Pool
from settings import *
import useragents
from random import choice
import sys

# 实时访问成功次数
access_number_successful = 0


def get_proxy():
    try:
        response = requests.get(ACCESS_SERVER, headers=useragents.get_user_agent())
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        print(e.response)
        return None


def is_over_account():
    global access_number_successful
    if access_number_successful > ACCESS_Acount:
        return False
    return True


def access():
    if is_over_account():
        try:
            random_proxy = str(get_proxy())
            print(random_proxy, 'daili')
            proxies = {
                "http": "http:" + random_proxy,
                "https": "https:" + random_proxy
            }
            response = requests.get(choice(ACCESS_URL), headers=useragents.get_user_agent(), proxies=proxies, timeout=30)
            if response.status_code == 200:
                print('access sucessful')
                global access_number_successful
                access_number_successful += 1
                return 'OK'
            return None
        except RequestException as e:
            print(e.response)
            access()
            return None
    else:
        print("访问次数已达到上限")
        sys.exit()


if __name__ == '__main__':
    pool = Pool(processes=100)
    for i in range(0, ACCESS_Acount+1):
        pool.apply_async(access())
    pool.close()
    pool.join()

