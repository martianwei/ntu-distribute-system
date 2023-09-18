import { createContext, useContext, useState, useEffect } from "react";
import axios from "axios"
import { gapi } from 'gapi-script';

const CLIENT_ID = process.env.REACT_APP_CLIENT_ID

const instance = axios.create({ baseURL: process.env.REACT_APP_API_ENDPOINT })

const InfoContext = createContext({
    logged_in: false,
    user_id: undefined,
    bookSeat: () => {},
    getIntro: () => {},
    getTime: () => {},
    getAllMovies: () => {},
    getReservers: () => {},
    getSeat: () => {},
    onSuccess: () => {},
    onFailure: () => {},
    onLogoutSuccess: () => {},
})

const useInfo = () => useContext(InfoContext)

const InfoProvider = (props) => {
    const [logged_in, set_logged_in] = useState(false)
    const [user_id, setUser_id] = useState(undefined)

    useEffect(() => {
        const start = () => {
            gapi.client.init({
                clientId: CLIENT_ID,
                scope: ""
            })
        };

        gapi.load('client:auth2', start)
    })

    const bookSeat = async(books) => {
        try{
            const { data: {msg} } = await instance.post('/reservation', {...books})
            return msg
        }catch(err){
            return "訂票失敗！！"
        }
    }

    const getReservers = async(user_id) => {
        try{
            const { data: {reservations} } = await instance.get('/user/reservations', {params: {user_id}});
            console.log(reservations)
            let length = reservations.length
            let bookData = []
            for (let i = 0; i < length; i++){
                let booking = { seats: [...reservations[i].seats], title: reservations[i].showtime.movie.title, movie_start_time: reservations[i].showtime.movie_start_time, cinema_id: reservations[i].showtime.cinema_id }
                bookData.push({...booking})
            }
            console.log(bookData)
            return bookData
        }catch(err){
            return {}
        }
    }

    const getAllMovies = async() => {
        try{
            const { data: { movies } } = await instance.get("/movie/all")
            return movies;
        }catch(err){
            console.error(err);
            // throw new Error("無法獲取電影資料");
        }
    }

    const getIntro = async(id) => {
        try{
            const { data: {movie} } = await instance.get(`/movie/${id}`)
            return movie;
        }catch(err){
            console.error(err);
            throw new Error("無法獲取該部電影資料");
        }
    }

    const getTime = async(id) => {
        try{
            const { data: {showtimes} } = await instance.get(`/showtime`, {params: {movie_id: id}})
            return showtimes;
        }catch(err){
            console.error(err);
            throw new Error("無法獲取該部電影時間資訊");
        }
    }

    const getSeat = async(id) => {
        try{
            const { data: {seats} } = await instance.get(`/seat`, {params: {showtime_id: id}})
            return seats;
        }catch(err){
            console.error(err);
            throw new Error("無法獲取該部電影時間資訊");
        }
    }

    const onFailure = res => {
        console.log("LOGIN FAILED! res: ", res)
    }

    const onLogoutSuccess = () => {
        console.log("LOGOUT SUCCESS!")
        setUser_id(undefined)
        set_logged_in(false)
    }

    const onSuccess = async res => {
        console.log("LOGIN SUCCESS! Current user: ", res.profileObj)
        let data = await fetch(`${process.env.REACT_APP_API_ENDPOINT}/user?username=${res.profileObj.googleId}`)
        let { user_id } = await data.json()
        
        if (user_id === "None") {
            data = await fetch(`${process.env.REACT_APP_API_ENDPOINT}/user`, {
                method: 'POST',
                // mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Methods': '*'
                },
                body: JSON.stringify({
                    'username': res.profileObj.googleId.toString(),
                    'email': res.profileObj.email.toString(),
                }),
                cache: 'default'
            })
            const { message } = await data.json()
            console.log(message)

            let new_data = await fetch(`${process.env.REACT_APP_API_ENDPOINT}/user?username=${res.profileObj.googleId}`);
            let { user_id } = await new_data.json()
            setUser_id(user_id)
            set_logged_in(true)
        }
        else{
            setUser_id(user_id)
            set_logged_in(true)
        }
    }

    return (
        <InfoContext.Provider
            value={{
                logged_in,
                user_id,
                bookSeat,
                getIntro,
                getTime,
                getAllMovies,
                getReservers,
                getSeat,
                onFailure,
                onLogoutSuccess,
                onSuccess,
            }}
            {...props}
        />
    );
}

export { InfoProvider, useInfo }