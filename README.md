# midi-smoother

To edit midi incremental pedal signals (control 64 sustain) for better playback on on/off only instruments. Set a threshold value (between 1-127) and convert all control 64 values to '0'.

## Dependencies

Python MIDI library - by vishnubob

    https://github.com/vishnubob/python-midi

## Build binary

Use pyinstaller to package the utility to single executable file.
    
    $ pyinstaller -F midismoother
