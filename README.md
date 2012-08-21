AVCProfileLevelEditor
=====================

H.264/AVC Profile and Level Editor for PlayStation Vita 

有很多PlayStation® Vita不能播放的MP4可以通过修改H.264/AVC的Profile Level使其
支持.
目前已知的Vita认可Profile Level为:
  Main Profile 2.1 0x4D 40 15
  Main Profile 3.1 0x4D 40 1f
  High Profile 3.1 0x64 00 1f
并且只有同Profile间修改可以支持

使用方法:
确认有Python 3的运行环境以后, 切换到本程序所在目录(或者设置环境变量), 格式:
  python3 main.py 文件列表
  本程序支持一次修改多个文件
如果操作成共完成原始文件会被修改, 并且生成一个记录文件用来保存原来的Profile Level
如果修改后的文件不能播放的话使用:
  python3 main.py -r 要恢复的那个文件路径
会读取记录文件并恢复成修改前的状态

日志文件格式:
前三个字节(byte)为原始Profile Level的二进制信息, 第二行是所在文件中位置, 第
三行是Profile Level的16进制表示

可能存在的问题:
  1. 因为对MPEG-4文件结构不是很了解, 不知道它的文件头有多长, 所以本程序只读
  取前8192个字节信息进行修改, 可能有些文件会有问题
  2. 目前只支持ISO Media, MPEG v4 system, version 1
  3. 即使是ISO Media, MPEG v4 system, version 1但是没有在前8k找到avcC标识也
  不被支持
  4. High Profile 4.1转到3.1只有前面部分能播放


