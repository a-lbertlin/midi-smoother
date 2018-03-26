#!/usr/bin/env python
import sys
import argparse
import traceback

import midi


def edit_control64(args):

    infile = args.infile
    outfile = ".".join(infile.split(".")[:-1]) + "-1." + infile.split(".")[-1]
    threshold = 60
    if args.outfile:
        outfile = args.outfile
    if args.threshold:
        threshold = args.threshold

    # Read MIDI file
    pattern = midi.read_midifile(infile)

    # Support only one track
    tracks = pattern[0]

    for event in tracks:
        if isinstance(event, midi.events.ControlChangeEvent):
            # midi.ControlChangeEvent(tick=36, channel=0, data=[64, 37])
            if (event.data[0] == 64 and event.data[1] <= threshold):
                event.data[1] = 0

    # Write MIDI file
    midi.write_midifile(outfile, pattern)


def get_parser():

    parser = argparse.ArgumentParser(prog="midismoother",
                                     description="Midi smoother utility",
                                     version="1.0",
                                     add_help=True)
    parser.print_usage = parser.print_help

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    parser.set_defaults(function=edit_control64)
    parser.add_argument("-t", "--threshold", type=int,
                        help="threshold of control 64 sustain, [1-127, default=60]",
                        default=60, dest="threshold")
    parser.add_argument("-o", "--outfile", type=str, help="output MIDI file", dest="outfile")
    parser.add_argument("infile", metavar="INFILE", help="MIDI file")

    return parser


def main():

    retcode = 0
    try:
        parser = get_parser()
        args = parser.parse_args()
        args.function(args)

    except Exception:
        retcode = 1
        print traceback.format_exc()

    sys.exit(retcode)


if __name__ == '__main__':
    main()
