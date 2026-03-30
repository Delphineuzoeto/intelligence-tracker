import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


#Create charts folder to save all images
os.makedirs("charts", exist_ok=True)

def chart_avg_rating():
    df = pd.read_csv("results/avg_rating.csv")

    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x="company", y="avg_rating", hue="company", palette="Reds_r", legend=False)
    plt.title("Average Rating by company (1-3 stars  = complaints only)")
    plt.xlabel("Company")
    plt.ylabel("Average Rating")
    plt.ylim(1, 3)
    plt.tight_layout()
    plt.savefig("charts/avg_rating.png")
    plt.close()
    print("Charts saved: avg_rating.png")


chart_avg_rating()

def chart_complaints_over_time():
    df = pd.read_csv("results/complaints_over_time.csv")
    
    plt.figure(figsize=(14, 6))
    for company in df["company"].unique():
        company_df = df[df["company"] == company]
        plt.plot(company_df["month"], company_df["total_complaints"], marker="o", label=company)
    
    plt.title("Complaints Over Time by Company")
    plt.xlabel("Month")
    plt.ylabel("Total Complaints")
    plt.xticks(rotation=90)
    plt.legend()
    plt.tight_layout()
    plt.savefig("charts/complaints_over_time.png")
    plt.close()
    print("Chart saved: complaints_over_time.png")

chart_complaints_over_time()

def chart_top_keywords():
    df = pd.read_csv("results/keyword_analysis.csv")
    
    # Sum mentions across all years per company and keyword
    df_grouped = df.groupby(["company", "keyword"])["mentions"].sum().reset_index()
    
    # Get top 10 keywords per company
    top_keywords = df_grouped.sort_values("mentions", ascending=False).groupby("company").head(10)
    companies = top_keywords["company"].unique()
    
    fig, axes = plt.subplots(1, len(companies), figsize=(18, 6), sharey=False)
    
    for i, company in enumerate(companies):
        data = top_keywords[top_keywords["company"] == company]
        axes[i].barh(data["keyword"], data["mentions"], color="steelblue")
        axes[i].set_title(company, fontsize=11, fontweight="bold")
        axes[i].set_xlabel("Mentions")
        axes[i].invert_yaxis()
    
    plt.suptitle("Top 10 Complaint Keywords per Company", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("charts/top_keywords.png")
    plt.close()
    print("Chart saved: top_keywords.png")

chart_top_keywords()