"""
==============================================================

ジーニーのTrackTestの問題。APIを使ってデータを利用する
みたいなやつだったから記録。もちろん実行はできない。

===============================================================
"""

import sys
import requests

def main(argv):

    n = argv[0]
    m = argv[1]
    l = argv[2]
    # print(n,m,l)
    url_userapi = "http://localhost:3000/api/sns/user"
    url_postapi = "http://localhost:3000/api/sns/posts"#?since=<since>&until=<until>
    id_params = {"user_id": n}
    time_params = {"since" : m, "until" : l}

    # Get User
    user_response = requests.get(url_userapi, params=id_params)
    if user_response.status_code == 404:    # for Not found
        print("No user.")
        return
    else:   # get mydata
        mydata = user_response.json()["result"]


    # Get Posts
    posts_response = requests.get(url_postapi, params = time_params)
    if posts_response.status_code == 404:    # for Not found
        print("No posts.")
        return
    else:   # get postsdata
        postsdata = posts_response.json()["result"]


    # Find my posts and Add liked_user
    ctlike_myposts = {}
    found = False  #mypost found or not

    for post in postsdata:
        # print(post)
        if post["user_id"] == n: #find my post
            found = True
            for liked_user in post["liked_by"]: #string like_user
                ctlike_myposts[liked_user] = ctlike_myposts.get(liked_user, 0) + 1  #if can't get liked_user => start 0

    if not ctlike_myposts:
        if found == True: #found my post but not liked
            print("No liked.")
        else:
            print("No posts.")
        return

    # Sort liked User
    items = list(ctlike_myposts.items())
    items_sorted = sorted(items, key=lambda item: (-item[1], int(item[0])))
    likers = items_sorted[:3]

    # Print result
    for liker_id, ct in likers :
        id_params = {"user_id": liker_id}
        liker_response = requests.get(url_userapi, params=id_params)
        likerdata = liker_response.json()["result"]
        print(f"name: {likerdata['name']}, number_of_follows: {len(likerdata['follows'])}")



if __name__ == '__main__':
    main(sys.argv[1:])