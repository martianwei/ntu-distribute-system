import Show from './components/Home';
import Navbar from './components/Navbar';
import SignIn from './components/Login';
import SignUp from './components/SignUp';
import Information from './components/Information';
import Seat from './containers/Seat';
import React from 'react';
import Time from './containers/Time'
import styled from 'styled-components';
import User from './containers/UserInfo'
import { useNavigate } from 'react-router-dom';
import './App.css';
import { useState, useEffect } from 'react';
import { Routes, Route, Outlet } from "react-router-dom";
import { useInfo } from './containers/hooks/useInfo';

const CustomButton = styled.button`
      background-color: #5E5E5E;
      color: white;
      margin: 0 10px;
      padding: 10px 20px;
      border-radius: 20px;
      height: 50px;
      font-size: 20px;
      border: none;
      outline: none;
      cursor: pointer;
      &:hover {
        background-color: white;
        color: #5E5E5E;
      }
`;

function App() {
  const Root = () => {
    const navigate = useNavigate()

    return (
        <div>
            <div style={{ display: 'flex', flexDirection:'row', alignItems: 'center', height: 70, backgroundColor: "#5E5E5E" }}>
                <CustomButton onClick={() => {navigate(".")}}>電影介紹</CustomButton>
                <CustomButton onClick={() => {navigate("./time")}}>電影時刻</CustomButton>
            </div>
            <Outlet />
        </div>
    );
  };

  const [movies, setMovies] = useState([])
  const { getAllMovies } = useInfo()

  useEffect(() => {
    const fetchMovies = async () => {
        try {
            const allMovies = await getAllMovies();
            setMovies(allMovies);
        } catch (err) {
            console.error(err);
            throw new Error("無法獲取電影資料");
        }
    }
    fetchMovies();
}, []);

  return (
    <>
      <Navbar />
      <Routes>
          <Route path="/" element={<Show />} />
          { movies.map((ele, i) => (
            <Route key={4*i} path={`/${ele.id}/*`} element={<Root />}>
              <Route key={4*i+1} index element={<Information />} />
              <Route key={4*i+2} path="time" element={<Time />} />
              <Route key={4*i+3} path={"book/:num/:num"} element={<Seat />} />
            </Route>
          ))}
          <Route path="/LogIn" element={<SignIn />} />
          <Route path="/SignUp" element={<SignUp />} />
          <Route path="/users/reservation" element={<User />} />
      </Routes>
    </>
  );
}

export default App;
