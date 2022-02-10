import React from "react";
import reactDom from "react-dom";
import { BrowserRouter, useNavigate } from "react-router-dom";
import { useState } from "react";


function SearchBar() {
    const navigate = useNavigate();
    const [searchQuery, setSearchQuery] = useState("");

    const onSubmit = (e) => {
        navigate("./titles", { state: {query: searchQuery } });
        e.preventDefault();
    }
    

    return(
        <form action="/" method ="get" onSubmit={onSubmit}>
            <label htmlFor="header-search">
                <span className="visually-hidden">Search for Movies...</span>
            </label>
            <input
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                type="text"
                id="header-search"
                placeholder="Search for Movies..."
                name="s"
                />
            <button type="submit">Search</button>
        </form>
        )
    }

const root = document.getElementById("search");
reactDom.render(<BrowserRouter><SearchBar /></BrowserRouter>, root)