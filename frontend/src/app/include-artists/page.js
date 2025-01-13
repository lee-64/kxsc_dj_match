'use client';
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation'
import { Music, Loader2 } from 'lucide-react';
import ArtistSearch from '@/components/ArtistSearch';
import ArtistList from '@/components/ArtistList';
import axios from 'axios';
import Hero from "@/components/Hero";

export default function IncludeArtists() {
  const router = useRouter()
  const [artists, setArtists] = useState([]);
  const [status, setStatus] = useState('idle'); // 'idle' | 'submitting' | 'success' | 'error'
  const [errorMessage, setErrorMessage] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check localStorage after component mounts
    if (typeof window !== 'undefined' && !localStorage.getItem('selectedMood')) {
      router.push('/choose-mood');
    }
    setIsLoading(false);
  }, [router]);

  // Show nothing while checking localStorage
  if (isLoading) {
    return null;
  }

  const handleAddArtist = (artist) => {
    if (artists.length >= 3) {
      alert('You can add up to 3 artists.');
      return;
    }
    setArtists([...artists, artist]);
  };

  const handleRemoveArtist = (index) => {
    const updatedArtists = artists.filter((_, i) => i !== index);
    setArtists(updatedArtists);
  };

  const handleSubmit = async () => {
    if (artists.length === 0) {
      alert('Please add at least one artist.');
      return;
    }
    setStatus('submitting');
    try {

      localStorage.setItem('selectedArtists', JSON.stringify(artists));

      const response = await axios.post('/api/artists', {
        artists_data: artists,
      });
      if (response.status === 200) {
        await response.data;  // Wait for the response data to be processed
        router.push('/results');
      } else {
        setStatus('error');
        setErrorMessage('Failed to submit artists. Please try again.');
      }
    } catch (error) {
      console.error('Error submitting artists:', error);
      setStatus('error');
      setErrorMessage('Error submitting artists. Please try again.');
    }
  };

return (
    <>
      <Hero header="Add Artists" description="Include some of your favorite artists"/>
      <div className="bg-white/5 border border-white/10 rounded-2xl p-8 shadow-2xl max-w-2xl mx-auto">
        <ArtistSearch onAddArtist={handleAddArtist} disabled={artists.length >= 3} />
        <ArtistList artists={artists} onRemoveArtist={handleRemoveArtist} />

        <button
          onClick={handleSubmit}
          disabled={status === 'submitting'}
          className="mt-8 w-full py-3 bg-gradient-to-r from-purple-500/20 to-red-500/20 border border-purple-500/30 text-purple-400 rounded-xl hover:from-purple-500/30 hover:to-red-500/30 transition-all duration-300 flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {status === 'submitting' ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Finding Your Match...</span>
            </>
          ) : (
            <>
              <Music className="w-5 h-5" />
              <span>Find My DJ Match</span>
            </>
          )}
        </button>

        {status === 'error' && (
          <p className="mt-4 text-red-400 text-center">{errorMessage}</p>
        )}
      </div>
    </>
  );
}