import React from 'react';

const MoodButton = ({ mood, onMoodSelect }) => {
  return (
    <button
      onClick={() => onMoodSelect(mood)}
      className="group w-full"
    >
      <div className="bg-white/5 border border-white/10 rounded-xl p-6 text-center transform transition-all duration-300 hover:-translate-y-2">
        <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-red-500 rounded-full mx-auto mb-4 flex items-center justify-center ring-2 ring-white/10 ring-offset-2 ring-offset-black">
          <span className="text-xl font-bold text-white">{mood.charAt(0).toUpperCase()}</span>
        </div>
        <p className="font-semibold text-gray-100 mb-1">{mood}</p>
        <p className="text-sm text-red-200/80">Select this mood</p>
      </div>
    </button>
  );
};


export default function MoodSelector({ onMoodSelect }) {
  const moods = ['Relaxed', 'Happy', 'Sad', 'Aggressive', 'Electronic', 'Party', 'Acoustic'];
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      {moods.map((mood) => (
        <MoodButton
          key={mood}
          mood={mood}
          onMoodSelect={onMoodSelect}
        />
      ))}
    </div>
  );
}