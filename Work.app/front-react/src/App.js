import React, { useEffect, useState } from 'react';
import './App.css';
import { Login } from './components/Login';

import axios from 'axios';
import { AddProject } from './components/AddProject';
import { ShowProject } from './components/ShowProject';
import { EditProject } from './components/EditProject';

function App() {
  const [projects, setProjects] = useState([]);
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [login, setLogin] = useState(false);
  const [error, setError] = useState(null);
  const [projectId, setProjectId] = useState(null);

  const [addProject, setAddProject] = useState(false);
  const [showProject, setShowProject] = useState(false);
  const [editProject, setEditProject] = useState(false);

  const [searchTermProject, setSearchTermProject] = useState("");
  const [searchResults, setSearchResults] = useState(projects);
  const [searchTermClient, setSearchTermClient] = useState("");

  // Search project
  useEffect(() => {
    const results = projects.filter(project =>
      project['name'].toLowerCase().includes(searchTermProject) &&
      project['client'].toLowerCase().includes(searchTermClient)
    );
    setSearchResults(results);
  }, [searchTermProject, searchTermClient, projects])
  
  const handleSearchProject = e => {
    setSearchTermProject(e.target.value);
  };

  const handleSearchClient = e => {
    setSearchTermClient(e.target.value);
  };

  useEffect(()=>{
    
    const token = localStorage.getItem("token")
    const config = {
      headers: { Authorization: `Bearer ${token}` }
    };
    axios.get(`http://127.0.0.1:8000/api/projects`, config)
      .then(res => {
        setProjects(res.data)
        setSearchResults(res.data)
        setLoading(false)
        setLogin(false)
        setError(false)
        
        axios.get(`http://127.0.0.1:8000/api/clients`, config)
        .then(res => {
          setClients(res.data)
        })

      })
      .catch((e)=>{
        if(e.response.data['message'] === 'Unauthenticated.'){
          setLoading(false)
          setError(true)
          setLogin(true)
        }
      })
  },[])

  
  function compare( a, b ) {
    if ( a['start'] < b['start'] ){
      return -1;
    }
    if ( a['start'] > b['start'] ){
      return 1;
    }
    return 0;
  }
  
  const handleNewProject = (data) => {
    projects.push(data)
    projects.sort(compare)
    setSearchResults(projects)
  }
  const handleUpdatedProject = (data) => {
    const newResults = projects.filter((proj) => proj['id'] !== data['id'])
    newResults.push(data)
    newResults.sort(compare)
    setProjects(newResults)
    setSearchResults(projects)
  }
  const handleDeleteProject = (id) => {
    const newResults = projects.filter((proj) => proj['id'] !== id)
    newResults.sort(compare)
    setProjects(newResults)
    setSearchResults(projects)
  }

  const handleShowProject = (id) => {
    setShowProject(true)
    setProjectId(id)
  }
  return (
    <div className="App">

      {login && <Login projects={setProjects} login={setLogin} error={setError}/>}
      {addProject && <AddProject clients={clients} add_project={setAddProject} new_project={handleNewProject} set_login={setLogin}/>}
      {showProject && <ShowProject id={projectId} show_project={setShowProject} edit_project={setEditProject} delete_project={handleDeleteProject} set_login={setLogin}/>}
      {editProject && <EditProject id={projectId} clients={clients} show_project={setShowProject} edit_project={setEditProject} new_project={handleUpdatedProject} set_login={setLogin}/>}
      
      <div className="add_btn" onClick={()=>setAddProject(true)}>+</div>
      <div className="nav">
        <div className="logo"><strong>work</strong><p>.app</p> </div>
      </div>
      <div className="projekty unselectable">
        <div className="info">
          <div className="id" onClick={()=>setAddProject(true)}>+</div>
          <div className="nazwa">
              <input
                type="text"
                placeholder="search..."
                value={searchTermProject}
                onChange={handleSearchProject}/>
          </div>
          <div className="firma">
              <input
                type="text"
                placeholder="client"
                value={searchTermClient}
                onChange={handleSearchClient}/>
          </div>
          <div className="data">date</div>
          <div className="cena">cost</div>
          <div className="status">status</div>
        </div>

        {/* Projekty */}
        <div className='projects'>
          {loading && <div className="api_status">Loading...</div>} 
          {error && <div className="api_status">You need to log in</div>} 
          {error !== true && loading === false && searchResults.length === 0 && <div>You have no projects</div>}
          {error !== true && loading === false &&
          
          searchResults.map((project) => (
            <div
              key={project['id']}
              className="projekt"
              onClick={()=>handleShowProject(project['id'])}>
              <div className="id pr_el" style={{color: 'var(--light_grey)'}}>{project['id']}</div>
              <div className="nazwa pr_el">{project['name']}</div>
              <div className="firma pr_el">{project['client']}</div>
              <div className="data pr_el">{project['start']}</div>
              <div className="cena pr_el">{project['cost']}</div>
              <div className="status pr_el">
                <div
                  className="status_box"
                  style={{backgroundColor: project['status'] === 'open' ?
                  'rgb(240, 240, 240)' :
                  project['status'] === 'sent' ?
                  'rgb(247, 255, 25)' :
                  'rgb(31, 224, 121)'}}
                  >
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
