export default function ErrorState({ message }) {
  return (
    <div className="bg-red-900/40 border border-red-500 p-4 rounded-lg">
      <p className="text-red-300 font-semibold">{message}</p>
    </div>
  );
}
