"use client"
 
import Banner from "@/components/Banner";
import Card from "@/components/Card";
import Navbar from "@/components/Navbar";
import SearchBar from "@/components/SearchBar";
import { useChatStore } from "@/store/store";
import React, { useEffect, useState } from "react"
export default function Home() {
    const fetchAllCats = useChatStore((state: any) => state.fetchAllCats)
    const cats = useChatStore((state: any) => state.cats)
    const page = useChatStore((state: any) => state.page)
    const setPage = useChatStore((state: any) => state.setPage)
    const totalPage = useChatStore((state: any) => state.totalPage);
    const isLoading = useChatStore((state: any) => state.isLoading);
    const activeTab = useChatStore((state: any) => state.activeTab);
    const query = useChatStore((state: any) => state.query);
    const selectedBreed = useChatStore((state: any) => state.selectedBreed);
    const fetchQuery = useChatStore((state: any) => state.fetchQuery);
    const fetchFavoriteCats = useChatStore((state: any) => state.fetchFavoriteCats)
    console.log(cats)

    useEffect(() => {
        fetchAllCats()
    }, [])
    const handleNextPage = () => {
        if (page < totalPage) {
            setPage(page + 1);
            if((query !== "" || selectedBreed !== "") && activeTab == "Features") {
                fetchQuery(query, selectedBreed)
            }
            else if(activeTab == "Favorites") {
                fetchFavoriteCats()
            }
            else {
                fetchAllCats()
            }
        }
        window.scrollTo({ top: 0 });
    };

    const handlePreviousPage = () => {
        if (page > 1) {
            setPage(page - 1);
            if((query !== "" || selectedBreed !== "") && activeTab == "Features") {
                fetchQuery(query, selectedBreed)
            }
            else if(activeTab == "Favorites") {
                fetchFavoriteCats()
            }
            else {
                fetchAllCats()
            }
        }
        window.scrollTo({ top: 0 });
    };
    return (
        <div className="flex flex-col p-4 space-y-4 h-screen max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8 gap-2">
            <Navbar />
            <SearchBar/>
            <div className="flex flex-col p-4 space-y-4 h-screen max-w-screen-lg mx-auto px-4 sm:px-6 lg:px-8 gap-2 pb-2">
                {cats.map((cat: any) => (
                    <Card key={cat.id} cat={cat} />  
                    ))
                }
                <div className="flex justify-between mt-4">
                    { page > 1 ?
                        (<button 
                            onClick={handlePreviousPage} 
                            disabled={page === 1} 
                            className="px-4 py-2 rounded-xl border border-gray-300 hover:scale-105"
                        >
                            Previous
                        </button>) : (
                            <div></div>
                        )
                    }
                    { page < totalPage ?
                        (<button 
                            onClick={handleNextPage} 
                            disabled={page === totalPage} 
                            className="px-4 py-2 rounded-xl border border-gray-300 hover:scale-105"
                        >
                            Next
                        </button>) : (
                            <div></div>
                        )
                    }
                </div>
                {/* <Banner/> */}
                <div className="h-4 pt-4"></div>
            </div>
        </div>
    );
}