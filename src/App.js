import React, { useState } from 'react';
import { QueryClient, QueryClientProvider, useInfiniteQuery } from 'react-query';
import axios from 'axios';
import BlogPost from './components/BlogPost';
import './App.css';

const queryClient = new QueryClient();

function BlogList() {
  const [filter, setFilter] = useState('');

  const fetchPosts = async ({ pageParam = 1 }) => {
    const { data } = await axios.post('http://localhost:8000/graphql', {
      query: `
        query($page: Int!) {
          blogPosts(page: $page, perPage: 10) {
            id
            title
            content
            date
            blogName
          }
          totalPosts
        }
      `,
      variables: { page: pageParam },
    });
    return data.data;
  };

  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    status,
  } = useInfiniteQuery('posts', fetchPosts, {
    getNextPageParam: (lastPage, pages) => {
      if (!lastPage || !lastPage.totalPosts) return undefined;
      const totalPages = Math.ceil(lastPage.totalPosts / 10);
      if (pages.length < totalPages) {
        return pages.length + 1;
      }
      return undefined;
    },
  });

  if (status === 'loading') return <div>Loading...</div>;
  if (status === 'error') return <div>Error fetching data</div>;

  const filteredPosts = data?.pages.flatMap(page => 
    page.blogPosts.filter(post => 
      post.title.toLowerCase().includes(filter.toLowerCase()) ||
      post.content.toLowerCase().includes(filter.toLowerCase())
    )
  ) || [];

  return (
    <div className="blog-list">
      <input
        type="text"
        placeholder="Filter posts..."
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        className="filter-input"
      />
      {filteredPosts.map(post => (
        <BlogPost key={post.id} post={post} />
      ))}
      {hasNextPage && (
        <button onClick={() => fetchNextPage()} disabled={isFetchingNextPage} className="load-more">
          {isFetchingNextPage ? 'Loading more...' : 'Load More'}
        </button>
      )}
    </div>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="App">
        <h1>Blog Posts</h1>
        <BlogList />
      </div>
    </QueryClientProvider>
  );
}

export default App;