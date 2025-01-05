import React from 'react';

export default function AutocompleteDropdown({ suggestions, onSelect }) {
  return (
    <ul
      className="max-h-64 overflow-y-auto"
      role="listbox"
    >
      {suggestions.map((suggestion, index) => (
        <li
          key={suggestion.mbid || index}
          role="option"
          className="px-4 py-3 hover:bg-white/10 cursor-pointer text-gray-800 transition-colors duration-200"
          onClick={() => onSelect(suggestion)}
        >
          {suggestion.name}
        </li>
      ))}
    </ul>
  );
}