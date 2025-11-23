"""
Create sample Reddit posts data for testing
This generates realistic tariff-related posts based on the project description
"""

import csv
import os
from datetime import datetime, timedelta
import random


def generate_sample_posts(num_posts: int = 100) -> list:
    """Generate sample Reddit posts about tariffs"""

    # Sample post templates
    templates = [
        "Trump announces {rate}% tariff on {country} imports worth ${amount} billion",
        "Biden and {leader} discuss trade deal in {city}",
        "BBC reports that {product} tariffs impact {sector} sector",
        "{country} exports {product} to USA",
        "The White House opposes the {policy} trade agreement",
        "{leader} increases tariffs on {product} from {country}",
        "CNN reports: {country} threatens retaliation against American tariffs",
        "{organization} warns that tariff policy will harm {sector}",
        "Steel and aluminum tariffs announced for imports from {country}",
        "Manufacturing sector concerned about {policy} impact on {product}",
        "{leader} negotiates with {country} over trade disputes",
        "Trade war escalates as {country} imposes {rate}% tariff on US goods",
        "{organization} supports MAGA tariff policy against {country}",
        "Farmers worry about {product} exports to {country}",
        "WTO rules against {country} tariff measures",
        "{leader} at {event}: America First trade policy will create jobs",
        "Al Jazeera: {country} and USA reach temporary trade agreement",
        "Automotive industry faces uncertainty over {rate}% car tariffs",
        "{country} accuses USA of unfair trade practices",
        "Wall Street Journal: Tariffs on {product} raise consumer prices",
        "USMCA replaces NAFTA with stricter manufacturing requirements",
        "{organization} analysis shows tariffs cost ${amount} billion annually",
        "{leader} threatens {country} with additional {rate}% tariffs",
        "Small businesses struggle with increased costs from {product} tariffs",
        "China retaliates with tariffs on American {product}",
    ]

    # Sample entities
    leaders = ["Trump", "Biden", "Modi", "Xi Jinping", "Trudeau", "Macron", "Johnson"]
    countries = ["China", "India", "Mexico", "Canada", "EU", "Japan", "Germany", "UK"]
    products = ["steel", "aluminum", "cars", "agricultural products", "soybeans", "solar panels", "electronics"]
    sectors = ["manufacturing", "agriculture", "automotive", "technology", "energy"]
    organizations = ["WTO", "IMF", "World Bank", "Bloomberg", "Reuters", "Forbes"]
    policies = ["NAFTA", "USMCA", "Section 232", "Section 301", "MAGA"]
    cities = ["Washington", "Beijing", "New Delhi", "Brussels", "Tokyo", "Ottawa"]
    events = ["G20 Summit", "Trade Conference", "Press Conference", "White House Meeting"]

    posts = []
    base_date = datetime(2024, 1, 1)

    usernames = [
        "trade_policy_wonk", "economic_observer", "tariff_analyst", "global_trader",
        "policy_watcher", "economic_news", "trade_expert", "political_junkie",
        "retroanduwu24", "Opioid-Connoisseur", "Professional-Kale216",
        "market_analyst", "trade_monitor", "policy_researcher", "econ_student"
    ]

    for i in range(num_posts):
        # Select random template and fill in
        template = random.choice(templates)

        text = template.format(
            rate=random.choice([10, 15, 20, 25, 30, 35]),
            country=random.choice(countries),
            amount=random.choice([50, 100, 150, 200, 250, 300]),
            leader=random.choice(leaders),
            product=random.choice(products),
            sector=random.choice(sectors),
            organization=random.choice(organizations),
            policy=random.choice(policies),
            city=random.choice(cities),
            event=random.choice(events)
        )

        # Random date
        days_offset = random.randint(0, 300)
        post_date = base_date + timedelta(days=days_offset)

        # Create post
        post = {
            'datetime_utc': post_date.strftime('%Y-%m-%d %H:%M:%S'),
            'username': random.choice(usernames),
            'post_link': f'https://reddit.com/r/Tariffs/comments/post{i}',
            'text_content': text,
            'relevance_score': round(random.uniform(0.6, 1.0), 2),
            'upvotes': random.randint(10, 500),
            'comments_count': random.randint(5, 100)
        }

        posts.append(post)

    return posts


def save_to_csv(posts: list, output_path: str):
    """Save posts to CSV file"""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    fieldnames = ['datetime_utc', 'username', 'post_link', 'text_content',
                  'relevance_score', 'upvotes', 'comments_count']

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(posts)

    print(f"✓ Created {len(posts)} sample posts at {output_path}")


def main():
    """Generate sample data"""

    output_path = "../data/reddit_posts.csv"

    # Check if file exists
    if os.path.exists(output_path):
        response = input(f"{output_path} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return

    # Generate posts
    print("Generating sample Reddit posts...")
    posts = generate_sample_posts(num_posts=200)

    # Save to CSV
    save_to_csv(posts, output_path)

    print("\nSample data created successfully!")
    print("You can now run the pipeline with:")
    print("  python main_pipeline.py")


if __name__ == "__main__":
    main()
