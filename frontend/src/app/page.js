import React from 'react';
import Link from 'next/link'
import { ChevronRight, Radio, Music, Headphones } from 'lucide-react';
import TypingAnimation from "@/components/TypingAnimation";

export default function Home() {
  return (
    <div className="relative">
      {/* Background gradient blur effect */}
      <div className="absolute inset-0 bg-gradient-to-r from-purple-500/10 via-red-500/10 to-orange-500/10 blur-3xl -z-10"/>

      {/* Main content container */}
      <div className="max-w-4xl mx-auto text-center pt-8">
        {/* Hero Section */}
        <h1 className="text-6xl font-mono font-bold italic mb-6 bg-gradient-to-r from-purple-400 via-red-400 to-orange-400 bg-clip-text text-transparent">
          Find Your DJ Match
        </h1>

        <div className="h-16 mb-16">
          <TypingAnimation>
            <p className="md:text-xl font-mono text-gray-300 max-w-2xl mx-auto leading-relaxed">
              Discover which KXSC DJ is most <span
                className="font-semibold text-gray-100">statistically similar</span> to your music taste through our
              matching algorithm.
            </p>
          </TypingAnimation>
        </div>


        {/*Temporarily Paused Services display box*/}
        {/* <div className="p-4 border border-red-400 text-red-400 rounded-md max-w-md mx-auto mb-4">
          <p className="font-semibold text-center italic">
            DJ Match services have been paused over the Summer and will resume next semester in Fall 2025
          </p>
        </div> */}


        <Link
            href="/choose-mood"
            className="inline-flex items-center space-x-2 px-8 py-4 bg-gradient-to-r from-purple-500 to-red-500 rounded-full text-gray-200 font-semibold hover:from-purple-600 hover:to-red-600 transition-all duration-300 hover:scale-105"
        >
          <span>Get Started</span>
          <ChevronRight className="w-5 h-5"/>
        </Link>


        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-24">
          {/* Feature 1 */}
          <div
              className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition-all duration-300">
            <div className="w-12 h-12 bg-purple-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <Radio className="w-6 h-6 text-purple-400"/>
            </div>
            <h3 className="text-xl font-semibold mb-2 text-gray-100">Personalized Radio</h3>
            <p className="text-gray-400">Begin your radio journey with KXSC DJs who share your music taste</p>
          </div>

          {/* Feature 2 */}
          <div
              className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition-all duration-300">
            <div className="w-12 h-12 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <Music className="w-6 h-6 text-red-400"/>
            </div>
            <h3 className="text-xl font-semibold mb-2 text-gray-100">Genre Deep Dives</h3>
            <p className="text-gray-400">Discover niche artists and hidden gems in your favorite genres</p>
          </div>

          {/* Feature 3 */}
          <div
              className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition-all duration-300">
            <div className="w-12 h-12 bg-orange-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <Headphones className="w-6 h-6 text-orange-400"/>
            </div>
            <h3 className="text-xl font-semibold mb-2 text-gray-100">Human-First Curation</h3>
            <p className="text-gray-400">Experience music handpicked by our fantastic DJs</p>
          </div>
        </div>

        {/* Disclaimer */}
        <footer className="mt-24 text-sm text-gray-400 max-w-2xl mx-auto">
          <p className="leading-relaxed">
            Your privacy matters. We <span className="font-semibold text-gray-300">never</span> store your personal
            data. This matching process is completely anonymous and secure.
          </p>
        </footer>
      </div>
    </div>
  );
}
