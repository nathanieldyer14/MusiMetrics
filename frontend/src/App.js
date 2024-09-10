// App.js
import React, { useState, useEffect } from "react";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import BackendInteraction from "./components/BackendInteraction";
import ArtistItem from "./components/ArtistItem";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";

function App() {
  const [selectedSection, setSelectedSection] = useState("recent_songs");
  const [recentData, setRecentData] = useState([{}]);
  const [topSongsData, setTopSongsData] = useState([{}]);
  const [topArtistsData, setTopArtistsData] = useState([{}]);
  const [showModal, setShowModal] = useState(false);
  const [playlistQuery, setPlaylistQuery] = useState("");
  const [playlistCreated, setPlaylistCreated] = useState(false);
  const [notificationMessage, setNotificationMessage] = useState("");

  useEffect(() => {
    // Fetch recent songs data
    fetch("/getRecentTracks?n=10")
      .then((res) => res.json())
      .then((res) => {
        setRecentData(res);
      });

    // Fetch top songs data
    fetch("/getTopTracks?n=10&time_range=long_term")
      .then((res) => res.json())
      .then((res) => {
        setTopSongsData(res);
      });

    // Fetch top artists data
    fetch("/getTopArtists?n=10&time_range=long_term")
      .then((res) => res.json())
      .then((res) => {
        setTopArtistsData(res);
      });
  }, []);

  const handleNavClick = (section) => {
    setSelectedSection(section);
    if (section === "playlist_generation") {
      setShowModal(true);
    }
  };

  const handleShowModal = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setPlaylistQuery("");
  };

  const handleGeneratePlaylist = () => {
    // Backend logic to generate playlist
    fetch(`/generatePlaylist?query=${playlistQuery}`)
      .then((res) => res.json())
      .then(() => {
        // Assuming res is the playlist image URL
        setPlaylistCreated(true);
        setNotificationMessage(
          "Your playlist has been created! Check your Spotify."
        );

        // Close the modal after 5 seconds (adjust duration as needed)
        setTimeout(() => {
          setShowModal(false);
          setNotificationMessage(""); // Clear the notification message
        }, 5000);
      })
      .catch((error) => {
        console.error("Error generating playlist:", error);
      });
    // .finally(() => {
    //   setShowModal(false); // Close the modal after generating playlist
    // });
  };

  return (
    <>
      <header>
        <Navbar expand="xl" className="bg-body-tertiary">
          <Container>
            <Navbar.Brand href="#home">MusiMetrics</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="ms-auto">
                <Nav.Link onClick={() => handleNavClick("recent_songs")}>
                  recent_songs
                </Nav.Link>
                <Nav.Link onClick={() => handleNavClick("top_songs")}>
                  top_songs
                </Nav.Link>
                <Nav.Link onClick={() => handleNavClick("top_artists")}>
                  top_artists
                </Nav.Link>
                <Nav.Link onClick={handleShowModal}>
                  playlist_generation
                </Nav.Link>
              </Nav>
            </Navbar.Collapse>
          </Container>
        </Navbar>
      </header>
      <main>
        <div>
          {/* Modal for Playlist Generation */}
          <Modal show={showModal} onHide={handleCloseModal}>
            <Modal.Header closeButton>
              <Modal.Title>Generate Playlist</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <Form>
                <Form.Group controlId="formPlaylistQuery">
                  <Form.Label>Enter your playlist query:</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="Ex: chill"
                    value={playlistQuery}
                    onChange={(e) => setPlaylistQuery(e.target.value)}
                  />
                </Form.Group>
                {playlistCreated && (
                  <div className="notification">
                    <p>{notificationMessage}</p>
                  </div>
                )}
              </Form>
            </Modal.Body>
            <Modal.Footer>
              <Button variant="secondary" onClick={handleCloseModal}>
                Close
              </Button>
              <Button variant="primary" onClick={handleGeneratePlaylist}>
                Generate Playlist
              </Button>
            </Modal.Footer>
          </Modal>

          {/* Notification for Playlist Creation
          {playlistCreated && (
            <div className="notification">
              <p>Your playlist has been created!</p>
              {playlistImage && (
                <img src={playlistImage} alt="Playlist Cover" />
              )}
            </div>
          )} */}

          {/* Pass corresponding data and selected section to BackendInteraction */}
          {selectedSection === "recent_songs" && (
            <BackendInteraction
              sectionData={recentData}
              selectedSection={selectedSection}
            />
          )}
          {selectedSection === "top_songs" && (
            <BackendInteraction
              sectionData={topSongsData}
              selectedSection={selectedSection}
            />
          )}
          {selectedSection === "top_artists" && (
            <BackendInteraction
              sectionData={topArtistsData}
              selectedSection={selectedSection}
            />
          )}
          {selectedSection === "playlist_generation" && (
            <BackendInteraction
              sectionData={null}
              selectedSection={selectedSection}
            />
          )}
        </div>
      </main>
    </>
  );
}

export default App;
