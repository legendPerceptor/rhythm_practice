# 节奏练习生成器

我在学习音乐的过程中，发现自己对节奏节拍的掌握比较薄弱，本项目可以自动生成各类节奏型混合的简谱，有助于锻炼节奏能力。网上主流的制谱软件对简谱编写支持较少（像 [MuseScore](https://musescore.org/en) 只支持五线谱），[番茄简谱](http://zhipu.lezhi99.com/Zhipu-index.html)等国内的软件并不是开源的，无法编写自动化脚本。经过搜寻，我发现了[LilyPond](https://lilypond.org/)这款开源的制谱软件。配合[jianpu-ly.py](https://github.com/ssb22/jianpu-ly)这个项目，可以比较方便地编写简谱。Lilypond 的脚本需要编译生成 pdf 或者图片文件，并不是所见即所得，所以不太适合作曲，但非常适合通过程序随机生成节奏型混合。
