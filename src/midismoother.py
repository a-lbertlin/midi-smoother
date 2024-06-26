#!/usr/bin/env python
import sys
import glob
import argparse
import traceback

import midi


def edit_control64(args):

    infiles = glob.glob(args.infiles)
    threshold = 60
    if args.threshold:
        threshold = args.threshold

    for infile in infiles:
        if len(infiles) == 1 and args.outfile:
            outfile = args.outfile
        else:
            outfile = ".".join(infile.split(".")[:-1]) + "-t" + str(threshold) \
                      + "." + infile.split(".")[-1]

        # Read MIDI file
        pattern = midi.read_midifile(infile)

        for track in pattern:
            for event in track:
                if isinstance(event, midi.events.ControlChangeEvent):
                    # midi.ControlChangeEvent(tick=36, channel=0, data=[64, 37])
                    if (event.data[0] == 64 and event.data[1] <= threshold):
                        event.data[1] = 0

        # Write MIDI file
        midi.write_midifile(outfile, pattern)

def edit_note(args):

    def toRemove(e):
        # midi.NoteOnEvent(tick=1, channel=0, data=[75, 18])
        # midi.NoteOffEvent(tick=1, channel=0, data=[75, 64])
        if isinstance(e, midi.events.NoteOnEvent) \
            or isinstance(e, midi.events.NoteOffEvent):
            if e.data[0] <= low_threshold or e.data[0] >= high_threshold:
                return True
        return False

    infiles = glob.glob(args.infiles)

    append = ""
    if args.low_threshold:
        low_threshold = args.low_threshold
        append += "-lt" + str(low_threshold)
    else:
        low_threshold = 0

    if args.high_threshold:
        high_threshold = args.high_threshold
        append += "-ht" + str(high_threshold)
    else:
        high_threshold = 999
        
    for infile in infiles:
        if len(infiles) == 1 and args.outfile:
            outfile = args.outfile
        else:
            outfile = ".".join(infile.split(".")[:-1]) + append \
                      + "." + infile.split(".")[-1]

        # Read MIDI file
        pattern = midi.read_midifile(infile)

        #for track in pattern:
        #    track[:] = [e for e in track if not toRemove(e)]

        for track in pattern:
            for event in track:
                if isinstance(event, midi.events.NoteOnEvent) or \
                        isinstance(event, midi.events.NoteOffEvent):
                   if event.data[0] <= low_threshold or event.data[0] >= high_threshold:
                        event.data[0] = 0
                        event.data[1] = 0

        # Write MIDI file
        midi.write_midifile(outfile, pattern)

def link_notes(args):

    infiles = glob.glob(args.infiles)

    for infile in infiles:

        if len(infiles) == 1 and args.outfile:
            outfile = args.outfile
        else:
            outfile = ".".join(infile.split(".")[:-1]) + "-link" \
                      + "." + infile.split(".")[-1]

        # Read MIDI file
        pattern = midi.read_midifile(infile)
        print("File: %s, Tracks: %s" % (infile, len(pattern)))

        for track in pattern:
            length = len(track)
            print("Events: %s" % length)
            for i in range(length):

                # Search NoteOffEvent
                if isinstance(track[i], midi.events.NoteOffEvent):
                    ##print("%s: %s" % (i, track[i]))

                    # midi.NoteOffEvent(tick=0, channel=0, data=[69, 64]),
                    eventoff = track[i]
                    channel = eventoff.channel
                    note = eventoff.data[0]
                    tick = eventoff.tick

                    for j in range(i+1, length):
                        event = track[j]
                        # not concomitant note off/on
                        if event.tick > 0:
                            break

                        ##print("\t%s: %s" % (j, track[j]))
                        # skip events other than NoteOnEvent and not the same note
                        if (not isinstance(track[j], midi.events.NoteOnEvent)) \
                            or (event.channel != channel) or (event.data[0] != note):
                            continue

                        # found
                        #print(track[i])
                        #print(track[j])

                        ## set tick to -1 for removal later
                        track[i].tick = -1      # concomitant NoteOffEvent
                        track[j].tick = -1      # concomitant NoteOnEvent

                        ## add the NoteOffEvent tick to next event
                        if tick > 0:
                            for k in range(i+1, length):
                                ##print("\t\t%s: %s" % (k, track[k]))
                                if track[k].tick == -1:
                                    continue
                                #print(track[k])
                                track[k].tick += tick
                                #print("adjust tick to %s" % track[k].tick)
                                break

                        break

            # Remove events
            for event in track[:]:
                if event.tick == -1:
                    track.remove(event)           
            print("New Events: %s" % len(track))

        # Write MIDI file
        midi.write_midifile(outfile, pattern)

def dump(args):
    infiles = glob.glob(args.infiles)

    for infile in infiles:
        if len(infiles) == 1 and args.outfile:
            outfile = args.outfile
        else:
            outfile = infile + ".dump"

        # Read MIDI file
        pattern = midi.read_midifile(infile)

        with open(outfile, 'w') as f:
            f.write(repr(pattern))

def get_parser():

    parser = argparse.ArgumentParser(prog="midismoother",
                                     description="Midi smoother utility")
    parser.add_argument("-V", "--version", action="version", version="%(prog)s 2.0")

    # Common arguments
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("-o", "--outfile", type=str, help="output MIDI file", dest="outfile")
    common.add_argument("infiles", metavar="INFILES",
                        help="MIDI files (wildcard is supported)")

    subparsers = parser.add_subparsers(metavar="COMMANDS", dest="command")

    # Command: edit-ctrl64
    parser_ctrl64 = subparsers.add_parser("edit-ctrl64", parents=[common],
            description="To edit midi incremental pedal signals (control 64 sustain)",
            help="edit ControlChangeEvent 64")
    parser_ctrl64.set_defaults(function=edit_control64)
    parser_ctrl64.add_argument("-t", "--threshold", type=int, default=60, dest="threshold",
                               help="threshold of control 64 sustain, [1-127, default=60]")

    # Command: edit-note
    parser_note = subparsers.add_parser("edit-note", parents=[common],
            description="To cut notes above the high threshold and/or under the low threshold",
            help="edit NoteOnEvent/NoteOffEvent")
    parser_note.set_defaults(function=edit_note)
    parser_note.add_argument("-lt", "--low-threshold", type=int, dest="low_threshold",
                             help="cute notes under the threshold")
    parser_note.add_argument("-ht", "--high-threshold", type=int, dest="high_threshold",
                             help="cute notes above the threshold")

    # Command: link-note
    parser_dump = subparsers.add_parser("link-notes", parents=[common],
            description="To remove the note off and on events at the same tick (delta time 0)",
            help="remove concomitant note off and on")
    parser_dump.set_defaults(function=link_notes)    

    # Command: dump
    parser_dump = subparsers.add_parser("dump", parents=[common],
            description="To dump the content of the MIDI file in readable format",
            help="dump the MIDI file")
    parser_dump.set_defaults(function=dump)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser


def main():

    retcode = 0
    try:
        parser = get_parser()
        args = parser.parse_args()
        args.function(args)

    except Exception:
        retcode = 1
        print(traceback.format_exc())

    sys.exit(retcode)


if __name__ == '__main__':
    main()
