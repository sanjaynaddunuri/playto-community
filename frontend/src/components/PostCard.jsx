import CommentTree from "./CommentTree";

export default function PostCard({ post, onLike }) {
  return (
    <div className="bg-gray-800 rounded-xl p-6 shadow-lg hover:shadow-xl transition">
      <div className="flex justify-between">
        <h3 className="text-blue-400 font-semibold">
          @{post.author}
        </h3>
        <span className="text-xs text-gray-400">
          Post #{post.id}
        </span>
      </div>

      <p className="mt-3 text-gray-200 leading-relaxed">
        {post.content}
      </p>

      <button
        onClick={() => onLike(post.id)}
        className="mt-4 text-pink-400 hover:text-pink-300"
      >
        ❤️ Like
      </button>

      <div className="mt-4">
        <CommentTree comments={post.comments} />
      </div>
    </div>
  );
}
