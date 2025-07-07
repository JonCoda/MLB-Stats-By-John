import datetime

class NewsArticle:
    """
    Represents a single news article with a title, source, date, and summary.
    """
    def __init__(self, title: str, source: str, publication_date: datetime.date, summary: str, url: str):
        """
        Initializes a NewsArticle object.

        Args:
            title (str): The headline of the article.
            source (str): The publisher of the article (e.g., MLB.com, ESPN).
            publication_date (datetime.date): The date the article was published.
            summary (str): A brief summary of the article's content.
            url (str): A URL to the full article.
        """
        self.title = title
        self.source = source
        self.publication_date = publication_date
        self.summary = summary
        self.url = url

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the news article.
        """
        date_str = self.publication_date.strftime('%B %d, %Y')
        return (
            f"'{self.title}'\n"
            f"  Source: {self.source}\n"
            f"  Date: {date_str}\n"
            f"  Summary: {self.summary}\n"
            f"  Read more: {self.url}\n"
        )

def generate_mock_mlb_news() -> list[NewsArticle]:
    """
    Generates a list of mock MLB news articles for demonstration.

    Returns:
        list[NewsArticle]: A list of NewsArticle objects, sorted by most recent.
    """
    articles = []
    today = datetime.date.today()

    articles.append(NewsArticle(
        title="Yankees Walk-Off Against Red Sox in 10th Inning Thriller",
        source="ESPN",
        publication_date=today,
        summary="Aaron Judge's sacrifice fly in the bottom of the 10th inning gave the New York Yankees a dramatic 3-2 win over the Boston Red Sox.",
        url="https://www.espn.com/mlb/story/_/id/0000000/yankees-walk-off-red-sox"
    ))

    articles.append(NewsArticle(
        title="Shohei Ohtani Hits 2 Homers, Pitches 7 Shutout Innings in Angels' Win",
        source="MLB.com",
        publication_date=today - datetime.timedelta(days=1),
        summary="Shohei Ohtani continued his MVP-caliber season with a dominant two-way performance, leading the Los Angeles Angels to a 5-0 victory.",
        url="https://www.mlb.com/news/shohei-ohtani-dominant-vs-mariners"
    ))

    articles.append(NewsArticle(
        title="Padres Acquire Star Pitcher at Trade Deadline",
        source="The Athletic",
        publication_date=today - datetime.timedelta(days=2),
        summary="The San Diego Padres have made a major splash, acquiring an ace pitcher from an AL Central team in exchange for a package of top prospects.",
        url="https://theathletic.com/mlb/news/padres-trade-ace-pitcher/"
    ))

    # Sort articles by publication date, newest first
    return sorted(articles, key=lambda article: article.publication_date, reverse=True)

def display_news_feed(articles: list[NewsArticle]):
    """
    Prints the formatted news feed to the console.
    """
    print("⚾" * 5 + "  MLB News Feed  " + "⚾" * 5)
    if not articles:
        print("\nNo news available at the moment.")
        return

    for article in articles:
        print("-" * 40)
        print(article)

if __name__ == "__main__":
    mlb_articles = generate_mock_mlb_news()
    display_news_feed(mlb_articles)
