import time
import sys
from forumScraper import isExistForumID, create_session

TXT = open(f'testedForumIDs-{int(time.time())}.txt', 'w')
session = create_session()
c_False = 0
id = 1
while id:
    idStatus = isExistForumID(str(id), session=session)
    print(f'{id}\t{idStatus}', end='            \r')
    if idStatus:
        c_False = 0
        TXT.write(f'{id}\t{idStatus}\n')
    else:
        c_False += 1

    if c_False == 150: # 连续 150 个 id 不存在
        sys.exit()

    id += 1
TXT.close()