# TODO: THIS IS NO LONGER VALID, DO NOT USE

import models
from bpsynctools import add_to_exportimport

models.initialize_engine('data/songs.db')

with models.Session() as session:
    db_songs = session.query(models.StoredSong).all()

for song in db_songs:
    add_to_exportimport(song, "out.txt")