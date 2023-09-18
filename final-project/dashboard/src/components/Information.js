import React from "react";
import { useInfo } from "../containers/hooks/useInfo";
import { useState, useEffect } from "react";
import { useLocation } from 'react-router-dom';

const Information = () => {
    const { getIntro } = useInfo()
    const location = useLocation();
    const movie = (location.pathname + location.search).slice(1);

    const [info, setInfo] = useState({title: "", picture_url: "", description: ""})

    useEffect(() => {
        const fetchMovie = async () => {
            try {
                const movie_info = await getIntro(movie);
                setInfo(movie_info);
            } catch (err) {
                console.error(err);
                throw new Error("無法獲取電影資料");
            }
        }
        fetchMovie();
    }, [getIntro, movie])

    
    return (
        <>
            <div style={{display: 'flex', justifyContent: 'space-around'}}>
                <h2>{info.title}</h2>
            </div>
            <div style={{display: 'flex', justifyContent: 'space-around', alignContent: 'center'}}>
                <div style={{width: '80%', display: 'flex', justifyContent: 'center', alignContent: 'center'}}>
                    <img src={info.picture_url} alt="pic" style={{width: 360, height: 480}}></img>
                    <div style={{height: 480, width: '90%', display: 'flex', flexDirection: 'column', alignItems: 'center', marginLeft: 100, backgroundColor: "#E6E6FA", borderRadius: 30, boxShadow: '0 0 1em black',}}>
                        <div style={{ display: 'flex', justifyContent: 'flex-start', alignItems: 'center', width: '95%' }}>
                            <h3>電影簡介:</h3>
                        </div>
                        <div style={{ overflow: 'auto', display: 'flex', width: '90%' }}>{info.description}</div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Information