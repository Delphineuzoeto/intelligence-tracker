import pandas as pd
from google_play_scraper import reviews, Sort


def scrape_reviews(app_id, company, category, count=500):
    all_reviews = []
    
    for score in [1, 2, 3]:
        result, _ = reviews(
            app_id,
            lang='en',
            country='ng',
            sort=Sort.NEWEST,
            count=count,
            filter_score_with=score
        )
        all_reviews.extend(result)
    
    df = pd.DataFrame(all_reviews)
    df['company'] = company
    df['category'] = category
    
    return df

apps = [
    {"app_id": "ng.giglogistics.giglgo", "company": "GIG Logistics", "category": "Last-Mile"},
    {"app_id": "com.kwik.customer", "company": "Kwik Delivery", "category": "Last-Mile"},
    {"app_id": "ng.gokada.superapp_client", "company": "Gokada", "category": "Last-Mile"},
    {"app_id": "com.topship.mobile", "company": "Topship", "category": "Traditional Express"},
    {"app_id": "com.sendstack.ctrlapp", "company": "Sendstack", "category": "Traditional Express"},
    {"app_id": "com.courierplus", "company": "CourierPlus", "category": "Traditional Express"},
]

def clean_and_save(df):
    keep_columns = ['reviewId', 'userName', 'content', 'score', 'at', 'company', 'category']
    cleaned_df = df[keep_columns]
    
    try:
        existing_df = pd.read_csv("logistics_reviews_clean.csv")
        combined_df = pd.concat([existing_df, cleaned_df], ignore_index=True)
        combined_df.drop_duplicates(subset='reviewId', inplace=True)
    except FileNotFoundError:
        combined_df = cleaned_df
    
    combined_df.to_csv("logistics_reviews_clean.csv", index=False)
    print(f"Clean CSV updated — total records: {len(combined_df)}")


def main():
    all_data = []

    for app in apps:
        print(f"Scraping{app['company']}...")
        df = scrape_reviews(app['app_id'], app["company"], app['category'])
        all_data.append(df)
        print(f"Done - {len(df)} reviews fetched")

    master_df = pd.concat(all_data, ignore_index=True)
    master_df.to_csv("logistics_reviews_raw.csv", index=False)
    clean_and_save(master_df)
    print(f"\nAll done! Total reviews: {len(master_df)}")

main()
