import React, { useRef, useState, useEffect, useCallback } from "react"
import axios from 'axios';


export const EditProject = (props) => {
    const [id, setId] = useState('')
    const [img, setImg] = useState(null)
    const [project_name, setProjectName] = useState('')
    const [client, setClient] = useState('')
    const [info, setInfo] = useState('')
    const [start, setStart] = useState('')
    const [status, setStatus] = useState('')
    const [cost, setCost] = useState('')
    const [errors, setErrors] = useState([])
    const imgRef = useRef()
    const [newImg, setNewImg] = useState(false)
    const [changes, setChanges] = useState(false)
    
    const setLogin = useCallback(() => {
        props.set_login(true)
    }, [props])

    useEffect(()=>{
        const token = localStorage.getItem("token")
        const config = {
            headers: {
                Authorization: `Bearer ${token}`
            }
        };
        axios.get(`http://127.0.0.1:8000/api/projects/${props.id}`, config)
        .then(res => {
            setImg(res.data['image'])
            setProjectName(res.data['name'])
            setClient(res.data['client'])
            if(res.data['info'] === null){
                setInfo('')
            }else{
                setInfo(res.data['info'])
            }
            setStart(res.data['start'])
            setStatus(res.data['status'])
            setCost(res.data['cost'])
            setId(res.data['id'])
        })
        .catch((e)=>{
            if(e.response.data['message'] === 'Unauthenticated.'){
                console.log('Unauthenticated')
                setLogin(true)
            }
        })
    },[props.id, setLogin])
    const newProject = (data) => {
        props.new_project(data)
    }
    const setEditProjectOff = () => {
        props.edit_project(false)
    }
    
    const handleSubmit = (e) => {
        e.preventDefault()
        const token = localStorage.getItem('token')
        const config = {
            headers: {
                "Accept": "application/json",
                "Authorization": `Bearer ${token}`,
            },
        };
            
        const formData = new FormData();
        formData.append('name', project_name)
        formData.append('client', client)
        formData.append('info', info)
        formData.append('start', start)
        formData.append('status', status)
        formData.append('cost', cost)
        if (img && newImg) {
            formData.append('image', img)
        }

        axios.post(`http://127.0.0.1:8000/api/projects/${id}?_method=PUT`, formData, config )
        .then(res => {
            const new_project = {
                'id': res.data['id'],
                'image': img,
                'name': project_name,
                'client': client,
                'info': info,
                'start': start,
                'status': status,
                'cost': cost,
            }
            setEditProjectOff()
            newProject(new_project)

        }).catch((e)=>{
            if(e.response.status === 422){
                setErrors(e.response.data.errors)
                console.log(e.response.data.errors)
            }else if(e.response.status === 401){
                setLogin()
            }else{
                console.log(e.response)
            }
        })
    }

    const handleSetImg = () => {
        setNewImg(true)
        setImg(imgRef.current.files[0])
    }
    const handleDelImg = () => {
        setNewImg(false)
        setImg('')
        setChanges(true)
        const token = localStorage.getItem('token')
        const config = {
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type" : "application/json",
                "Accept": "application/json",
            }
        }

        axios.post(`http://127.0.0.1:8000/api/projects/${props.id}/imgdel?_method=PUT`, {}, config)
        .then(res => {
            console.log(res.data)
        })
        .catch((e)=>{
            console.log(e.response)
        })
    }
    return (
        <div className="blur" onClick={(event)=>{
            if(event.target === event.currentTarget){
                setEditProjectOff()
            }
        }
        }>

            <div className="add_project">
                <div className="title">Edit project</div>
                <div className="img_prev">
                    <img
                        src={
                            newImg ? URL.createObjectURL(imgRef.current.files[0]) :
                            img ? `http://127.0.0.1:8000/storage/images/${img}` : `http://127.0.0.1:8000/storage/images/no_image.png`
                        }></img>
                    {img && <div className="imgDel" onClick={handleDelImg}></div>}
                </div>
                <form onSubmit={handleSubmit} encType="multipart/form-data" name="add_project">
                    <input
                        type="file"
                        alt=""
                        onChange={() => {
                            handleSetImg()
                            setChanges(true)
                        }}
                        id="img_add"
                        ref={imgRef}/>
                    <div className="project_client_add">
                        <div style={{width: '100%'}}>
                            <input
                                style={{width: '100%'}}
                                type="text"
                                value={project_name}
                                id="project_add"
                                onChange={(e) => {
                                    setProjectName(e.target.value)
                                    setChanges(true)
                                }}
                                maxLength="40"/>
                            {errors && <div className="error">{errors['name']}</div>}
                        </div>
                        <div style={{width: '100%'}}>
                            <select
                                style={{width: '100%'}}
                                value={client}
                                name="clients"
                                onChange={(e) => {
                                    setClient(e.target.value)
                                    setChanges(true)
                                }}
                                id="clients_list_add">
                                <option value="" hidden>Select Client</option>
                                {props.clients.map((client) => (
                                    <option key={client['id']} value={client['name']}>{client['name']}</option>
                                ))}
                            </select>
                            {errors && <div className="error">{errors['client']}</div>}
                        </div>
                    </div>
                    <textarea
                        id="info_add"
                        name="info_add"
                        value={info}
                        placeholder="Info"
                        onChange={(e) => {
                            setInfo(e.target.value)
                            setChanges(true)
                        }}
                        maxLength="200"></textarea>
                    <div className="bottom_inputs_add">
                        <div className="start_status_cost_add">
                            <label htmlFor="name">start</label>
                            <input
                                type="date"
                                name="date_add"
                                defaultValue={start}
                                onChange={(e) => {
                                    setStart(e.target.value)
                                    setChanges(true)
                                }}
                                id="date_add"/>
                            <label htmlFor="status_add">status</label>
                            {errors && <div>{errors['start']}</div>}
                            <select
                                id="status_list"
                                name="status_add"
                                value={status}
                                onChange={(e) => {
                                    setStatus(e.target.value)
                                    setChanges(true)
                                }}>
                                <option value="open">Open</option>
                                <option value="sent">Sent</option>
                                <option value="closed">Closed</option>
                            </select>
                            {errors && <div>{errors['status']}</div>}
                            <label htmlFor="cost_add">cost</label>
                            <input
                                type="text"
                                defaultValue={cost ? cost : ""}
                                name="cost_add"
                                onChange={(e) => {
                                    setCost(e.target.value)
                                    setChanges(true)
                                }}
                                id="cost_add"
                                maxLength="5"/>
                        </div>
                        <div
                            className="btn"
                            onClick={()=>{
                                props.edit_project(false)
                                props.show_project(true)
                            }}
                        >back</div>
                        <button disabled={!changes} className="btn" type="submit" id="submit_add_project">{changes ? 'update' : 'no changes'}</button>

                    </div>
                </form>
            </div>
        </div>
    )
}