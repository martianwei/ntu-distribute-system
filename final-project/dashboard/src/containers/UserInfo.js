import React from "react";
import { useState, useEffect } from "react";
import { useInfo } from "./hooks/useInfo";
import { styled } from '@mui/material/styles';
import Table from '@mui/material/Table';
import Chip from "@mui/material/Chip";
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import TablePagination from '@mui/material/TablePagination';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

const Text = ( number ) => {
    let i = number % 20 === 0 ? Math.floor(number / 20) : Math.floor(number / 20) + 1
    let j = number % 20 === 0 ? 20 : number % 20
    return i.toString() + "排" + j.toString() + "號"
}

const Time = ( date ) => {
    const datetime = new Date(date)
    const year = datetime.getUTCFullYear().toString();
    const month = (datetime.getUTCMonth() + 1).toString();
    const day = datetime.getUTCDate().toString();

    const hours = datetime.getUTCHours().toString();
    const minutes = datetime.getUTCMinutes().toString().padStart(2, '0');
    
    return year + "-" + month + "-" + day + " " + hours + ":" + minutes
}

const StyledTableCell = styled(TableCell)(({ theme }) => ({
    [`&.${tableCellClasses.head}`]: {
      backgroundColor: theme.palette.common.black,
      color: theme.palette.common.white,
    },
    [`&.${tableCellClasses.body}`]: {
      fontSize: 14,
    },
  }));
  
  const StyledTableRow = styled(TableRow)(({ theme }) => ({
    '&:nth-of-type(odd)': {
      backgroundColor: theme.palette.action.hover,
    },
    // hide last border
    '&:last-child td, &:last-child th': {
      border: 0,
    },
  }));

const User = () => {
    const { user_id, getReservers } = useInfo()
    const [reservations, setReservations] = useState([])

    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(5);
    
    const handleChangePage = (event, newPage) => {
        setPage(newPage);
        setTimeout(() => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }, 0);
    };
    
    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(+event.target.value);
        setPage(0);
        setTimeout(() => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }, 0);
    };

    useEffect(() => {
        const fetchReservations = async() => {
            if (!user_id){
                setReservations([])
            }
            else{
                let reserves = await getReservers(user_id);
                setReservations(reserves)
            }
        }
        fetchReservations();
        setPage(0);
    }, [getReservers, user_id])

    return (
        <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
            <h2>Your Reservations</h2>
            <TableContainer component={Paper} sx={{width: '70%'}}>
                <Table aria-label="customized table">
                    <TableHead>
                        <StyledTableRow>
                            <StyledTableCell>Movie Title</StyledTableCell>
                            <StyledTableCell align="center">Movie Start Time</StyledTableCell>
                            <StyledTableCell align="center">Movie Seats</StyledTableCell>
                            <StyledTableCell align="center">Cinema</StyledTableCell>
                        </StyledTableRow>
                    </TableHead>
                    <TableBody>
                        {   
                            reservations && reservations.length > 0 ?
                            reservations.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row, i) => (
                            <StyledTableRow
                            key={`row ${i}`}
                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                            >
                                <StyledTableCell component="th" scope="row">
                                    {row.title}
                                </StyledTableCell>
                                {/* <StyledTableCell align="right">{row.title}</StyledTableCell> */}
                                <StyledTableCell align="center">{Time(row.movie_start_time)}</StyledTableCell>
                                <StyledTableCell sx={{ display: 'flex', flexDirection: 'row', justifyContent: 'center' }}>{
                                    row.seats.map((ele, j) => (
                                        <Chip key={`${i}-${j}`} label={Text(ele.seat_number)} color="primary" sx={{margin: 1, boxShadow: '0 0 8px green', color: "white"}}/>
                                    ))}</StyledTableCell>
                                <StyledTableCell align="center">{row.cinema_id}</StyledTableCell>
                            </StyledTableRow>
                        )) : <></>}
                    </TableBody>
                </Table>
            </TableContainer>
            <TablePagination
                rowsPerPageOptions={[5, 10]}
                component="div"
                count={reservations.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
            />
        </div>   
    );
}

export default User
