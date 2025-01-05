import React from 'react';
import { Music, X, Search, Loader2 } from 'lucide-react';

export default function ArtistList({ artists, onRemoveArtist }) {
  return (
    <div className="mt-6">
      <div className="flex items-center space-x-3 mb-4">
        <Music className="w-5 h-5 text-purple-400" />
        <h2 className="text-xl font-bold bg-gradient-to-r from-purple-400 to-red-400 bg-clip-text text-transparent">
          Added Artists ({artists.length}/3)
        </h2>
      </div>

      <ul className="space-y-2">
        {artists.map((artist, index) => (
          <li
            key={index}
            className="flex justify-between items-center backdrop-blur-sm bg-white/5 border border-white/10 rounded-xl p-3 group hover:bg-white/10 transition-colors duration-200"
          >
            <span className="text-gray-500">{artist.name}</span>
            <button
              onClick={() => onRemoveArtist(index)}
              className="text-red-400 hover:text-red-300 transition-colors duration-200"
            >
              <X className="w-5 h-5" />
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}