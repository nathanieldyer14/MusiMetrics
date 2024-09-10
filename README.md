## NOTE: This is a copy of a UIUC project I (Nathaniel Dyer) worked on
The original is here: https://github.com/nsunkad/wikispeedier

# Introduction

## Overview of MusiMetrics

Our app is a tool for Spotify users to look at their Spotify metrics over time and visualize their data. It also allows users to create their own playlist based on keywords and moods.

For more details, view the full project proposal: https://docs.google.com/document/d/1IZ0haG5nM1Q9TsJw8x4M6R4u88BkYJSCYi_dcEvHDYU/edit#heading=h.qougbnz1fcec 

You can also view our complete presentation: https://docs.google.com/presentation/d/12kd-OmkILCwT-hk_IjYdU7SUtvzhXs3IchQFdmr7D-M/

# Technical Architecture

You can view our technical architecture diagram in the project proposal document above, and complete descriptions of the interactions between technologies in the presentation.

Technologies used:

Backend
- Spotify Web API
- SpotiPy Library
- LyricsGenius API

Frontend
- HTML/CSS
- React
- Flask

# Developers

Backend:
- **Dhruv Raval**: Worked on playlist generation, Flask, and OAuth connection with the Spotify API.
- **Nathaniel Dyer**: Worked on Lyrics Generation, Flask, and built out data retreival methods for the backend.


Frontend:
- **Clea Sharp**: Worked on frontend connection with the backend.
- **Shaurya Gupta**: Worked on frontend design and development.

# Environment Setup

## Initial environment setup

Navigate to your source directory, and then find the .env file.

Change your IDs to your own credentials. Instructions on how to obtain these credentials is found below.

Navigate to the Spotify Developer Dashboard and the Genius API website and create credentials. After doing so, copy and paste those credentials into the CLIENT_ID, CLIENT_SECRET, and GENIUS_CLIENT_TOKEN fields.

## Running Flask

In your terminal, input the following command:

```
python3 -m flask run (Mac)
python -m flask run (Windows)
```

This will enable the Flask server to begin running.

## Running the Frontend

Navigate to the frontend directory (you can use the ```cd frontend``` command)

Run the following commands:
```
npm install
npm start
```

*Note: Ensure you have npm installed on your machine and the required packages installed throughout the entire project. Packages can be installed using pip or your preferred package installer.*

### Running the Web App
Once everything is running, go to the localhost link that is displayed in your browser. From here, you can click through the various features and see your results. 
