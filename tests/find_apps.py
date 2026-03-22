from google_play_scraper import search, reviews, Sort

# companies = [
#     "Haul247 Nigeria",
#     "Sendstack Nigeria",
#     "Kwik messenger Nigeria",
#     "CourierPlus Nigeria",
#     "Gokada Nigeria",
# ]

# for company in companies:
#     print(f"\nSearching: {company}")
#     results = search(company, lang='en', country='ng', n_hits=3)
#     for app in results:
#         print(f"  {app['title']} --- {app['appId']}")

result, _ = reviews(
    'com.courierplus',
    lang='en',
    country='ng',
    sort=Sort.NEWEST,
    count=10
)

print(f"Total fetched: {len(result)}")
for r in result[:3]:
    print(r['score'], '---', r['content'])