import React, { useState } from 'react';
import { breeds } from '../lib/constants'
import { useChatStore } from '@/store/store';

const SearchBar: React.FC = () => {
  const query = useChatStore((state) => state.query);
  const setQuery = useChatStore((state) => state.setQuery);
  const selectedBreed = useChatStore((state) => state.selectedBreed);
  const setSelectedBreed = useChatStore((state) => state.setSelectedBreed);
  const setPage = useChatStore((state) => state.setPage);
  const setTotalPage = useChatStore((state) => state.setTotalPage);
  const fetchQuery = useChatStore((state) => state.fetchQuery);
  const setActiveTab = useChatStore((state) => state.setActiveTab);

  const handleSearch = () => {
    console.log(selectedBreed, query);
    setActiveTab('Features')
    setPage(1);
    setTotalPage(1);
    fetchQuery(query, selectedBreed || 'All');
  };

  const handleBreedChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedBreed(e.target.value);
  };

  return (
    <div className="relative max-w-xl w-full mx-auto flex gap-2">
        <div className="relative">
            <select
                value={selectedBreed || 'All'}
                onChange={handleBreedChange}
                className="p-2 border dark:border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer"
            >
                { breeds.map((breed) => (
                    <option key={breed} value={breed}>
                    {breed}
                    </option>
                ))}
            </select>
        </div>
        <div className='relative w-full'>
            <input 
                className="w-full py-2 px-4 border dark:border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" 
                type="search" 
                placeholder="Search"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
            />
            <button 
                className="absolute inset-y-0 right-0 flex items-center px-4 text-gray-700 bg-gray-100 border dark:border-gray-300 rounded-r-xl hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                onClick={handleSearch}
            >
                <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" clip-rule="evenodd" d="M14.795 13.408l5.204 5.204a1 1 0 01-1.414 1.414l-5.204-5.204a7.5 7.5 0 111.414-1.414zM8.5 14A5.5 5.5 0 103 8.5 5.506 5.506 0 008.5 14z" />
                </svg>
            </button>
        </div>
    </div>
  );
};

export default SearchBar;