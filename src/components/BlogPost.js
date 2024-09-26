import React from 'react';

function BlogPost({ post }) {
  return (
    <div className="blog-post">
      <h2>{post.title}</h2>
      <p className="meta">
        <span>{post.blogName}</span> • <span>{post.date}</span>
      </p>
      <p>{post.content.substring(0, 200)}...</p>
    </div>
  );
}

export default BlogPost;