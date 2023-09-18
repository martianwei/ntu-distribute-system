import React from "react";
import { useState, useEffect } from "react";
import { useInfo } from "./hooks/useInfo";
import { useNavigate } from "react-router-dom";
import Button from '@mui/material/Button';
import List from '@mui/material/List';
import ListItemText from '@mui/material/ListItemText';
import { styled } from '@mui/system';
import { useLocation } from 'react-router-dom';

const CircleButton = styled(Button)`
  width: 80px;
  height: 80px;
  font-size: 24px;
  margin: 0 25px 0 25px;
  border-radius: 50%;
  border: 2px solid ${({ theme }) => theme.palette.primary};
`;

const get_dict_time = (alltimes) => {
    const length = alltimes.length
    let dict_of_time = {}
    for (let i = 0; i < length; i++){
        let month = new Date(alltimes[i].movie_start_time).getUTCMonth() + 1;
        let day = new Date(alltimes[i].movie_start_time).getUTCDate();
        let key = month.toString() + "/" + day.toString()
        if (dict_of_time.hasOwnProperty(key)){
            dict_of_time[key].push(alltimes[i])
        }
        else{
            dict_of_time[key] = [alltimes[i]]
        }
    }
    return dict_of_time
}

const get_first_day = (alltimes) => {
    if (alltimes.length > 0){
        const month = new Date(alltimes[0].movie_start_time).getUTCMonth() + 1;
        const day = new Date(alltimes[0].movie_start_time).getUTCDate();
        return month + "/" + day
    }
    return ""
}

const get_text = (element) => {
    if (element.movie_start_time){
        const time = new Date(element.movie_start_time);
        const hour = time.getUTCHours().toString()
        const minute = time.getUTCMinutes().toString().padStart(2, '0');
        return hour + ":" + minute
    }
    return ""
}

const Time = () => {
    const { getTime } = useInfo()

    const location = useLocation();
    
    const movie = (location.pathname + location.search).split("/")[1];

    const [dict_of_time, setDict] = useState({})
    const [movie_showtimes, setShowtimes] = useState([])
    const [day, setDay] = useState([])
    const [dates, setDates] = useState([])
    const [times, setTimes] = useState([])

    useEffect(() => {
        const fetchShowtimes = async () => {
            try {
                let showtimes = await getTime(movie);
                showtimes = showtimes.length > 0 ? showtimes.sort((a, b) => a.movie_start_time - b.movie_start_time) : []
                setShowtimes(showtimes)
            } catch (err) {
                console.error(err);
                throw new Error("無法獲取電影資料");
            }
        }
        fetchShowtimes();
    }, [getTime, movie])

    useEffect(() => {
        let dict_of_time = get_dict_time(movie_showtimes)
        setDay(get_first_day(movie_showtimes));
        setDict(dict_of_time)
        setTimes(dict_of_time[get_first_day(movie_showtimes)])
        setDates(Object.keys(dict_of_time))
    }, [movie_showtimes])
    
    const navigate = useNavigate()

    return (
        <>
            <div style={{display: 'flex', marginTop: '2%'}}>
                {dates.map((ele, i) => (
                    <CircleButton key={i} variant = {ele === day ? "contained" : "outlined"} onClick={() => {setDay(ele); setTimes(dict_of_time[ele]);}}>{ele}</CircleButton>
                ))}
            </div>
            <List sx={{ marginTop: 3 }}>
                {
                    times ? times.map((ele, i) => (
                        <div key={i} style={{ backgroundColor: "#F0F0F0" }}>
                            <div style={{ display: 'flex', height: 60, justifyContent: 'space-around', alignItems: 'center' }}>
                                <ListItemText primary={get_text(ele)} primaryTypographyProps={{ style: { fontSize: '20px', marginLeft: '20px' } }}/>
                                <Button onClick={() => navigate(`../book/${ele.id}/${ele.cinema_id}`)} sx={{ fontSize: 20, marginRight: 5}}>去訂票</Button>
                            </div>
                        </div>)) 
                        : 
                        <div>Not Found!</div>
                }
            </List>
        </>
    )
}

export default Time