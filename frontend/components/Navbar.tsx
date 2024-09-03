import React, { useState } from 'react'
import Darkmode from './DarkMode'
import { useChatStore } from '@/store/store';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const activeTab = useChatStore((state: any) => state.activeTab);
  const setActiveTab = useChatStore((state: any) => state.setActiveTab);
  const fetchFavoriteCats = useChatStore((state: any) => state.fetchFavoriteCats)
  const fetchAllCats = useChatStore((state: any) => state.fetchAllCats)
  const setPage = useChatStore((state: any) => state.setPage)
  const setTotalPage = useChatStore((state: any) => state.setTotalPage)
  const setQuery = useChatStore((state: any) => state.setQuery)
  const setSelectedBreed = useChatStore((state: any) => state.setSelectedBreed)
  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const handleTabClick = (tabName: string) => {
    setActiveTab(tabName);
    setIsOpen(!isOpen);
    setPage(1)
    setTotalPage(1)
    if (tabName === 'Favorites') {
      setQuery('')
      setSelectedBreed('')
      fetchFavoriteCats()
    } else {
      fetchAllCats()
    }
  };

  return (
    <nav className="relative z-50">
      <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
        <div className="flex items-center space-x-3 rtl:space-x-reverse cursor-pointer">
            <span 
              className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white md:text-3xl"
              onClick={() => setActiveTab('Features')}
            >
              Cats
            </span>
        </div>
        <button  
          className="inline-flex items-center p-2 w-10 h-10 justify-center text-sm rounded-lg md:hidden focus:outline-none"
          onClick={toggleMenu}
        >
          <svg className="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h15M1 7h15M1 13h15"/>
          </svg>
        </button>
        <div className={`w-full md:block md:w-auto ${isOpen ? 'block' : 'hidden'} absolute top-16 left-1 md:static md:flex md:space-x-8 md:mt-0 md:border-0 bg-primary-foreground md:bg-background`}>
          <ul className="font-medium flex flex-col p-4 md:p-0 rounded-lg md:flex-row md:space-x-8 rtl:space-x-reverse">
            <li>
              <p 
                className={`block py-2 px-3 cursor-pointer rounded md:hover:scale-110 transition-transform duration-300 ease-in-out md:text-xl ${activeTab === 'Features' ? 'border-b-2' : ''}`}
                onClick={() => handleTabClick('Features')}
              >
                Features
              </p>
            </li>
            <li>
              <p 
                className={`block py-2 px-3 cursor-pointer rounded md:hover:scale-110 transition-transform duration-300 ease-in-out md:text-xl ${activeTab === 'Favorites' ? 'border-b-2' : ''}`}
                onClick={() => handleTabClick('Favorites')}
              >
                Favorites
              </p>
            </li>
            <li className='mt-2 ml-2 md:mt-1 md:ml-0'>
              <Darkmode />
            </li>
          </ul>
        </div>
      </div>
    </nav>
  )
}

export default Navbar