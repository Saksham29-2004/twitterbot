import React, { useState } from 'react';
import axios from 'axios';

const ArticleTable = ({ articles }) => {
  const [tweetingStatus, setTweetingStatus] = useState({});  // To keep track of tweet status per article

  if (!Array.isArray(articles) || articles.length === 0) {
    return <div>No articles available.</div>;
  }

  const handleTweet = async (articleId, tweetContent) => {
    setTweetingStatus((prevStatus) => ({ ...prevStatus, [articleId]: 'Tweeting...' }));

    try {
        const response = await axios.post('http://127.0.0.1:8000/scrapers/tweet', {
        content: tweetContent,
        });

        if (response.data.status === 'success') {
        setTweetingStatus((prevStatus) => ({ ...prevStatus, [articleId]: 'Tweeted' }));
        } else {
        setTweetingStatus((prevStatus) => ({ ...prevStatus, [articleId]: 'Failed' }));
        }
    } catch (error) {
        setTweetingStatus((prevStatus) => ({ ...prevStatus, [articleId]: 'Error' }));
    }
    };


  return (
    <table className="article-table">
      <thead>
        <tr>
          <th>Source</th>
          <th>Title</th>
          <th>Status</th>
          <th>Tweet</th>
          <th>Chars</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {articles.map((article) => {
          if (!article.title || !article.source) return null; // Skip incomplete data

          const tweetContent = `Check out this article: ${article.title} - ${article.url}`;

          return (
            <tr key={article.id} className="table-row">
              <td>{article.source}</td>
              <td>{article.title}</td>
              <td>
                <span className={`status-badge ${article.status}`}>
                  {article.status}
                </span>
              </td>
              <td style={{ maxWidth: '350px' }}>{article.tweet}</td>
              <td>{article.tweet?.length}/280</td>
              <td>
                <button
                  className="btn tweet-btn"
                  onClick={() => handleTweet(article.id, tweetContent)}
                  disabled={tweetingStatus[article.id] === 'Tweeting...'}
                >
                  {tweetingStatus[article.id] === 'Tweeting...' ? 'Tweeting...' : 'Tweet'}
                </button>
                <button className="btn retry-btn">Retry</button>
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};

export default ArticleTable;
