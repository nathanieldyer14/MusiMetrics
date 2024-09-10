import React from "react";
import SongItem from "./SongItem";
import ArtistItem from "./ArtistItem";
import ListGroup from "react-bootstrap/ListGroup";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";

const BackendInteraction = (props) => {
  const { sectionData, selectedSection } = props;

  if (!sectionData) {
    // Return some loading or empty state if data is not available yet
    return <div>Loading...</div>;
  }

  const {
    Ids = [],
    Dates = [],
    "Song Titles": songTitles = [],
    Artists = [],
    "Album Art": albumArt = [],
    Lyrics = [],
    Images = [],
  } = sectionData;

  const maxLength = Math.max(
    Ids.length,
    Dates.length,
    songTitles.length,
    Artists.length,
    albumArt.length,
    Lyrics.length
  );

  return (
    <div>
      <Container>
        <Row>
          <Col sm={3}>
            <ListGroup as="ol" numbered variant="flush">
              {/* Loop over the arrays */}
              {Array.from({ length: maxLength }).map((_, index) => (
                <ListGroup.Item as="li" key={index}>
                  {selectedSection === "recent_songs" ||
                  selectedSection === "top_songs" ? (
                    <SongItem
                      key={index}
                      song={{
                        id: Ids[index] || "N/A",
                        date: Dates[index] || "", // Provide an empty string if not available
                        songName: songTitles[index] || "N/A",
                        artist: Artists[index] || "N/A",
                        albumArt: albumArt[index] || "https://placehold.it/200",
                        lyrics: Lyrics[index] || "N/A",
                      }}
                    />
                  ) : selectedSection === "top_artists" ? (
                    <ArtistItem
                      key={index}
                      artist={{
                        name: Artists[index],
                        image: {
                          url: Images[index]?.url || "https://placehold.it/200",
                        },
                      }}
                    />
                  ) : null}
                </ListGroup.Item>
              ))}
            </ListGroup>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default BackendInteraction;
