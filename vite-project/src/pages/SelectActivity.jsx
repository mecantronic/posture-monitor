import React from 'react';

export const ChooseActivity = () => {
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
        <link rel="stylesheet" href={process.env.PUBLIC_URL + '/css/activity.css'} />
        {/* Favicon */}
        <link rel="icon" href={process.env.PUBLIC_URL + '/assets/favicon.ico'} />
        {/* Script */}
        <script src={process.env.PUBLIC_URL + '/js/script.js'} defer></script>
      </head>

      <body className="container">
        <nav>
          <img src={process.env.PUBLIC_URL + '/assets/Logo Caviar Black (1).png'} width="110px" height="55px" alt="Logo" />
          <p className="username">Sofia Medina</p>
        </nav>
        <main className="main-container">
          <div className="main-title">
            <h1 className="text">Choose activity</h1>
          </div>
          <div className="activity-container">
            <div>
              <div className="section-activity">
                <h3 className="center-text">Decant</h3>
                <img src={process.env.PUBLIC_URL + '/assets/WhatsApp Image 2023-11-29 at 09.29.26.jpeg'} width="250px" height="200px" className="bg-activity-image" id="img-activity-1" alt="Decant Activity" />
              </div>
              <div className="section-activity">
                <h3 className="center-text">Stow</h3>
                <img src={process.env.PUBLIC_URL + '/assets/warehouse-forklift-driver-thinking-something-while-going-through-delivery-schedule-industrial-building.jpg'} width="250px" height="200px" className="bg-activity-image" id="img-activity-2" alt="Stow Activity" />
              </div>
            </div>
            <div>
              <div className="section-activity">
                <h3 className="center-text">Pick</h3>
                <img src={process.env.PUBLIC_URL + '/assets/pexels-elevate-1267338.jpg'} width="250px" height="200px" className="bg-activity-image" id="img-activity-3" alt="Pick Activity" />
              </div>
              <div className="section-activity">
                <h3 className="center-text">Pack singles</h3>
                <img src={process.env.PUBLIC_URL + '/assets/man-warehouse-working-with-packages.jpg'} width="250px" height="200px" className="bg-activity-image" id="img-activity-4" alt="Pack Singles Activity" />
              </div>
            </div>
            <div>
              <div className="section-activity">
                <h3 className="center-text">Pack multi</h3>
                <img src={process.env.PUBLIC_URL + '/assets/delivery-employees-working-together.jpg'} width="250px" height="200px" className="bg-activity-image" id="img-activity-5" alt="Pack Multi Activity" />
              </div>
            </div>
          </div>
          <form method="get" action="/video_input">
            <button className="button-select-activity">Select</button>
          </form>
        </main>
        <script defer src={process.env.PUBLIC_URL + '/js/script.js'}></script>
      </body>
    </html>
  );
};