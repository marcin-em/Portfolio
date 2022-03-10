import React, { useState } from "react"
import axios from 'axios';


export const Login = (props) => {

    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)

    const setLoginOff = () => {
        props.login(false)
    }
    const setErrorOff = () => {
        props.error(false)
    }
    const setProjects = (data) => {
        props.projects(data)
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        setLoading(true)
        axios.post(`http://127.0.0.1:8000/api/login`,  {
              'name': username,
              'password': password
          })
          .then(res => {
            setLoading(false)
            localStorage.setItem("token", res.data.token)
            setLoginOff()
            setErrorOff()
            const config = {
                headers: { Authorization: `Bearer ${res.data.token}` }
              };
            axios.get(`http://127.0.0.1:8000/api/projects`, config)
                .then(res => {
                    setProjects(res.data)
                })
          })
          .catch((e)=>{
            setError(e.response.data)
            setLoading(false)
          })
    }
    return (
        <div className="blur blur-login">
            <div className="login">
                <div className="title">Login</div>
                <form onSubmit={handleSubmit} name="login">
                    <input
                        type="text"
                        placeholder="Username"
                        id="username"
                        onChange={(e) => setUsername(e.target.value)}/>
                    <input
                        type="password"
                        placeholder="Password"
                        id="password"
                        onChange={(e) => setPassword(e.target.value)}/>
                    {loading
                    ?
                    <button className="btn" type="submit" id="submit_login" disabled>logging...</button>
                    :
                    <button className="btn" type="submit" id="submit_login">login</button>
                    }
                </form>
                {error && <div>{error['message']}</div>}
            </div>
        </div>
    )
}