import numpy as np
from MIDI.midi_to_name import midi_to_name, hit_mapping
from mido import MidiFile, MetaMessage, tick2second, bpm2tempo

def midi_to_hit(filename = 'MIDI/midi_drums.mid'):

    mid = MidiFile(filename)
    ticks_per_beat = mid.ticks_per_beat
    track = mid.tracks[0]
    tempo = bpm2tempo(90)
    hits = []
    last_hit_time = 0
    total_time = 0
    for msg in track:
        if type(msg) == MetaMessage:
            if msg.type == 'set_tempo':

                tempo = msg.tempo

        total_time += tick2second(msg.time, ticks_per_beat, tempo)
        last_hit_time += tick2second(msg.time, ticks_per_beat, tempo)
        if msg.type == 'note_on' and msg.note in midi_to_name.keys():
            hit = midi_to_name[msg.note]
            if hit in hit_mapping.keys():
                simplified_hit = hit_mapping[hit]
                hits.append({"hit": simplified_hit, "last_hit_time": last_hit_time, "total_time": total_time, "strength": msg.velocity})
                last_hit_time = 0
    return hits