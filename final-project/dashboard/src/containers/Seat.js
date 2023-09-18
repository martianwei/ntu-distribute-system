import React from "react";
import styled from 'styled-components';
import { useState, useEffect } from "react";
import { useInfo } from "./hooks/useInfo";
import { Button } from "@mui/material";
import { useTheme } from '@mui/material/styles';
import { useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";
import { Snackbar } from '@mui/material';

import Alert from '@material-ui/lab/Alert';

const getColor = (number) => {
    if (number === 0)
        return "#00BFFF"
    else if (number === 1)
        return "#FFFF2C"
    else if (number === 2)
        return "#EE2222"
}

const StyledButton = styled.button`
  background-color: ${props => getColor(props.number)};
  cursor: pointer;
  padding: 10px 10px;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  margin: 10px;
`;

const Unsee = styled.div`
    background-color: green
    cursor: pointer;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    margin: 5px;
`

const Seat = () => {
    const { logged_in, user_id, getSeat, bookSeat } = useInfo()
    

    const theme = useTheme();
    const location = useLocation();
    const navigate = useNavigate();
    const showtime_id = (location.pathname + location.search).split("/")[3];
    const cinema_id = (location.pathname + location.search).split("/")[4];
    const [occupied, setOccupied] = useState([])
    const [array, setArray] = useState([])
    const [open, setOpen] = useState(false);
    const [booked, setBooked] = useState(false)
    const [books, setBooks] = useState([])
    const [message, setMessage] = useState("")
    const [success, setSuccess] = useState(false)

    let len_of_occupied = occupied.length

    useEffect(() => {
        const fetchBooks = async () => {
            try {
                let occupy = await getSeat(showtime_id);
                setOccupied(occupy)
            } catch (err) {
                console.error(err);
                throw new Error("無法獲取電影資料");
            }
        }
        fetchBooks();
    }, [getSeat, showtime_id])

    useEffect(() => {
        const initialArray = [];
        for (let i = 0; i < 10; i++) {
          initialArray.push([]);
          for (let j = 0; j < 20; j++) {
            initialArray[i].push(0);
          }
        }
        for (let k = 0; k < len_of_occupied; k++) {
          let id = occupied[k].seat_number - 1;
          let i = Math.floor(id / 20);
          let j = id % 20;
          initialArray[i][j] = 2;
        }
        setArray(initialArray)
    }, [occupied, len_of_occupied])

    const handleOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
        if (booked){
            navigate('..')
        }
    };

    const sendBook = async(seat_numbers) => {
        if (seat_numbers.length === 0){
            setMessage("訂票不能為空！")
            handleOpen()
        }
        else if (!logged_in || !user_id){
            setMessage("登入後即可進行訂票操作！")
            handleOpen()
        }
        else{
            setBooked(true)
            try{
                await bookSeat({user_id, showtime_id, cinema_id, seat_numbers})
                setSuccess(true)
                setMessage("訂票處理中！")
                handleOpen()
            }catch(err) {
                setMessage("訂票失敗！！")
                handleOpen()
            }
        }
    }

    const clearSeat = () => {
        setBooks([])
        const updatedArray = [...array];
        for (let i = 0; i < 10; i++){
            for (let j = 0; j < 20; j++){
                if (updatedArray[i][j] === 1){
                    updatedArray[i][j] = 0
                }
            }
        }
        setArray(updatedArray)
    }

    const click = ( num, i, j ) => {
        const updatedArray = [...array];
        if (num === 0){
            setBooks([...books, i*20 + j + 1])
            updatedArray[i][j] = 1;
        }   
        else if (num === 1){
            setBooks(books.filter(book => book !== i*20 + j + 1))
            updatedArray[i][j] = 0;
        }
        setArray(updatedArray)
    }

    const Blank = ({ele, i, j, click }) => {
        return(
            <>
                <Unsee />
                <StyledButton number={ele} i={i} j={j} width={15} height={15} onClick={() => {click(ele, i, j)}}/>
            </>
        )
    }
    
    return(
        <>
            
            <Snackbar open={open} autoHideDuration={1500} onClose={handleClose} 
                anchorOrigin={{
                    vertical: 'top',
                    horizontal: 'center'
                }}>
                <Alert severity = {success ? "success" : "error"}>
                    {message}
                </Alert>
            </Snackbar>
            
            <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: 10, marginBottom: 10 }}>
                <StyledButton width={5} height={5} number={0}/>
                <div>未售出</div>
                <StyledButton width={5} height={5} number={1}/>
                <div>您的位置</div>
                <StyledButton width={5} height={5} number={2}/>
                <div>已售出</div>
            </div>
            <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <div>
                    {array.map((element, i) => (
                        (i % 10 === 4) ? 
                            <div key={"test"}>
                                <div key = {`blank-${i}`} style={{height: 45, display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems: 'center'}}>
                                        {element.map((ele, j) => 
                                            <Unsee key = {`${i}-${j}`}/>
                                        )}
                                    </div>
                                <div key = {i} style={{height: 45, display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems: 'center'}}>
                                    {element.map((ele, j) => 
                                        (j % 20 === 4 || j % 20 === 15) ? 
                                        <Blank key = {`blank-${i}-${j}`} ele={ele} i={i} j={j} click={click} />
                                        : <StyledButton key = {`square-${i}-${j}`} number={ele} i={i} j={j} width={15} height={15} onClick={() => {click(ele, i, j)}}/>
                                    )}
                                </div>
                            </div>
                            :
                            <div key = {i} style={{height: 45, display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems: 'center'}}>
                                {element.map((ele, j) => 
                                    (j % 20 === 4 || j % 20 === 15) ? 
                                    <Blank key = {`blank-${i}-${j}`} ele={ele} i={i} j={j} click={click}/>
                                    : <StyledButton key = {`square-${i}-${j}`} number={ele} i={i} j={j} width={15} height={15} onClick={() => {click(ele, i, j)}}/>
                                )}
                            </div>
                    ))}
                </div>
            </div>
            <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: 20 }}>
                <Button 
                    sx={{
                        backgroundColor: theme.palette.primary.main, 
                        color: "white",
                        marginRight: 10,
                        '&:hover': {
                            backgroundColor: theme.palette.primary.dark
                        }
                    }}
                    disabled={booked}
                    onClick={() => { clearSeat() }}
                >重設場次</Button>
                <Button 
                    sx={{
                        backgroundColor: theme.palette.primary.main, 
                        color: "white",
                        '&:hover': {
                            backgroundColor: theme.palette.primary.dark
                        }
                    }}
                    disabled={booked}
                    onClick={() => { sendBook(books); }}
                >送出訂單</Button>
            </div>
        </>
    )
}

export default Seat