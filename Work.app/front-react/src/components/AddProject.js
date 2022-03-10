import React, { useRef, useState } from "react"
import axios from 'axios';


export const AddProject = (props) => {
    let today = new Date().toISOString().slice(0, 10)

    const [img, setImg] = useState(null)
    const [project_name, setProjectName] = useState('')
    const [client, setClient] = useState('')
    const [info, setInfo] = useState('')
    const [start, setStart] = useState(today)
    const [status, setStatus] = useState('open')
    const [cost, setCost] = useState(0)
    const [errors, setErrors] = useState([])
    const imgRef = useRef()
    
    const setAddProjectOff = () => {
        props.add_project(false)
    }
    const setLogin = () => {
        props.set_login(true)
    }
    const newProject = (data) => {
        props.new_project(data)
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
        if (img) {
            formData.append('image', img)
        }

        axios.post(`http://127.0.0.1:8000/api/projects`, formData, config )
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
            newProject(new_project)
            setAddProjectOff()

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
    return (
        <div className="blur" onClick={(event)=>{
            if(event.target === event.currentTarget){
                setAddProjectOff()
            }
        }
        }>
            <div className="add_project">
                <div className="title">Add new project</div>
                {img &&
                <div className="img_prev">
                    <img src={URL.createObjectURL(imgRef.current.files[0])}></img>
                </div>
                }
                <form onSubmit={handleSubmit} encType="multipart/form-data" name="add_project">
                    <input
                        type="file"
                        alt=""
                        onChange={() => setImg(imgRef.current.files[0])}
                        id="img_add"
                        ref={imgRef}/>
                    <div className="project_client_add">
                        <div style={{width: '100%'}}>
                            <input
                                style={{width: '100%'}}
                                type="text"
                                placeholder="Project"
                                id="project_add"
                                onChange={(e) => setProjectName(e.target.value)}
                                maxLength="40"/>
                            {errors && <div className="error">{errors['name']}</div>}
                        </div>
                        <div style={{width: '100%'}}>
                            <select
                                style={{width: '100%'}}
                                name="clients"
                                onChange={(e) => setClient(e.target.value)}
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
                        placeholder="Info"
                        onChange={(e) => setInfo(e.target.value)}
                        maxLength="200"></textarea>
                    <div className="bottom_inputs_add">
                        <div className="start_status_cost_add">
                            <label htmlFor="name">start</label>
                            <input
                                type="date"
                                name="date_add"
                                defaultValue={today}
                                onChange={(e) => setStart(e.target.value)}
                                id="date_add"/>
                            <label htmlFor="status_add">status</label>
                            {errors && <div>{errors['start']}</div>}
                            <select
                                id="status_list"
                                name="status_add"
                                onChange={(e) => setStatus(e.target.value)}>
                                <option value="open">Open</option>
                                <option value="sent">Sent</option>
                                <option value="closed">Closed</option>
                            </select>
                            {errors && <div>{errors['status']}</div>}
                            <label htmlFor="cost_add">cost</label>
                            <input
                                type="text"
                                defaultValue={cost}
                                name="cost_add"
                                onChange={(e) => setCost(e.target.value)}
                                id="cost_add"
                                maxLength="5"/>
                        </div>
                        <button className="btn" type="submit" id="submit_add_project">add</button>
                    </div>
                </form>
            </div>
        </div>
    )
}