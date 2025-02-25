'use client';
import React, { useState, useEffect, useRef } from 'react';
import dynamic from 'next/dynamic';
import {ChevronDown, ChevronRight} from "lucide-react";
const Plot = dynamic(()=> {return import ("react-plotly.js")}, {ssr: false})


function CollapsibleDetails() {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="text-sm font-light tracking-wide text-red-200/60">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center gap-1 hover:text-red-200/80 transition-colors"
      >
        {isExpanded ? (
          <ChevronDown className="w-4 h-4" />
        ) : (
          <ChevronRight className="w-4 h-4" />
        )}
        <span>Data & Visualization Details</span>
      </button>

      {isExpanded && (
        <div className="mt-2 ml-5 space-y-2">
          <p>
            Feature values are <i>normalized</i> to ensure consistent scaling across all features,
            so the magnitude of a category represents its z-score (i.e. how many standard deviations
            it is from the mean of all DJs' features).
          </p>

          <p>
            For example, a sample DJ with a 'Danceability' of -1.0 indicates that the average
            danceability of tracks played by that DJ are 1 standard deviation below the mean
            danceability of every track played by all DJs. The conclusion: the DJ created for
            this example is not a great option (relative to every other KXSC DJ) if you're
            looking for some tunes to dance to.
          </p>

          <p>
            The mood features followed by "_Index" (e.g. Sad Index) are a normalized average
            of a DJ's high-level mood data confidence. Higher index levels mean that a given
            DJ likely plays tracks that exhibit greater "Sad" qualities relative to other DJs,
            and vice versa.
          </p>
        </div>
      )}
    </div>
  );
}

export default function MatchAnalysis({ figure }) {
  const containerRef = useRef(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

  const figureObj = JSON.parse(figure);

  useEffect(() => {
    const updateSize = () => {
      if (containerRef.current) {
        const { width } = containerRef.current.getBoundingClientRect();
        setDimensions({
          width: width,
          height: width * 0.8
        });
      }
    };

    // Initial size
    updateSize();

    // Add resize listener
    const resizeObserver = new ResizeObserver(updateSize);
    if (containerRef.current) {
      resizeObserver.observe(containerRef.current);
    }

    // Cleanup
    return () => {
      if (containerRef.current) {
        resizeObserver.unobserve(containerRef.current);
      }
    };
  }, []);

  const getResponsiveLayout = () => {
    const baseLayout = figureObj.layout || {};

    return {
      ...baseLayout,
      width: dimensions.width,
      height: dimensions.width * 0.8,
      paper_bgcolor: "rgba(0,0,0,0)",
      showlegend: true,
      legend: {
        x: 0.5,
        y: 1.2,
        xanchor: 'center',
        yanchor: 'top',
        orientation: 'h',
        font: {
          color: '#9CA3AF'
        },
        bgcolor: 'transparent'
      },
      // Center the figure within the box
      margin: {
        l: 40,
        r: 40,
        t: 40,
        b: 40
      },
      polar: {
        ...(baseLayout.polar || {}),
        radialaxis: {
          ...(baseLayout.polar?.radialaxis || {}),
          visible: true,
          showline: false,
          color: '#9CA3AF',  // Axis label color
          gridcolor: 'rgba(156, 163, 175, 0.1)', //  Radius lines color

        },
        angularaxis: {
          ...(baseLayout.polar?.angularaxis || {}),
          color: '#9CA3AF',  // Category label text color
          linecolor: 'rgba(156, 163, 175, 0.5)',  // Outermost radius color
          gridcolor: 'rgba(156, 163, 175, 0.1)', //  Outward lines color
        },
        bgcolor: 'transparent'
      }
    };
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-2xl p-8">
        <h2 className="text-2xl font-bold mb-6 bg-gradient-to-r from-purple-400 to-red-400 bg-clip-text text-transparent">
          Match Analysis
        </h2>
        <div
          ref={containerRef}
          className="w-full bg-white/5 rounded-xl flex items-center justify-center border border-white/10"
        >
          {dimensions.width > 0 && figureObj?.data ? (
            <Plot
              data={figureObj.data}
              layout={getResponsiveLayout()}
              config={{
                displayModeBar: false,
                responsive: true,
                dragmode: false
              }}
            />
          ) : (
            <p className="text-gray-400">Loading Spider Chart...</p>
          )}
        </div>
      </div>

      <div className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-2xl p-8">
        <h2 className="text-2xl font-bold mb-6 bg-gradient-to-r from-purple-400 to-red-400 bg-clip-text text-transparent">
          How We Matched You
        </h2>
        <div className="space-y-4">
          <div className="text-lg font-light tracking-wide text-red-200/80">
          <p>
            Key audio features from the top tracks of the artists you
            select are computed to create your <span className="font-semibold italic tracking-wide underline underline-offset-2">unique musical profile</span>.
            This includes:
          </p>
          <ul className="my-3 ml-2 space-y-2">
            <li className="list-disc list-inside">
              Your desired mood
            </li>
            <li className="list-disc list-inside">
              Artists you selected from their play history
            </li>
            <li className="list-disc list-inside">
              Audio metadata
            </li>
          </ul>
          <p className="text-lg font-light tracking-wide text-red-200/80">
            Your DJ Match is the KXSC DJ most aligned with your musical feature array.
          </p>
        </div>
          <CollapsibleDetails/>
        </div>
      </div>
    </div>
);
}

