import {BrowserRouter, Route, Routes} from 'react-router-dom'
import { FC } from 'react'
import Login from "./pages/Login"
import SignUp from './pages/SIgnUp'


const Router:FC = () => {
    return <BrowserRouter>
        <Routes>
        <Route path="/login" element = {<Login />} />
        <Route path="/verify" element = {<SignUp />} />
        </Routes>
    </BrowserRouter>
}

export default Router 