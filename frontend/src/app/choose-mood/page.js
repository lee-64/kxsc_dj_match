'use client'
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import MoodSelector from '@/components/MoodSelector';
import Hero from '@/components/Hero';

export default function ChooseMood() {
  const router = useRouter()
  const [status, setStatus] = useState('idle');
  const [errorMessage, setErrorMessage] = useState('');
  const handleMoodSelect = async (mood) => {
    setStatus('loading');
    localStorage.setItem('selectedMood', mood);
    try {
      const response = await axios.post('/api/mood', { mood });
      if (response.status === 200) {
        setStatus('success');
        router.push('/include-artists');
      } else {
        setStatus('error');
        setErrorMessage('Failed to send mood. Please try again.');
        localStorage.removeItem('selectedMood');  // Remove from localStorage on failure
      }
    } catch (error) {
      console.error('Error sending mood:', error);
      setStatus('error');
      setErrorMessage('Error sending mood. Please try again.');
    }
  };
  return (
    <>
      <Hero header="Choose Your Music Mood" description="Select the mood that best matches your current vibe"/>
      <div className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-2xl p-8 mb-16">
        <MoodSelector onMoodSelect={handleMoodSelect} />
        {/* Status Messages */}
        {/*{status === 'loading' && (*/}
        {/*  <div className="mt-8 text-center">*/}
        {/*    <p className="text-gray-300 font-mono tracking-tighter">Processing your selection...</p>*/}
        {/*  </div>*/}
        {/*)}*/}
        {status === 'error' && (
          <div className="mt-8 text-center">
            <p className="text-red-400 font-mono tracking-tighter">{errorMessage}</p>
          </div>
        )}
      </div>
    </>
  );
}

