from enum import Enum
from pathlib import Path

import sys
import random
import argparse
import subprocess
import time

from .jianpuly import process_input, write_output


class BeatPattern:
    def __init__(self, name: str, pattern: str, length: int):
        self.name = name
        self.pattern = pattern
        self.length = length

    def __str__(self):
        return f"<{self.name}, {self.length}>"

    def __repr__(self):
        return f"<{self.name}, {self.length}>"

    def get_pattern(self):
        return self.pattern


class RhythmModes(Enum):
    RandomOneBeats = 1
    RandomTwoBeats = 2
    RandomMixedOneBeatsAndTwoBeats = 3
    HardMixedWithTies = 4


OneBeatPatterns = [
    BeatPattern(name="四", pattern="x", length=1),
    BeatPattern(name="二八", pattern="qx qx", length=1),
    BeatPattern(name="八十六", pattern="qx sx sx", length=1),
    BeatPattern(name="十六八", pattern="sx sx qx", length=1),
    BeatPattern(name="四个十六", pattern="sx sx sx sx", length=1),
    BeatPattern(name="附点", pattern="qx. sx", length=1),
    BeatPattern(name="后附", pattern="sx qx.", length=1),
    BeatPattern(name="小切分", pattern="sx qx sx", length=1),
    BeatPattern(name="三连音", pattern="3[ qx qx qx ]", length=1),
]

TwoBeatPatterns = [
    BeatPattern(name="二", pattern="x -", length=2),
    BeatPattern(name="附点", pattern="x. qx", length=2),
    BeatPattern(name="后附", pattern="qx x.", length=2),
    BeatPattern(name="附点点", pattern="x. sx sx", length=2),
    BeatPattern(name="点点附", pattern="sx sx x.", length=2),
    BeatPattern(name="大切分", pattern="qx x qx", length=2),
    BeatPattern(name="大切分分", pattern="qx x sx sx", length=2),
    BeatPattern(name="大大切分", pattern="sx sx x qx", length=2),
    BeatPattern(name="大大切分分", pattern="sx sx x sx sx", length=2),
]

BeatPatternsWithTies = [
    BeatPattern(name="四连四", pattern="x ~ x", length=2),
    BeatPattern(name="四连八十六", pattern="x ~ qx sx sx", length=2),
    BeatPattern(name="四连二八", pattern="x ~ qx qx", length=2),
    BeatPattern(name="十六八连四", pattern="sx sx qx ~ x", length=2),
    BeatPattern(name="二八连四", pattern="qx qx ~ x", length=2),
    BeatPattern(name="二八连二八", pattern="qx qx ~ qx qx", length=2),
    BeatPattern(name="二八连八十六", pattern="qx qx ~ qx sx sx", length=2),
    BeatPattern(name="十六八连二八", pattern="sx sx qx ~ qx qx", length=2),
    BeatPattern(name="十六八连八十六", pattern="sx sx qx ~ qx sx sx", length=2),
    BeatPattern(name="四连小切分", pattern="x ~ sx qx sx", length=2),
    BeatPattern(name="二八连小切分", pattern="qx qx ~ sx qx sx", length=2),
    BeatPattern(name="四连三连音",pattern="x ~ 3[ qx qx qx ]", length=2),
    BeatPattern(name="二八连三连音", pattern="qx qx ~ 3[ qx qx qx ]", length=2),
    BeatPattern(name="四连四个十六", pattern="x ~ sx sx sx sx", length=2),
    BeatPattern(name="二八连四个十六", pattern="qx qx ~ sx sx sx sx", length=2),
    BeatPattern(name="八十六连小切分", pattern="qx sx sx ~ sx qx sx", length=2),
    BeatPattern(name="十六八连小切分", pattern="sx sx qx ~ sx qx sx", length=2),
    BeatPattern(name="八十六连三连音", pattern="qx sx sx ~ 3[ qx qx qx ]", length=2),
    BeatPattern(name="十六八连三连音", pattern="sx sx qx ~ 3[ qx qx qx ]", length=2),
    BeatPattern(name="八十六连四个十六", pattern="qx sx sx ~ sx sx sx sx", length=2),
    BeatPattern(name="十六八连四个十六", pattern="sx sx qx ~ sx sx sx sx", length=2),
    BeatPattern(name="四个十六连小切分", pattern="sx sx sx sx ~ sx qx sx", length=2),
    BeatPattern(name="小切分连四个十六", pattern="sx qx sx ~ sx sx sx sx", length=2),
    BeatPattern(name="四个十六连三连音", pattern="sx sx sx sx ~ 3[ qx qx qx ]", length=2),
    BeatPattern(name="三连音连四个十六", pattern="3[ qx qx qx ] ~ sx sx sx sx", length=2),
    BeatPattern(name="四个十六连四个十六", pattern="sx sx sx sx ~ sx sx sx sx", length=2)
]

OneAndTwoBeatPatterns = OneBeatPatterns + TwoBeatPatterns
HardMixedPatterns = OneAndTwoBeatPatterns + BeatPatternsWithTies


def get_random_sequence(
    sequence_list: list[BeatPattern], total_beats: int, per_measure_beats: int
):
    generated_list = []
    generated_measures = 0
    current_measure_beats = 0
    while generated_measures * per_measure_beats < total_beats:
        selected_pattern = random.choice(sequence_list)
        if current_measure_beats + selected_pattern.length <= per_measure_beats:
            generated_list.append(selected_pattern)
            current_measure_beats += selected_pattern.length
        else:
            selected_pattern = random.choice(OneBeatPatterns)
            generated_list.append(selected_pattern)
            current_measure_beats += selected_pattern.length
        if current_measure_beats == per_measure_beats:
            generated_measures += 1
            current_measure_beats = 0
    return generated_list


def generate_sequence_of_n_beats(
    num_of_beats: int, mode: RhythmModes, time_signature: str = "4/4"
):
    if num_of_beats < 4:
        print(f"请至少生成4拍以上的序列！您当前尝试生成{num_of_beats}拍，程序将退出！")
        sys.exit(1)

    num_beats_per_measure = int(time_signature.split("/")[0])
    if num_of_beats % num_beats_per_measure != 0:
        print(
            f"你想生成{num_of_beats}拍，但是每小节设置为{num_beats_per_measure}拍，无法整除，不嫩构建完整的小节，请重新设置！"
        )
        sys.exit(1)

    generated_list = []
    if mode == RhythmModes.RandomOneBeats:
        generated_list = [random.choice(OneBeatPatterns) for _ in range(num_of_beats)]
    elif mode == RhythmModes.RandomTwoBeats:
        generated_list = [
            random.choice(TwoBeatPatterns) for _ in range(num_of_beats // 2)
        ]
    elif mode == RhythmModes.RandomMixedOneBeatsAndTwoBeats:
        generated_list = get_random_sequence(
            OneAndTwoBeatPatterns, num_of_beats, num_beats_per_measure
        )
    elif mode == RhythmModes.HardMixedWithTies:
        generated_list = get_random_sequence(
            HardMixedPatterns, num_of_beats, num_beats_per_measure
        )
    else:
        raise TypeError("不存在所选的节奏模式")
    return generated_list


def parse_mode(mode: str) -> RhythmModes:
    if mode == "onebeat":
        return RhythmModes.RandomOneBeats
    elif mode == "twobeat":
        return RhythmModes.RandomTwoBeats
    elif mode == "mixed":
        return RhythmModes.RandomMixedOneBeatsAndTwoBeats
    elif mode == "hardmixed":
        return RhythmModes.HardMixedWithTies

    # Should not reach here
    return RhythmModes.RandomOneBeats


def get_jianpu_lilypond_str_from_BeatPatternList(
    num_of_beats: int,
    pattern_list: list[BeatPattern],
    title: str = "节奏练习",
    time_signature: str = "4/4",
):
    head = f"""% jianpu-ly.py 文檔
title={title}
{time_signature}

"""
    num_beats_per_measure = int(time_signature.split("/")[0])
    print("number of beats per measure: ", num_beats_per_measure)
    print("total_beats to generate: ", num_of_beats)
    if num_of_beats % num_beats_per_measure != 0:
        print(
            f"你想生成{num_of_beats}拍，但是每小节设置为{num_beats_per_measure}拍，无法整除，不嫩构建完整的小节，请重新设置！"
        )
        sys.exit(1)

    lines = []
    current_beats = 0
    line_patterns = []
    for pattern in pattern_list:
        current_beats += pattern.length
        line_patterns.append(pattern.get_pattern())
        if current_beats == num_beats_per_measure:
            lines.append(" ".join(line_patterns))
            current_beats = 0
            line_patterns = []

    article = head + "\n".join(lines) + "\n"
    return article


def compile_lilypond_file(lilypond_out: str, output_file):
    result = subprocess.run(
        ["lilypond", "--png", "-dbackend=eps", f"-o{output_file}", "-"],
        input=lilypond_out.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode == 0:
        print("Output file generated successfully.")
    else:
        print("Error:", result.stderr.decode("utf-8"))


def generate_jianpu_file(
    num_of_beats: int,
    mode: RhythmModes,
    title: str,
    time_signature: str,
    output_file: Path,
):
    random.seed(time.time())
    generated_list = generate_sequence_of_n_beats(num_of_beats, mode)
    print(generated_list)
    article = get_jianpu_lilypond_str_from_BeatPatternList(
        num_of_beats, generated_list, title=title, time_signature=time_signature
    )
    print(article)

    # Call jianpu-ly to generate the Lilypond file.
    lilypond_out = process_input(article)

    # Call Lilypond to compile the previous generated file to final pdf file.
    compile_lilypond_file(lilypond_out, output_file)
