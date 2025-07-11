from enum import Enum
import sys
import random
import argparse


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

OneAndTwoBeatPatterns = OneBeatPatterns + TwoBeatPatterns

BeatPatternsWithTies = [
    BeatPattern(name="四连四", pattern="x ~ x", length=2),
    BeatPattern(name="四连八十六", pattern="x ~ qx sx sx", length=2),
    BeatPattern(name="四连二八", pattern="x ~ qx qx", length=2),
    BeatPattern(name="十六八连四", pattern="sx sx qx ~ x", length=2),
    BeatPattern(name="二八连四", pattern="qx qx ~ x", length=2),
]


def generate_sequence_of_n_beats(num_of_beats: int, mode: RhythmModes):
    if num_of_beats < 4:
        print(f"请至少生成4拍以上的序列！您当前尝试生成{num_of_beats}拍，程序将退出！")
        sys.exit(1)
    generated_list = []
    if mode == RhythmModes.RandomOneBeats:
        generated_list = [random.choice(OneBeatPatterns) for _ in range(num_of_beats)]
    elif mode == RhythmModes.RandomTwoBeats:
        generated_list = [random.choice(TwoBeatPatterns) for _ in range(num_of_beats)]
    elif mode == RhythmModes.RandomMixedOneBeatsAndTwoBeats:
        generated_list = [
            random.choice(OneAndTwoBeatPatterns) for _ in range(num_of_beats)
        ]
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


def get_jianpu_lilypond_str_from_BeatPatternList(
    pattern_list: list[BeatPattern], title: str = "节奏练习"
):
    head = f"""% jianpu-ly.py 文檔
title={title}
4/4

"""
    n = len(pattern_list)
    lines = []
    for i in range(0, n, 4):
        group = pattern_list[i : i + 4]
        lines.append(" ".join([beatpattern.get_pattern() for beatpattern in group]))
    article = head + "\n".join(lines) + "\n"
    return article


def main():
    parser = argparse.ArgumentParser(
        description="本软件可以随机生成一系列由各种节奏型组成的简谱，旨在帮助同学在音乐学习过程中熟练掌握节奏型。"
    )

    mode_help_str = """onebeat 将生成各种一拍节奏型，
twobeat 将生成各种两拍节奏型
mixed 将生成各种混合节奏型
hardmixed 将生成含有前面所有的节奏型以及带连线的节奏型
"""
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        choices=["onebeat", "twobeat", "mixed", "hardmixed"],
        help=mode_help_str,
    )

    parser.add_argument(
        "-n", "--num_of_beats", type=int, default=8, help="输入总共需要生成多少拍"
    )

    args = parser.parse_args()
    mode = parse_mode(args.mode)
    generated_list = generate_sequence_of_n_beats(args.num_of_beats, mode)
    print(generated_list)
    article = get_jianpu_lilypond_str_from_BeatPatternList(generated_list)
    print(article)


if __name__ == "__main__":
    main()
