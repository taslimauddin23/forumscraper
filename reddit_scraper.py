import streamlit as st
import asyncpraw
import asyncio
import nest_asyncio
from datetime import datetime
import pandas as pd

# Apply nest_asyncio to avoid event loop issues
nest_asyncio.apply()

# Async function to connect to Reddit
async def connect_to_reddit():
    reddit = asyncpraw.Reddit(
       client_id="drgaw6g0UKUt6HHPBtCHXA",          # Replace with your actual client ID
        client_secret="Y7IgHIwAj_1FSvF8g8OcfprOKaWQyw",  # Replace with your actual client secret
        user_agent="RedditScraper/1.0 by /u/Taslima_FreelanceSEO",   # Example: "my_bot by /u/yourusername"
    )
    return reddit

# Async function to search Reddit for specific topics
async def search_reddit(reddit, query, subreddit="all", limit=10):
    subreddit_instance = await reddit.subreddit(subreddit)
    search_results = subreddit_instance.search(query, limit=limit)

    # Parse the results
    posts = []
    async for post in search_results:
        posts.append({
            'title': post.title,
            'score': post.score,
            'url': post.url,
            'subreddit': post.subreddit.display_name,
            'created': datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
            'num_comments': post.num_comments
        })
    
    return posts

# Main function to run the Streamlit app
async def main():
    st.title("Reddit Scraper")

    # Input fields for the user
    search_query = st.text_input("Search Query", "racing post")
    target_subreddit = st.text_input("Subreddit", "HorseRacingUK")
    limit = st.number_input("Number of Results", min_value=1, max_value=100, value=5)

    if st.button("Search"):
        with st.spinner("Fetching results..."):
            reddit = await connect_to_reddit()
            results = await search_reddit(reddit, search_query, target_subreddit, limit)

            if results:
                # Display results in a dataframe
                df = pd.DataFrame(results)
                st.write(df)

                # Optionally, allow the user to download the results as CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download as CSV",
                    data=csv,
                    file_name='reddit_search_results.csv',
                    mime='text/csv',
                )
            else:
                st.warning("No results found.")

# Run the main function in a Streamlit app
if __name__ == "__main__":
    asyncio.run(main())
