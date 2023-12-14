import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Login } from "./pages/Login";
import { TermConditions } from "./pages/TermConditions";


function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />}></Route>
        <Route path="/term_conditions" element={<TermConditions />}></Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App;
