from rhythm_practice.generate import generate_jianpu_file, parse_mode
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="本软件可以随机生成一系列由各种节奏型组成的简谱，旨在帮助同学在音乐学习过程中熟练掌握节奏型。"
    )

    mode_help_str = """onebeat 将生成各种一拍节奏型
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
        "-n",
        "--num_of_beats",
        type=int,
        default=8,
        help="输入总共需要生成多少,默认生成8拍",
    )

    parser.add_argument(
        "-s", "--time_signature", type=str, default="4/4", help="输入拍号(默认为4/4拍)"
    )

    parser.add_argument(
        "-t", "--title", type=str, default="节奏练习", help="输入生成的简谱的标题"
    )

    parser.add_argument(
        "-o", "--output", type=str, default="./rhythm_practice.pdf", help="选择生成的文件名"
    )

    args = parser.parse_args()
    mode = parse_mode(args.mode)
    num_of_beats = args.num_of_beats
    title = args.title
    time_signature = args.time_signature
    output_file = args.output
    generate_jianpu_file(num_of_beats, mode, title, time_signature, output_file=output_file)


if __name__ == "__main__":
    main()
