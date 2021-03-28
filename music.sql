DROP TABLE PLAYLIST;
DROP TABLE MUSIC;

CREATE TABLE PLAYLIST (
    playlist_id INTEGER PRIMARY KEY,
    playlist_url VARCHAR NOT NULL
);

CREATE TABLE MUSIC (
    music_id INTEGER PRIMARY KEY,     
    title VARCHAR NOT NULL,
    artist CHAR(30) NOT NULL,
    playlist_id INT NOT NULL,
    FOREIGN KEY (playlist_id) REFERENCES playlist (playlist_id)
);