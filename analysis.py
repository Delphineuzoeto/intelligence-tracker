import pandas as pd
import sqlite3
import os

def load_data():
    """
    Loads the clean CSV into a SQLite database.
    Creates a 'reviews' table, replacing it on each run with fresh data.
    Returns the database connection for use by other functions.
    """
    df = pd.read_csv("logistics_reviews_clean.csv")
    conn = sqlite3.connect("logistics.db")
    df.to_sql("reviews", conn, if_exists="replace", index=False)
    print("Database ready")
    print(f"Total records loaded: {len(df)}")
    return conn

def keyword_analysis(conn):
    """
    Categorizes each review by matching keywords in the complaint text.
    Groups results by company, year, and keyword to show what people
    complain about most — and how that changes over time.
    Saves output to results/keyword_analysis.csv
    """
    query = """
    SELECT company,
        STRFTIME('%Y', at) as year,
        CASE
            WHEN LOWER(content) LIKE '%waybill%' THEN 'waybill'
            WHEN LOWER(content) LIKE '%wallet%' THEN 'wallet'
            WHEN LOWER(content) LIKE '%timeout%' THEN 'timeout'
            WHEN LOWER(content) LIKE '%pickup%' OR LOWER(content) LIKE '%pick up%' THEN 'pickup'
            WHEN LOWER(content) LIKE '%package%' THEN 'package'
            WHEN LOWER(content) LIKE '%insurance%' THEN 'insurance'
            WHEN LOWER(content) LIKE '%no response%' THEN 'no response'
            WHEN LOWER(content) LIKE '%address%' THEN 'address'
            WHEN LOWER(content) LIKE '%delay%' OR LOWER(content) LIKE '%wait%' THEN 'delay'
            WHEN LOWER(content) LIKE '%scam%' THEN 'scam'
            WHEN LOWER(content) LIKE '%refund%' THEN 'refund'
            WHEN LOWER(content) LIKE '%driver%' THEN 'driver'
            WHEN LOWER(content) LIKE '%stolen%' THEN 'stolen'
            WHEN LOWER(content) LIKE '%support%' THEN 'support'
            WHEN LOWER(content) LIKE '%lost%' THEN 'lost'
            WHEN LOWER(content) LIKE '%wrong%' THEN 'wrong'
            WHEN LOWER(content) LIKE '%cancel%' THEN 'cancel'
            WHEN LOWER(content) LIKE '%rude%' THEN 'rude'
            WHEN LOWER(content) LIKE '%call%' THEN 'call'
            WHEN LOWER(content) LIKE '%rider%' THEN 'rider'
            WHEN LOWER(content) LIKE '%otp%' THEN 'otp'
            WHEN LOWER(content) LIKE '%customer service%' OR LOWER(content) LIKE '%customer care%' THEN 'customer care'
            WHEN LOWER(content) LIKE '%connect%' THEN 'connection'
            WHEN LOWER(content) LIKE '%verif%' THEN 'verification'
            WHEN LOWER(content) LIKE '%slow%' THEN 'slow'
            WHEN LOWER(content) LIKE '%debit%' OR LOWER(content) LIKE '%charged%' THEN 'payment issue'
            WHEN LOWER(content) LIKE '%crash%' OR LOWER(content) LIKE '%hang%' THEN 'crash'
            WHEN LOWER(content) LIKE '%login%' OR LOWER(content) LIKE '%logged out%' THEN 'login'
            WHEN LOWER(content) LIKE '%track%' THEN 'tracking'
            WHEN LOWER(content) LIKE '%app%' THEN 'app'
        END as keyword,
        COUNT(*) as mentions
    FROM reviews
    WHERE keyword IS NOT NULL
    GROUP BY company, year, keyword
    ORDER BY company, year, mentions DESC
    """
    df = pd.read_sql_query(query, conn)
    df.to_csv("results/keyword_analysis.csv", index=False)
    print(f"Keyword analysis done — {len(df)} rows")
    return df

def complaints_over_time(conn):
    """
    Counts total complaints per company per month.
    Used to track whether problems are getting better or worse over time.
    Saves output to results/complaints_over_time.csv
    """
    query = """
    SELECT company,
        STRFTIME('%Y-%m', at) as month,
        COUNT(*) as total_complaints
    FROM reviews
    GROUP BY company, month
    ORDER BY company, month ASC
    """
    df = pd.read_sql_query(query, conn)
    df.to_csv("results/complaints_over_time.csv", index=False)
    print(f"Complaints over time done — {len(df)} rows")
    return df

def avg_rating(conn):
    """
    Calculates the average star rating per company.
    Lower average = more user dissatisfaction.
    Saves output to results/avg_rating.csv
    """
    query = """
    SELECT company, category,
        COUNT(*) as total_reviews,
        ROUND(AVG(score), 2) as avg_rating
    FROM reviews
    GROUP BY company, category
    ORDER BY avg_rating ASC
    """
    df = pd.read_sql_query(query, conn)
    df.to_csv("results/avg_rating.csv", index=False)
    print(f"Average rating done — {len(df)} rows")
    return df

# Create results folder if it doesn't exist yet
# exist_ok=True means it won't throw an error if the folder is already there
os.makedirs("results", exist_ok=True)

# Run all analysis functions in order
conn = load_data()
keyword_analysis(conn)
complaints_over_time(conn)
avg_rating(conn)