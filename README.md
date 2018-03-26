# midi-smoother

To edit midi incremental pedal signals (control 64 sustain) for better playback on on/off only instruments. Set a threshold value (between 1-127) and convert all control 64 values to '0'.

## Dependencies

Python MIDI library - by vishnubob

    https://github.com/vishnubob/python-midi

## Build binary

Use pyinstaller to package the utility to single executable file.
    
    $ pyinstaller -F midismoother

## Usage

Run the midismoother/midismoother.exe on Linux/Windows.

    usage: midismoother [-h] [-v] [-t THRESHOLD] [-o OUTFILE] INFILES

    Midi smoother utility

    positional arguments:
      INFILES               MIDI files (wildcard is supported)

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -t THRESHOLD, --threshold THRESHOLD
                            threshold of control 64 sustain, [1-127, default=60]
      -o OUTFILE, --outfile OUTFILE
                            output MIDI file
    
Examples:

    $ midismoother -t 64 -o new.mid origin.mid
    $ midismoother *.mid
    
