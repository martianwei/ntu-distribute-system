import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useInfo } from '../containers/hooks/useInfo';
import { useState, useEffect } from 'react';

const Show = () => {
    const navigate = useNavigate();

    const [movies, setMovies] = useState([]);
    const { getAllMovies } = useInfo();

    const click = (src) => {
        navigate(`/${src}`)
    }

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
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
            <div style={{width: '80%', display: 'flex', flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'center', alignItems: 'center'}}>
                {movies.map((ele, i) => (
                    <div style={{ width: 280, height: 365, display: 'flex', justifyContent: 'center', alignItems: 'center' }} key={i}>
                        <img src={ele.picture_url} alt="" style={{ width: 260, height: 345, cursor: 'pointer' }} onClick={() => {click(ele.id)}}/>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default Show;