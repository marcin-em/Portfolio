import React, { useEffect, useState, useCallback } from "react"
import axios from 'axios';


export const ShowProject = (props) => {

    const [id, setId] = useState(null)
    const [img, setImg] = useState('no_image.png')
    const [project_name, setProjectName] = useState('')
    const [client, setClient] = useState('')
    const [info, setInfo] = useState('')
    const [start, setStart] = useState('')
    const [status, setStatus] = useState('')
    const [cost, setCost] = useState('')

    const setLogin = useCallback(() => {
        props.set_login(true)
    }, [props])
    useEffect(()=>{
        const token = localStorage.getItem('token')
        const config = {
            headers: {
                "Accept": "application/json",
                "Authorization": `Bearer ${token}`,
            },
        };
        axios.get(`http://127.0.0.1:8000/api/projects/${props.id}`, config)
            .then(res => {

                if(res.data['image']){
                    setImg(res.data['image'])
                }
                setId(res.data['id'])
                setProjectName(res.data['name'])
                setClient(res.data['client'])
                setInfo(res.data['info'])
                setStart(res.data['start'])
                setStatus(res.data['status'])
                setCost(res.data['cost'])
            })
            .catch((e)=>{
                if(e.response.data['message'] === 'Unauthenticated.'){
                    setLogin()
                    console.log('Unauthenticated')
                }
            })
    },[props.id, setLogin])

    const setShowProjectOff = () => {
        props.show_project(false)
    }
    const setEditProjectOn = () => {
        props.show_project(false)
        props.edit_project(true)
    }
    
    const handleDelete = (id) => {
        
        const token = localStorage.getItem('token')
        const config = {
            headers: {
                "Accept": "application/json",
                "Authorization": `Bearer ${token}`,
            },
        };
        axios.delete(`http://127.0.0.1:8000/api/projects/${id}`, config)
        .then(() => {
            props.show_project(false)
            props.delete_project(id)
        })
        .catch((e)=>{
            if(e.response.data['message'] === 'Unauthenticated.'){
                setLogin()
                console.log('Unauthenticated')
            }
        })
    }
    
    return (
        <div className="blur" onClick={(event)=>{
            if(event.target === event.currentTarget){
                setShowProjectOff()
            }
        }
        }>
            <div className="view_project">
                <div className="title_wrap">
                    <div className="title">{project_name}<small>{id}</small></div>
                    <div className="title_client">{client}</div>
                </div>
                <div className="project_info">
                    <div className="img_prev">
                        {img && <img src={`http://127.0.0.1:8000/storage/images/${img}`}></img>}
                    </div>
                    <div className="info_view">{info}</div>
                    <div className="bottom_inputs_add">
                        <div className="start_status_cost_add">
                            <div className="date_view">
                                <div className="date1">start</div>
                                <div className="date2">{start}</div>
                            </div>
                            <div className="status_view">
                                <div className="status1">status</div>
                                <div className="status2">{status}</div>
                            </div>
                            <div className="cost_view">
                                <div className="cost1">cost</div>
                                <div className="cost2">{cost}</div>
                            </div>
                        </div>
                        <div className="edit_delete_btns">
                            <div className="btn" onClick={setEditProjectOn} id="edit_btn">change</div>
                            <div className="btn" onClick={()=>handleDelete(id)} id="delete_btn"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}