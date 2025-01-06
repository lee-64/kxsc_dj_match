'use client';
import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Music, Clock, Radio, User, ChevronLeft } from 'lucide-react';
import MatchAnalysis from '@/components/MatchAnalysis';
import LoadingScreen from "@/components/LoadingScreen";
import Hero from "@/components/Hero";


export default function Results() {
  const [matchData, setMatchData] = useState({});
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchWithTimeout = async (url, timeout = 30000) => {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      const response = await fetch(url, {
        signal: controller.signal
      });
      clearTimeout(timeoutId);
      return response;
    } catch (error) {
      clearTimeout(timeoutId);
      throw error;
    }
  };

  useEffect(() => {
    const fetchResults = async () => {
      try {
        // Check for cached results
        const cachedData = localStorage.getItem('djMatchResults');
        if (cachedData) {
          const {results, timestamp} = JSON.parse(cachedData);
          const now = new Date().getTime();
          const cacheAge = now - timestamp;
          const CACHE_DURATION = 1000 * 60 * 5;

          if (cacheAge < CACHE_DURATION) {
            setMatchData(results);
            setIsLoading(false);
            return;
          } else {
            localStorage.removeItem('djMatchResults');
          }
        }

        const response = await fetchWithTimeout('/api/results', 45000);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();

        try {
          localStorage.setItem('djMatchResults', JSON.stringify({
            results: data.results,
            timestamp: new Date().getTime()
          }));
        } catch (storageError) {
          console.warn('Failed to cache results:', storageError);
        }

        setMatchData(data.results);
      } catch (error) {
        console.error('Error fetching results:', error);
        setError(error.message);

        // Try to fall back to cached data
        try {
          const cachedData = localStorage.getItem('djMatchResults');
          if (cachedData) {
            const {results} = JSON.parse(cachedData);
            setMatchData(results);
            setError('Using cached data - Unable to fetch latest results');
          }
        } catch (fallbackError) {
          setMatchData({});
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchResults();
  }, []);

  const handleReload = async () => {
    try {
      setIsLoading(true);
      setError(null);
      localStorage.removeItem('djMatchResults');

      const response = await fetchWithTimeout('/api/results', 45000);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();

      localStorage.setItem('djMatchResults', JSON.stringify({
        results: data.results,
        timestamp: new Date().getTime()
      }));

      setMatchData(data.results);
    } catch (error) {
      console.error('Error fetching new results:', error);
      setError('Failed to get new match. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  // Get selectedArtists from localStorage once when component mounts
  const selectedArtists = (() => {
    try {
      // TODO localStorage.getItem('selectedArtists') should only be accessed during the LoadingScreen. If the user simply refreshes the results page (and so the LoadingScreen isn't used), selectedArtists should not be accessed.
      const stored = localStorage.getItem('selectedArtists');
      return stored ? JSON.parse(stored) : [];
    } catch (e) {
      console.error('Error reading selectedArtists from localStorage:', e);
      return [];
    }
  })();

  const artistNames = selectedArtists.map(artist => artist.name);

  if (isLoading) {
    return <LoadingScreen artists={artistNames}/>;
  }


  if (error) {
    return (
        <div className="min-h-screen text-gray-200 flex flex-col items-center justify-center">
          <p className="text-red-500 mb-4">Error: {error}</p>
          <button
              onClick={handleReload}
              className="px-4 py-2 bg-red-800 text-white rounded hover:bg-red-700 transition-colors"
          >
            Try Again
          </button>
        </div>
    );
  }

  return (
      <>
        <div className="container mx-auto -mt-16 px-4 py-12">
          {/* Title Section */}
          <div className="text-center mb-8 relative">
            <div className="absolute inset-0 bg-gradient-to-r from-purple-500/10 via-red-500/10 to-orange-500/10 blur-3xl -z-10"/>

            <h1 className="text-4xl -tracking-tight italic font-bold mb-8 bg-gradient-to-r from-purple-400 via-red-400 to-orange-400 bg-clip-text text-transparent">
              Your DJ Match is...
            </h1>

            {/* Hero Component */}
            <Hero
                header={matchData.dj_match}
                description={
                  <span className="flex items-center justify-center space-x-2 text-gray-300">
                    <Clock className="w-4 h-4"/>
                    <span className="font-mono tracking-tighter">
                      {matchData.timeslot} at{" "}
                      <Link
                          className="text-blue-500 underline hover:text-blue-700"
                          href={'https://kxsc.org'}
                      >
                        kxsc.org
                      </Link>
                    </span>
                    <span className="mx-2">•</span>
                    <Radio className="w-4 h-4"/>
                    <p className="font-mono tracking-tighter">&ldquo;{matchData.show_name}&rdquo;</p>
                  </span>
                }
                fullWidth={true}
            />

            {/* Reset Button */}
            <button
                onClick={() => {
                  localStorage.removeItem('djMatchResults');
                  window.location.href = '/choose-mood';
                }}
                className="mt-3 px-6 py-2 bg-red-600/20 border border-red-500/30 text-red-400 rounded-full hover:bg-red-500/30 transition-all duration-300 flex items-center mx-auto space-x-2"
            >
              <ChevronLeft className="w-4 h-4"/>
              <span>Start Over</span>
            </button>
          </div>

          {/* Info Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
            {/* Recent Songs Card */}
            <div className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-2xl p-8">
              <div className="flex items-center space-x-3 mb-6">
                <Music className="w-6 h-6 text-purple-400"/>
                <h2 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-red-400 bg-clip-text text-transparent">
                  Recent Songs
                </h2>
              </div>
              <ul className="space-y-4">
                {matchData.recent_songs.map((track, index) => (
                    <li
                        key={index}
                        className="flex items-center space-x-4 group cursor-pointer"
                    >
                      <div
                          className="w-12 h-12 bg-red-500/10 border border-red-500/20 rounded-lg flex items-center justify-center group-hover:bg-red-500/20 group-hover:scale-105 transition-all duration-200">
                  <span className="text-red-400 font-mono">
                    {(index + 1).toString().padStart(2, '0')}
                  </span>
                      </div>
                      <span
                          className="tracking-wide text-red-200/80 group-hover:text-red-100/80 group-hover:scale-105 transition-all duration-200">
                  {track}
                </span>
                    </li>
                ))}
              </ul>
            </div>

            {/* About Card */}
            <div className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-2xl p-8">
              <div className="flex items-center space-x-3 mb-6">
                <User className="w-6 h-6 text-purple-400"/>
                <h2 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-red-400 bg-clip-text text-transparent">
                  About
                </h2>
              </div>
              <div className="space-y-4">
                <p className="text-lg font-light tracking-wide text-red-200/80">
                  {matchData.about_me}
                </p>
                <p className="text-base font-light tracking-wide text-red-200/60">
                  {matchData.mission_statement}
                </p>
                <div className="pt-4">
              <span className="text-sm uppercase tracking-widest text-red-400/80">
                Genres:{" "}
              </span>
                  <span className="text-sm text-red-300/60">
                Electronic • Jazz • Ambient • Downtempo
              </span>
                </div>
              </div>
            </div>
          </div>

          {/* Top Matches Section */}
          <div className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-2xl p-8 mb-16">
            <h2 className="text-2xl font-bold mb-8 text-center bg-gradient-to-r from-purple-400 to-red-400 bg-clip-text text-transparent">
              Your Top Matches
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
              {matchData.top_djs.map((dj, index) => (
                  <div key={dj} className="group">
                    <div
                        className="bg-white/5 border border-white/10 rounded-xl p-6 text-center transform transition-all duration-300 hover:-translate-y-2">
                      <div
                          className="w-16 h-16 bg-gradient-to-br from-purple-500 to-red-500 rounded-full mx-auto mb-4 flex items-center justify-center ring-2 ring-white/10 ring-offset-2 ring-offset-black">
                        <span className="text-xl font-bold">#{index + 1}</span>
                      </div>
                      <p className="font-mono font-semibold text-gray-100 mb-1">{dj}</p>
                      <p className="text-sm text-red-200/80">
                        {matchData.match_percentages[index]}% Match
                      </p>
                    </div>
                  </div>
              ))}
            </div>
          </div>

          {/* Match Analysis */}
          <MatchAnalysis figure={matchData.spider_fig}/>
        </div>
      </>
  );
}