import React, { useState } from 'react'
import { NavLink } from 'react-router-dom'
import "./css/NavBar.css";

function Navbar() {
    return (
        <nav className="nav">
            <NavLink to='/' style={{ textDecoration: 'none' }}>
                <div className="site-title" >
                    BSN
                </div>
            </NavLink>
            <div className="other-pages">
                <ul>
                    <li>
                        <NavLink to='/communities' style={{ textDecoration: 'none' }}>
                            <div className="link-title">
                                Communities
                            </div>
                        </NavLink>
                    </li>
                    <li>
                        <NavLink to='/posts' style={{ textDecoration: 'none' }}>
                            <div className="link-title">
                                Posts
                            </div>
                        </NavLink>
                    </li>
                    <li>
                        <NavLink to='/create' style={{ textDecoration: 'none' }}>
                            <div className="link-title">
                                Create
                            </div>
                        </NavLink>
                    </li>
                </ul>
            </div>
        </nav>
    )
}

export default Navbar