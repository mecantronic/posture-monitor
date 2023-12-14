import React, { useState, useEffect } from 'react';
import '../components/css/login.css'

export const Login = () => {

    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
  
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('/'); // Reemplaza '/api' con tu URL correcta
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setMessage(data.message);
            } catch (error) {
                setError(error.message);
            }
        };

        fetchData();
    }, []);

    return (
        <html lang="en">
            <head>
                <meta charSet="UTF-8" />
                <meta httpEquiv="X-UA-Compatible" content="IE=edge" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <meta name="theme-color" content="#FFB81A" />

                {/* SEO Meta Tags */}
                <meta name="description" content="Vitaance Care landing page" />
                <meta name="author" content="Created by Mecantronic" />

                {/* OG Meta Tags */}
                <meta property="og:site_name" content="Vitaance Care" />
                <meta property="og:site" content="https://vitaance-pose.onrender.com" />
                <meta property="og:title" content="Vitaance Care" />
                <meta property="og:type" content="Landing Page" />

                {/* Website Title */}
                <title>Vitaance Care</title>

                {/* Styles */}
                <link rel="stylesheet" href={process.env.PUBLIC_URL + './components/css/login.css'} />

                {/* Favicon */}
                <link rel="icon" href={process.env.PUBLIC_URL + './assets/favicon.ico'} />

                {/* Script */}
                <script src={process.env.PUBLIC_URL + './js/script.js'} defer></script>
            </head>

            <body className="container">
                <nav>{/* Add your navigation content here */}</nav>
                <main className="main-container">
                    <h1>{message}</h1>
                    <section>
                        <img src={process.env.PUBLIC_URL + './assets/image4.png'} width="450px" height="140px" />
                        <div className="img-characters">
                            <img src={process.env.PUBLIC_URL + './assets/Mascots-10_msj.png'} width="200px" height="220px" />
                        </div>
                    </section>
                    <section className="login-section">
                        <h1 className="text">Login</h1>
                        <div>
                            <input type="text" name="username" id="username" placeholder="Username or email" className="login-input" />
                        </div>
                        <div>
                            <input type="password" name="password" id="password" placeholder="Password" className="login-input" />
                        </div>
                        <form method="get" action="/term_conditions">
                            <button className="login-button text">Log In</button>
                        </form>
                    </section>
                    <div className="img-characters-2" style={{ display: 'none' }}>
                        <img src={process.env.PUBLIC_URL + './assets/Mascots-19.png'} width="110px" height="120px" />
                        <img src={process.env.PUBLIC_URL + './assets/Mascots-01.png'} width="100px" height="120px" />
                        <img src={process.env.PUBLIC_URL + './assets/Mascots-10.png'} width="100px" height="120px" />
                        <img src={process.env.PUBLIC_URL + './assets/image3.png'} width="100px" height="120px" />
                    </div>
                </main>
            </body>
        </html>
    );
};