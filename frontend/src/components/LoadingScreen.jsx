import React, { useState, useEffect } from 'react';
import { Loader2 } from 'lucide-react';

export default function LoadingScreen({ artists }) {
  const [currentMessage, setCurrentMessage] = useState('');
  const [progress, setProgress] = useState(0);

  // Loading messages based on user's selected artists
  const loadingMessages = [
    "Initializing music analysis...",
    ...artists.map(artist => `Analyzing ${artist}'s musical features...`),
    "Comparing with our DJ database...",
    "Calculating compatibility scores...",
    "Finding your perfect DJ match...",
    "Generating personalized insights..."
  ];

  // TODO add kxsc-themed loading messages

  useEffect(() => {
    let currentIndex = 0;
    const totalDuration = artists.length * 10000;
    const stepDuration = totalDuration / loadingMessages.length;  // Duration per message

    const messageInterval = setInterval(() => {
      if (currentIndex < loadingMessages.length) {
        setCurrentMessage(loadingMessages[currentIndex]);
        setProgress((currentIndex + 1) * (100 / loadingMessages.length));
        currentIndex++;
      } else {
        clearInterval(messageInterval);
      }
    }, stepDuration);

    return () => clearInterval(messageInterval);
  }, []);

  return (
  <div className="fixed inset-0 text-white flex flex-col items-center justify-center p-4 z-50">
    <div className="max-w-md w-full space-y-8">
      {/* Animated Logo/Icon */}
      <div className="flex justify-center">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-purple-500/20 via-red-500/20 to-orange-500/20 blur-xl animate-pulse" />
            <Loader2 className="w-16 h-16 text-white animate-spin" />
          </div>
        </div>

        {/* Progress Bar */}
        <div className="relative pt-1">
          <div className="flex mb-2 items-center justify-between">
            <div>
              <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full bg-purple-500/20 text-purple-300">
                Loading
              </span>
            </div>
            <div className="text-right">
              <span className="text-xs font-semibold inline-block text-purple-300">
                {Math.round(progress)}%
              </span>
            </div>
          </div>
          <div className="overflow-hidden h-2 mb-4 text-xs flex rounded-full bg-purple-500/20">
            <div
              style={{ width: `${progress}%` }}
              className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-gradient-to-r from-purple-500 to-red-500 transition-all duration-500"
            />
          </div>
        </div>

        {/* Loading Message */}
        <div className="text-center">
          <h2 className="text-xl font-semibold mb-2 bg-gradient-to-r from-purple-400 to-red-400 bg-clip-text text-transparent">
            Finding Your DJ Match
          </h2>
          <p className="text-gray-400 animate-pulse">
            {currentMessage}
          </p>
        </div>
      </div>
    </div>
  );
}