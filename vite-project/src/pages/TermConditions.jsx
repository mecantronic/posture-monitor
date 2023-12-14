import React from 'react';

export const TermConditions = () => {
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
        <link rel="stylesheet" href={process.env.PUBLIC_URL + '/css/term.css'} />
        {/* Favicon */}
        <link rel="icon" href={process.env.PUBLIC_URL + '/assets/favicon.ico'} />
        {/* Script */}
        <script src={process.env.PUBLIC_URL + '/js/script.js'} defer></script>
      </head>

      <body className="container">
        <main className="main-container">
          <div className="logo-icon">
            <img src={process.env.PUBLIC_URL + '/assets/Logo Caviar Black (1).png'} width="165px" height="75px" alt="Logo" />
          </div>
          <div>
            <h1>Term and Conditions</h1>
            <p>
              The Vitaance Pose does not store images or sound files on our servers. We guarantee data privacy and security, as the processing is done temporarily and locally on your device.
            </p>
            <form method="get" action="/choose_activity">
              <button className="term-conditions-button">I agree</button>
            </form>
          </div>
        </main>
      </body>
    </html>
  );
};