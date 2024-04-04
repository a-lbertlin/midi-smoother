# midi-smoother

#### edit-ctrl64
To edit midi incremental pedal signals (control 64 sustain) for better playback on on/off only instruments. Set a threshold value (between 1-127) and convert all control 64 values to '0'.

#### edit-note
To cut notes above the high threshold and/or under the low threshold.

#### link-note
To remove the note off and on events at the same tick (delta time 0)

#### dump
To dump the content of the MIDI file in readable format.

## Dependencies

Python MIDI library - by vishnubob
```
https://github.com/vishnubob/python-midi
```

## Build binary

Use pyinstaller to package the utility to single executable file.
```
$ pyinstaller -F src/midismoother.py
```

## Usage

Run the midismoother/midismoother.exe on Linux/Windows.
```
usage: midismoother [-h] [-V] COMMANDS ...

Midi smoother utility

positional arguments:
  COMMANDS
    edit-ctrl64  edit ControlChangeEvent 64
    edit-note    edit NoteOnEvent/NoteOffEvent
    link-notes   remove concomitant note off and on
    dump         dump the MIDI file

options:
  -h, --help     show this help message and exit
  -V, --version  show program's version number and exit
```

Examples:
```
$ midismoother edit-ctrl64 -t 64 -o new.mid origin.mid
$ midismoother edit-note -lt 20 -ht 90 "*.mid"
```    
