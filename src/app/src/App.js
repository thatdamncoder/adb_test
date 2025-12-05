import './App.css';
import React, { useState, useEffect } from 'react';

const API_URL = 'http://localhost:8000/todos';

export function App() {
  const [todos, setTodos] = useState([]);
  const [newTodoDescription, setNewTodoDescription] = useState('');

  const fetchTodos = async () => {
    try {
      const response = await fetch(API_URL);
      const data = await response.json();
      console.log("data from GET", data);
      setTodos(data);

    } 
    catch (error) {
      console.error('Failed to fetch todos:', error);
    }
  };

  useEffect(() => {
    fetchTodos();
  }, []); 

  const handleFormSubmit = async (e) => {
    e.preventDefault(); 

    if (!newTodoDescription.trim()) {
      alert('Please enter a description.');
      return;
    }

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ description: newTodoDescription }),
      });

      if (response.status === 201) {
        console.log('Todo created successfully!');
        
        setNewTodoDescription('');
        fetchTodos();
      } 
      else {
        const error = await response.json();
        console.error('Failed to create todo: ', error);
        alert(`Error creating todo: ${error.error}`);
      }
    } 
    catch (error) {
      console.error('Unexpected error during POST:', error);
      alert('Unexpected error, check console');
    }
  };

  return (
    <div className="App container">
      
      {/* List Section */}
      <h1 className="mainTitle">List of TODOs ({todos.length})</h1>
      
      <div className="todoList">
        {todos.map(todo => (
          <div key={todo._id.$oid} className="todoItem">
            <span className="todoText">{todo.description}</span>
          </div>
        ))}
      </div>
      
      {/* Input Section */}
      <h2 className="sectionTitle">Create a ToDo</h2>
    
      <form onSubmit={handleFormSubmit} className="inputContainer"> 
        <div>
          <label htmlFor="todo" className="inputLabel">ToDo:</label>
        </div>
        <div>
          <input 
            type="text" 
            id="todo"
            className="input"
            placeholder=""
            value={newTodoDescription}
            onChange={(e) => setNewTodoDescription(e.target.value)} 
          />
        </div>
        <div style={{ "marginTop": "5px" }}>
          <button type="submit" className="addBtn">
            Add ToDo!
          </button>
        </div>
      </form>
      
    </div>
  );
}

export default App;