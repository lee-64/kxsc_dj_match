import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Search, Loader2 } from 'lucide-react';
import AutocompleteDropdown from '@/components/AutocompleteDropdown';
import axios from 'axios';
import { useDebounce } from 'use-debounce';

export default function ArtistSearch({ onAddArtist, disabled }) {
  const [input, setInput] = useState('');
  const [debouncedInput] = useDebounce(input, 300);
  const [suggestions, setSuggestions] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const containerRef = useRef(null);

  const fetchSuggestions = useCallback(async (query) => {
    if (!query) {
      setSuggestions([]);
      return;
    }
    setLoading(true);
    try {
      const response = await axios.get(`/api/search/artists`, {
        params: { query },
      });
      if (response.status === 200) {
        setSuggestions(response.data.artists_data);
      } else {
        setSuggestions([]);
      }
      setError(null);
    } catch (err) {
      console.error('Error fetching artist suggestions:', err);
      setError('Failed to fetch artist suggestions.');
      setSuggestions([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchSuggestions(debouncedInput);
  }, [debouncedInput, fetchSuggestions]);

  // Update showDropdown when we have input and suggestions
  useEffect(() => {
    if (debouncedInput && suggestions.length > 0) {
      setShowDropdown(true);
    } else {
      setShowDropdown(false);
    }
  }, [debouncedInput, suggestions]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleChange = (e) => {
    setInput(e.target.value);
    if (error) setError(null);
  };

  const handleFocus = () => {
    // Show dropdown on focus if we have input and suggestions
    if (input && suggestions.length > 0) {
      setShowDropdown(true);
    }
  };

  const handleSelectSuggestion = (suggestion) => {
    setInput('');
    setShowDropdown(false);
    onAddArtist({
      name: suggestion.name,
      mbid: suggestion.mbid
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() === '') return;
    onAddArtist(input.trim());
    setInput('');
    setShowDropdown(false);
  };

  return (
    <div className="relative" ref={containerRef}>
      <form onSubmit={handleSubmit}>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            value={input}
            onChange={handleChange}
            onFocus={handleFocus}
            placeholder="Type an artist name"
            className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 pl-10 pr-12 focus:outline-none focus:ring-2 focus:ring-purple-500/50 placeholder-gray-500 text-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={disabled}
            aria-autocomplete="list"
            aria-expanded={showDropdown}
            aria-controls="autocomplete-list"
            aria-activedescendant=""
          />
          {loading && (
            <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
              <Loader2 className="w-5 h-5 animate-spin text-gray-400" />
            </div>
          )}
        </div>
      </form>

      {error && (
        <div className="mt-2 text-red-400 text-sm">
          {error}
        </div>
      )}

      {showDropdown && suggestions.length > 0 && (
        <div className="absolute w-full mt-2 bg-white/50 backdrop-blur border border-white/10 rounded-xl shadow-2xl z-10 overflow-hidden">
          <AutocompleteDropdown
            id="autocomplete-list"
            suggestions={suggestions}
            onSelect={handleSelectSuggestion}
          />
        </div>
      )}
    </div>
  );
}