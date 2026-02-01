import { useEffect, useState } from "react";
import api from "../api";
import PostCard from "./PostCard";
import Loading from "./Loading";
import ErrorState from "./ErrorState";

export default function Feed() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("posts/")
      .then(res => setPosts(res.data))
      .catch(err => {
        console.error(err);
        setError("Failed to load feed. Backend not responding.");
      })
      .finally(() => setLoading(false));
  }, []);

  const likePost = (postId) => {
    api.post("like/", { user_id: 1, post_id: postId })
      .catch(() => alert("Already liked"));
  };

  if (loading) return <Loading />;
  if (error) return <ErrorState message={error} />;

  return (
    <div className="space-y-6">
      {posts.length === 0 && (
        <p className="text-gray-400">No posts yet</p>
      )}

      {posts.map(post => (
        <PostCard
          key={post.id}
          post={post}
          onLike={likePost}
        />
      ))}
    </div>
  );
}
