// SongItem.js
import React, { useState } from "react";
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";

function SongItem({ song }) {
  const [showLyrics, setShowLyrics] = useState(false);

  // Extract the URL with a height and width of 300x300
  const albumArtUrl = song.albumArt[1]?.url || "https://placehold.it/300";

  // Format the date only if it's defined
  const formattedDate = song.date
    ? new Date(song.date).toLocaleString("en-US", {
        month: "numeric",
        day: "numeric",
        year: "numeric",
        hour: "numeric",
        minute: "numeric",
        second: "numeric",
        timeZoneName: "short",
      })
    : null;

  const handleLyricsClick = () => {
    setShowLyrics(!showLyrics);
  };

  return (
    <Card>
      <Card.Img variant="top" src={albumArtUrl} />
      <Card.Body>
        <Card.Title>{song.songName}</Card.Title>
        <Card.Text>
          <strong>Artist:</strong> {song.artist}
          <br />
          {formattedDate && (
            <>
              <strong>Date:</strong> {formattedDate}
              <br />
            </>
          )}
        </Card.Text>
        <Button onClick={handleLyricsClick}>
          {showLyrics ? "Hide Lyrics" : "Show Lyrics"}
        </Button>
        {showLyrics && (
          <Card.Text>
            <strong>Lyrics:</strong> {song.lyrics || "N/A"}
          </Card.Text>
        )}
      </Card.Body>
    </Card>
  );
}

export default SongItem;
