#!/usr/bin/python3

from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://c3voc.de/share/schedules/tib3s.xml'

def introFrames(args):
    #fade in title
    frames = 5*fps
    for i in range(0, frames):
        yield(
            ('title', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
        )

def backgroundFrames(parameters):
    frames = 3*fps
    for i in range(0, frames):
        yield(
            ('logo', 'style', 'opacity', 1),
        )

def outroFrames(args):
    frames = 3*fps
    for i in range(0, frames):
        yield(
            ('logo',    'style', 'opacity', 1),
        )

def pauseFrames(args):
    #fade in pause
    frames = 3*fps
    for i in range(0, frames):
        yield(
            ('Pause',  'style', 'opacity', "%.4f" % easeInCubic(i, 0.2, 1, frames)),
        )

    # fade out
    frames = 3*fps
    for i in range(0, frames):
        yield(
            ('Pause',  'style', 'opacity', "%.4f" % easeInCubic(i, 1, -0.8, frames)),
        )

def debug():
    render('intro.svg',
        '../introXL.ts',
        introFrames,
        {
            '$id': 7775,
            '$title': 'BigDataEurope - The collaborative creation of an open software platform for researchers addressing Europe\'s societal challenges',
            '$subtitle': 'With some subtitle!',
            '$personnames':  'Nikolaus Forgó'
        }
    )

    render('intro.svg',
        '../intro.ts',
        introFrames,
        {
            '$id': 7776,
            '$title': 'Solid scenario’s for sustainable software',
            '$subtitle': 'With some subtitle!',
            '$personnames':  'Patrick J. Aerts'
        }
    )

    render('outro.svg',
        '../outro.ts',
        outroFrames
    )

    render(
        'background.svg',
        '../background.ts',
        backgroundFrames
    )

    render('pause.svg',
        '../pause.ts',
        pauseFrames
    )


def tasks(queue, args, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
        if not (idlist==[]):
                if 000000 in idlist:
                        print("skipping id (%s [%s])" % (event['title'], event['id']))
                        continue
                if int(event['id']) not in idlist:
                        print("skipping id (%s [%s])" % (event['title'], event['id']))
                        continue

        # generate a task description and put them into the queue
        queue.put(Rendertask(
            infile = 'intro.svg',
            outfile = str(event['id'])+".ts",
            sequence = introFrames,
            parameters = {
                '$id': event['id'],
                '$title': event['title'],
                '$subtitle': event['subtitle'],
                '$personnames': event['personnames']
            }
        ))

    # place a task for the outro into the queue
    if not "out" in skiplist:
        queue.put(Rendertask(
            infile = 'outro.svg',
            outfile = 'outro.ts',
            sequence = outroFrames
         ))

    # place the pause-sequence into the queue
    if not "pause" in skiplist:
        queue.put(Rendertask(
            infile = 'pause.svg',
            outfile = 'pause.ts',
            sequence = pauseFrames
        ))

    # place the background-sequence into the queue
    if not "bg" in skiplist:
        queue.put(Rendertask(
            infile = 'background.svg',
            outfile = 'background.ts',
            sequence = backgroundFrames
        ))
