"use client"
 
import React, { useState } from "react"
import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"
import { Button } from "@/components/ui/button"


const Darkmode = () => {
    const { setTheme } = useTheme()
    const [darkMode, setDarkMode] = useState(false)

    const toggleTheme = () => {
        setDarkMode(prev => !prev)
        if(darkMode) {
            setTheme("dark")
        } else {
            setTheme("light")
        }
    }
    return (
        <div className="mb-2 md:hover:scale-110">
            <Button variant="outline" size="icon" onClick={toggleTheme} className="rounded" >
                <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
                <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
                <span className="sr-only">Toggle theme</span>
            </Button>
        </div>

    );
}

export default Darkmode