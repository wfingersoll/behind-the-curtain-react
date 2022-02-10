import React from "react";
import reactDom from "react-dom";

const Index = () => {
    const [count, setCount] = React.useState(0)
    const onClick = () => setCount(c => c + 1)
    return (    
    <div>
        <h1>The count is {count}</h1>
        <button onClick={onClick}>Count</button>
    </div>
    )
}

const root = document.getElementById("index")
reactDom.render(<Index />, root)