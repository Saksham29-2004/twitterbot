import { useEffect, useState } from "react";
import ArticleTable from "../components/ArticleTable";

export default function Overview() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/scrapers/api/news")
      .then((res) => res.json())
      .then((data) => {
        console.log("RSS DATA FROM BACKEND:", data);
        setArticles(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Fetch failed:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return (
    <div className="loading-spinner">
      <div className="spinner"></div> Loading RSS feeds...
    </div>
  );

  return (
    <div className="dashboard-container">
      <h2 className="dashboard-title">Latest RSS News</h2>
      <ArticleTable articles={articles} />
    </div>
  );
}
