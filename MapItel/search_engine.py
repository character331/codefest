import time
import pandas as pd
import os
from news import NewsAPI
from scraper import get_web_content
from chat import chat_parse
import json
from geo import get_geo

news = NewsAPI("3a10124094384d0e8da1e133c3583a14")
required_fields = {'Name', 'Date', 'Location', 'Summary'}


def search(location, keyword):
    # check cache
    cache = try_find_cached(location, keyword)
    if cache:
        return cache

    # start new search
    try:
        target_geo = get_geo(location)
        if not target_geo:
            # print(f"invalid location: {location}, {target_geo}")
            return 400
    except:
        # print(f"invalid location: {location}")
        return 400

    print("location", location, target_geo)
    urls = news.search_articles(location, keyword)

    pages = []
    print(f"get {len(urls)} links from news endpoint.", urls, sep="\n")
    print("start scrap...")
    for i, url in enumerate(urls[:5]):
        try:
            contents = get_web_content(url)
            page = ({"contents": contents, "url": url})
            pages.append(page)
            print(f"Done scrap pages {i + 1}/{len(urls)}", url)
        except:
            pass
            # print(f"scrap fail in {url}")

        # break

    all_events = []
    print("\nstart parse contents...")
    for j, page in enumerate(pages):
        for content in page["contents"]:
            res = chat_parse(location, keyword, content)
            try:
                events = json.loads(res)
                for event in events:
                    print(event)
                    try:
                        assert len(set(event.keys()).difference(required_fields)) == 0
                        event["url"] = page["url"]

                        event["Geo"] = get_geo(event["Location"])  # latitude and longitudedinate

                        if not event["Geo"]:
                            # print(f'invalid location: {location}, {event["Geo"]}')
                            continue
                        else:
                            all_events.append(event)
                            print("\n", event["name"], event["Geo"])
                    except:
                        pass
                        # print("event", event)

            except:
                pass
                # print("res", res)
            # break
        print(f"Done analysis pages {j + 1}/{len(pages)}. total event: {len(all_events)}")

    # to do: cache
    file_name = f"./cache/{location}-{keyword}-{time.time()}"
    json.dump({"target": target_geo, "locations": all_events}, open(file_name, "w"))
    # open("static/result.js", "w").write(f"var locations = {json.dumps(all_events)}")

    # register to cache
    if os.path.isfile("./cache/index.csv"):
        queries_cached = pd.read_csv("./cache/index.csv")
    else:
        queries_cached = pd.DataFrame({"location": [], "keyword": [], "cache": []})
    new_row = pd.DataFrame({"location": [location], "keyword": [keyword], "cache": [file_name]})
    queries_cached = pd.concat([queries_cached, new_row], ignore_index=True)
    queries_cached.to_csv("./cache/index.csv", index=False)

    return file_name


def try_find_cached(location, keyword):
    if not os.path.isfile("./cache/index.csv"):
        return False
    else:
        queries_cached = pd.read_csv("./cache/index.csv")
        same_queried = queries_cached[(queries_cached.keyword == keyword) & (queries_cached.location == location)]

        if len(same_queried) > 0:
            file_name = queries_cached[(queries_cached.keyword == keyword) &
                                       (queries_cached.location == location)].cache.iloc[-1]
            # print("find cache!", location, keyword, file_name)
            return file_name

        else:
            # print("didn't find cache!")
            return False

# location = "new york"
# keyword = "food"
# print(search(location, keyword))
