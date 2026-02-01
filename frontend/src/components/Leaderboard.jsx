import { useEffect, useState } from "react";
import api from "../api";

export default function Leaderboard() {
  const [leaders, setLeaders] = useState([]);

  useEffect(() => {
    api.get("leaderboard/")
      .then(res => setLeaders(res.data))
      .catch(() => {});
  }, []);

  return (
    <div className="bg-gray-800 p-5 rounded-xl sticky top-6">
      <h2 className="text-yellow-400 font-bold text-xl mb-4">
        🏆 Leaderboard (24h)
      </h2>

      {leaders.length === 0 && (
        <p className="text-gray-400 text-sm">
          No activity yet
        </p>
      )}

      <ul className="space-y-2">
        {leaders.map((u, i) => (
          <li
            key={i}
            className="flex justify-between bg-gray-700 px-3 py-2 rounded"
          >
            <span>@{u.user__username}</span>
            <span className="font-bold">{u.total_karma}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
