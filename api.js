const fetch = require('node-fetch').default;
const { MongoClient } = require('mongodb');


// MongoDB connection URL
const mongoUrl = 'mongodb://localhost:27017';
const dbName = 'spotify';
const collectionName = 'presences';


// Spotify authorization token
const token = 'TEST_TOKEN'; // Replace with your Spotify token

async function fetchWebApi(endpoint, method, body) {
    const res = await fetch(`https://api.spotify.com/${endpoint}`, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
        method,
        body: JSON.stringify(body),
    });
    return await res.json();
}

async function getTrackUrisFromMongo() {
    const client = new MongoClient(mongoUrl);
    await client.connect();

    const db = client.db(dbName);
    const collection = db.collection(collectionName);

    const tracks = await collection.find({}).toArray();

    const trackUris = tracks.map(track => track.uri);

    await client.close();

    return trackUris;
}

async function createPlaylist() {
    const trackUris = await getTrackUrisFromMongo();

    const { id: user_id } = await fetchWebApi('v1/me', 'GET');

    const playlist = await fetchWebApi(
        `v1/users/${user_id}/playlists`, 'POST', {
        "name": "My recommendation playlist",
        "description": "Playlist created by the tutorial on developer.spotify.com",
        "public": false,
    }
    );

    await fetchWebApi(
        `v1/playlists/${playlist.id}/tracks?uris=${trackUris.join(',')}`,
        'POST'
    );

    return playlist;
}

async function main() {
    const createdPlaylist = await createPlaylist();
    console.log(createdPlaylist.name, createdPlaylist.id);
}

main().catch(console.error);