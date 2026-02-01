import Feed from "./components/Feed";
import Leaderboard from "./components/Leaderboard";

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-white p-6 grid grid-cols-4 gap-6">
      <div className="col-span-3">
        <h1 className="text-3xl font-bold mb-6">
          Community Feed
        </h1>
        <Feed />
      </div>
      <Leaderboard />
    </div>
  );
}

export default App;
