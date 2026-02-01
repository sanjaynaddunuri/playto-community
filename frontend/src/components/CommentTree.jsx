export default function CommentTree({ comments, depth = 0 }) {
  if (!comments || comments.length === 0) return null;

  return (
    <div className="space-y-2 mt-3">
      {comments.map(c => (
        <div
          key={c.id}
          className="pl-3 border-l border-gray-600"
          style={{ marginLeft: depth * 12 }}
        >
          <p className="text-green-400 text-sm">
            @{c.author}
          </p>
          <p className="text-gray-300 text-sm">
            {c.content}
          </p>

          <CommentTree
            comments={c.replies}
            depth={depth + 1}
          />
        </div>
      ))}
    </div>
  );
}
