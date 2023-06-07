# midi-smoother

#### edit-ctrl64
To edit midi incremental pedal signals (control 64 sustain) for better playback on on/off only instruments. Set a threshold value (between 1-127) and convert all control 64 values to '0'.

#### edit-note
To cut notes above the high threshold and/or under the low threshold.

#### dump
To dump the content of the MIDI file in readable format.

## Dependencies

Python MIDI library - by vishnubob

    https://github.com/vishnubob/python-midi

## Build binary

Use pyinstaller to package the utility to single executable file.

    $ pyinstaller -F src/midismoother.py

## Usage

Run the midismoother/midismoother.exe on Linux/Windows.

    usage: midismoother [-h] [-v] COMMANDS ...

    Midi smoother utility

    positional arguments:
      COMMANDS
        edit-ctrl64  edit ControlChangeEvent 64
        edit-note    edit NoteOnEvent/NoteOffEvent
        dump         dump the MIDI file

    optional arguments:
      -h, --help     show this help message and exit
      -v, --version  show program's version number and exit

Examples:

    $ midismoother edit-ctrl64 -t 64 -o new.mid origin.mid
    $ midismoother edit-note -lt 20 -ht 90 "*.mid"
    
