import React from "react";
import reactDom from "react-dom";
import { BrowserRouter, useNavigate, } from "react-router-dom";
import { useState} from "react";


function ViewTitle() {

    const { state } = useLocation();
    console.log(state.query);
    return(
        <h1>{state.query}</h1>
    )

}

const root = document.getElementById("title");
reactDom.render(<BrowserRouter><ViewTitle /></BrowserRouter>, root)