# 「天涯论坛」存档

## forumScraper.py

抓取天涯论坛特定版面里的全部帖子的元数据（标题，链接，作者，作者UID），保存到 data/*.txt 。  
抓完了会往 .txt 加一行结束标记： `--End--` 。

## testForumIDs.py

从 1 开始，测试版面id是否存在，结果保存在 testedForumIDs.txt 里。

## forum-ids.txt

收集天涯的版面id