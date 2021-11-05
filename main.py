import tweepy

import time


def num(n):
    if n == 0:
        # 9,000,000
        result = "0000000"
    elif 0 < n < 10:
        # 9,000,00*
        result = "000000" + str(n)
    elif 10 <= n < 100:
        # 9,000,0**
        result = "00000" + str(n)
    elif 100 <= n < 1000:
        # 9,000,***
        result = "0000" + str(n)
    elif 1000 <= n < 10000:
        # 9,00*,***
        result = "000" + str(n)
    elif 10000 <= n < 100000:
        # 9,0**,***
        result = "00" + str(n)
    elif 100000 <= n < 1000000:
        # 9,***,***
        result = "0" + str(n)
    else:
        result = str(n)
    return result


def data(tapi, screen_name):
    followers = []
    followings = []
    for page in tweepy.Cursor(tapi.get_follower_ids, screen_name=screen_name).pages():
        for c in page:
            followers.append(c)
        time.sleep(1)
    print(f"Stream {len(followers):,} followers complate!")

    for page in tweepy.Cursor(tapi.get_friend_ids, screen_name=screen_name).pages():
        for c in page:
            followings.append(c)
        time.sleep(1)
    print(f"Stream {len(followings):,} followings complate!")

    # People who did not follow User
    pwdnfu = [value for value in followers if value not in followings]
    # People that User did not follow
    ptudnf = [value for value in followings if value not in followers]

    print(f"People that @{screen_name} did not follow: {len(pwdnfu):,}")
    print(f"People who did not follow @{screen_name}: {len(ptudnf):,}")

    result = {
        'follower': followers,
        'following': followings,
        'pwdnfu': pwdnfu,
        'ptudnf': ptudnf
    }
    return result


def write(tapi, ids):
    counter = 1
    for p in ids:
        try:
            info = tapi.get_user(user_id=p)
            link = "https://twitter.com/" + info.screen_name
            print(f"No: {num(counter)}, Tweets: {num(info.statuses_count)}, Link: {link}")
        except:
            print(f"No: {num(counter)}, Id: {p} Not found!")
        counter += 1
        time.sleep(1)
    input("Press any key to exit.")


if __name__ == '__main__':
    cf = {
        'key': '*****',
        'kse': '*****',
        'tok': '*****',
        'tse': '*****'
    }
    auth = tweepy.OAuthHandler(cf['key'], cf['kse'])
    auth.set_access_token(cf['tok'], cf['tse'])
    api = tweepy.API(auth, wait_on_rate_limit=True)

    username = input("Please enter Twitter @username: ")
    user_ids = data(api, username)
    print("Select your function:")
    print(f"[1] People who be followed @{username}.")
    print(f"[2] People that @{username} be followed.")
    print(f"[3] People who did not followed @{username}.")
    print(f"[4] People that @{username} did not followed.")
    print(f"[5] Exit from app.")
    run = int(input("Insert your function code? (1|2|3|4|5) : "))

    if run == 1:
        write(api, user_ids['follower'])
    elif run == 2:
        write(api, user_ids['following'])
    elif run == 3:
        write(api, user_ids['ptudnf'])
    elif run == 4:
        write(api, user_ids['pwdnfu'])
    elif run == 5:
        input("Press any key to exit.")
