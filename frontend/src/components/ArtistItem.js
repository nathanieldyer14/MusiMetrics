// ArtistItem.js
import React from "react";
import Card from "react-bootstrap/Card";

function ArtistItem({ artist }) {
  return (
    <Card>
      <Card.Img variant="top" src={artist.image.url} />
      <Card.Body>
        <Card.Title>{artist.name}</Card.Title>
      </Card.Body>
    </Card>
  );
}

export default ArtistItem;
