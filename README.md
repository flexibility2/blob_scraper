Code are in the branch of '**task1**', '**task2**', '**task3**'

# Task1

## Overview

This web crawler is designed to scrape blog posts from Protocol Labs and Ethereum blogs. It's built using Python and includes features for scheduling, error handling, and database storage.
![image](https://github.com/user-attachments/assets/3a95419f-4e7c-4d97-9a6e-d00e926d93c2)


## Key Components

1. **Scraper Function (`scrape_blog`):**

   - Uses `requests` to fetch web pages
   - Employs `BeautifulSoup` for HTML parsing
   - Implements site-specific scraping logic for each blog

2. **Database Integration (`store_in_database`):**

   - Uses SQLite for data storage
   - Stores blog post title, content, date, and blog name

3. **Scheduling (`schedule` library):**

   - Runs the scraper daily at midnight
   - Includes an initial run on startup

4. **Error Handling and Logging:**

   - Comprehensive logging using Python's `logging` module
   - Try-except blocks for robust error handling

5. **User-Agent Rotation:**
   - Randomly selects user agents to mimic different browsers

## Main Workflow

1. Scrape blogs (Protocol Labs and Ethereum)
2. Parse HTML and extract relevant information
3. Store scraped data in SQLite database
4. Repeat process daily

## API Integration (`main.py`)

- FastAPI-based GraphQL API
- Provides endpoints to query scraped blog posts
- Implements pagination for efficient data retrieval

## Deployment

- Dockerized application for easy deployment and scaling
- Combines scraper and API in a single container

## Future Improvements

- Add more blogs to scrape
- Implement more advanced scheduling (e.g., different frequencies for different blogs)
- Enhance error recovery mechanisms

# Task2

## Overview

This React application serves as a frontend for displaying blog posts scraped by the web crawler. It features infinite scrolling, filtering, and real-time updates using React Query.
![image](https://github.com/user-attachments/assets/f122ed21-d602-43f5-950d-f4f6fac9cdd9)


## Key Components

1. **App Component (`App.js`):**

   - Main component that wraps the entire application
   - Utilizes React Query's `QueryClientProvider`

2. **BlogList Component:**

   - Handles fetching and displaying blog posts
   - Implements infinite scrolling using `useInfiniteQuery`
   - Provides filtering functionality

3. **BlogPost Component (`BlogPost.js`):**

   - Renders individual blog post information

4. **Styling (`App.css`):**
   - Provides basic styling for the application

## Main Features

1. **Infinite Scrolling:**

   - Fetches posts in batches as the user scrolls
   - Utilizes React Query for efficient data fetching and caching

2. **Post Filtering:**

   - Allows users to filter posts based on title or content
   - Implements client-side filtering for quick results

3. **GraphQL Integration:**

   - Uses axios to send GraphQL queries to the backend
   - Fetches paginated blog post data

4. **Error Handling:**
   - Displays loading and error states to the user

## Data Flow

1. `useInfiniteQuery` fetches data from the GraphQL API
2. Data is stored and managed by React Query
3. `BlogList` component renders the fetched posts
4. User interactions (scrolling, filtering) trigger data updates

## Styling

- Responsive design with flexbox
- Simple and clean UI for easy reading

## Future Improvements

- Implement server-side filtering for better performance with large datasets
- Add sorting options for blog posts
- Enhance UI/UX with more interactive features
- Implement user authentication for personalized experiences
