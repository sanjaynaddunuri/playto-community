export default function Loading() {
  return (
    <div className="space-y-4 animate-pulse">
      {[1, 2, 3].map(i => (
        <div key={i} className="h-28 bg-gray-800 rounded-xl"></div>
      ))}
    </div>
  );
}
