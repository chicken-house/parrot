<!-- TOC -->

- [parrot](#parrot)
    - [介绍](#介绍)
    - [使用](#使用)
            - [安装](#安装)
            - [初始化环境](#初始化环境)
            - [添加单次](#添加单次)
            - [复习单词](#复习单词)
    - [规则](#规则)
        - [添加规则](#添加规则)
        - [复习规则](#复习规则)
            - [复习时展示哪些内容](#复习时展示哪些内容)
            - [完整的复习计划是什么](#完整的复习计划是什么)
            - [复习的结果有哪些](#复习的结果有哪些)
            - [如果有一天没有复习，第二天再复习时怎么办](#如果有一天没有复习第二天再复习时怎么办)
            - [在进行第五阶段复习时，仍然需要看句子才能知道含义怎么办？](#在进行第五阶段复习时仍然需要看句子才能知道含义怎么办)
    - [具体实现](#具体实现)
    - [changelog](#changelog)
        - [Future](#future)
            - [随时听 P2](#随时听-p2)
            - [更新model P3](#更新model-p3)
            - [comparison功能 P3](#comparison功能-p3)
        - [2023-02 v2.1.0](#2023-02-v210)
            - [1. 对phonetic symbol合法性进行检查，防止输错 P1——Done](#1-对phonetic-symbol合法性进行检查防止输错-p1done)
            - [2. 支持修改word.text P0——Done](#2-支持修改wordtext-p0done)
            - [3. 支持仅修改meaning，而不重新生成ReviewPlan P0——Done](#3-支持仅修改meaning而不重新生成reviewplan-p0done)
            - [4. 实现泛读复习计划 P0——Done](#4-实现泛读复习计划-p0done)
            - [5. 实现查询功能 P0——Done](#5-实现查询功能-p0done)
            - [6. 模糊查询 P1——Done](#6-模糊查询-p1done)
            - [7. 复习计划打散 P1——Done](#7-复习计划打散-p1done)
            - [8. review过程升级——Done](#8-review过程升级done)
            - [9. predict算法更新 P2——Done](#9-predict算法更新-p2done)
            - [10. review过程分阶段保存，应对单词较多的情况 P1](#10-review过程分阶段保存应对单词较多的情况-p1)
        - [2022-5-4 v2.0.0](#2022-5-4-v200)
            - [实现一个单词多个含义的场景](#实现一个单词多个含义的场景)

<!-- /TOC -->
# parrot
<!-- /MarkdownTOC -->
## 介绍
该项目是一个背单词的工具。虽然有很多商业的背单词软件，但这些软件功能上大同小异，最重要的是这些软件并不能满足我的需求。下面是我整理的需求以及市面上已有软件的满足情况：

| 我的需求                                                                                                     | 现有工具                                                                                                                           |
|:-------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------|
| 创建自己的词库                                                                                               | 这一点很多软件支持                                                                                                                 |
| 电脑上使用。由于我是通过电脑来阅读英文材料，并收集未知的单词，因此电脑使用场景比较重。                       | 大部分软件都是以手机为主，电脑上几乎没什么功能。                                                                                   |
| 为单词添加语境。我觉得背单词得结合语境，所以将语境和单词一并记下来有助于单词的记忆，也可培养单词的语感       | 市面上大部分软件都不支持。虽然很多软件会给出自己的实例句子，但这些句子跟我读到这个单词的语境完全没有关系，我还是想添加自己的语境。 |
| 为单词添加新的含义。有些单词有特殊的用法，大部分已有的词典可能都没有涵盖到，因此需要自己去为单词创建新的含义 | 大部分现有软件不支持该需求，或者需要长时间的审批                                                                                   |
| 为单词添加备注。有些单词有特殊的用法，或者使用上有些要注意的地方，需要备注下来                               | 大部分现有软件不支持该需求                                                                                                         |

基于以上考虑，身为码农的我便决定为自己量身定做一个背单词工具，当然欢迎跟我有类似困扰的同学使用，并多提宝贵意见。
## 使用
#### 安装
`pip install git+https://github.com/chicken-house/parrot.git`
#### 初始化环境
`parrot migrate`
#### 添加单次
`parrot add`
#### 复习单词
`parrot review`

## 规则
### 添加规则
每日最多添加20个单词或短语
重新添加已经在词库的单词，会更新 changed_time ，并添加新的 review_plan，并把最后一个老的review_plan 的状态更新为“没记住”。

### 复习规则
#### 复习时展示哪些内容
展示单词、音标和句子，意思隐藏。
#### 完整的复习计划是什么
参考艾宾浩斯记忆曲线，time_to_review 为时间依据来复习。复习分为5个阶段，分别是1天后，2天后，6天后，15天后，30天后。举个例子：假如1.1添加的单词，复习时间分别为1.2、1.3、1.7、1.16、1.31。
#### 复习的结果有哪些
复习时，每个单词有三种结果：知道了，记住了，没记住。
 * 知道了。看到语义，想起了该单词的含义。这种选项下，会继续按照下面的复习计划来复习。
 * 记住了。只看单词就知道发音和含义，则是该选项。这种选项下，直接跳到第三复习阶段，即6天后复习。
 * 没记住。看了句子后仍不清楚单词的含义。这种选项下，重新跳回第一复习阶段，即1天后复习。
#### 如果有一天没有复习，第二天再复习时怎么办
把应该昨天复习的内容，拿到今天复习。比如昨天应该进行 hello 这个单词的第三阶段复习，但是临时有事没有复习。今天继续复习 hello 单词的第三阶段，复习完之后以当前时间为基准，7天后进行第四阶段复习。注意，这里不再根据 changed_time 来确定下一次复习时间，而是用当前的复习时间确定下一次复习时间。
#### 在进行第五阶段复习时，仍然需要看句子才能知道含义怎么办？
应该继续选择“知道了”，该单词的复习计划也会结束。这么做的考虑如下：
 * 这种情况应该比较少。所以对于这少数没有达到“记住了”的状态的单词，完全可以在下一次遇见时，重新添加，重新执行复习计划。
 * 背单词的目的是为了使用。既然能读明白，那么已经达到了基本的使用目的。

## 具体实现
创建一张复习计划表。代表每个单词的一次复习计划。只有7天内的复习计划才有效。
每次新加入一个单词，或者完成某一阶段（除了第五个复习阶段）的复习时，在该表中为该单词添加一条新的记录，代表下一次复习计划。
每次复习时，从复习计划表中选出未记录来复习，并根据复习结果和当前复习计划所处的阶段，决定是否为下一次复习创建新的复习计划。同时，将已经复习过的复习计划记录标记为已复习。

## changelog

### Future

#### 随时听 P2

支持将任意音频材料输入，然后行程逐句的音频+字幕。同时手机端可以播放，一方面增加输入，另一方面可以充分利用碎片化时间。
字幕：可以利用语音转文字，或者互联网上可以下载到的影视作品的字幕

#### 更新model P3

下一个大版本做，考虑：
* 是否将meaning和word合并？是否有必要单独为word建模？如果合并的话，fts可以添加word.text的索引，add的时候也可以使用fts来搜索

#### comparison功能 P3

新增一个model代表comparison，有多个meaning_id组成，有文字解释不同。
comparison有自己的review_plan。review_plan加一个type，代表
review的时候先展示每个meaning的word的text，
与meaning同级，有meaning和review_plan

### 2023-02 v2.1.0

#### 1. 对phonetic symbol合法性进行检查，防止输错 P1——Done

google貌似没找到
尝试从现有meaning中提取——当前方式

#### 2. 支持修改word.text P0——Done

查出来后，修改时第一个修改的是word.text

#### 3. 支持仅修改meaning，而不重新生成ReviewPlan P0——Done

#### 4. 实现泛读复习计划 P0——Done

看到英文能知道意思就行。最看最近7天的，时间不超过5分钟
新增一个model，`ERLookupRecord`
泛读review的时候没有unremember

#### 5. 实现查询功能 P0——Done

查询works和meaning

#### 6. 模糊查询 P1——Done

**为什么只创建use_case的fts**
因为external content的fts要求所有的列必须都在同一张table中，word.text不在meaning表中，所以有额外工作：
1. 要么，将word.text添加到meaning中，word表就没有存在意义了，需要修改model
2. 要么，创建另一个fts表来存储word。
这两种方式都会带来不不小的复杂性。
考虑到use_case中肯定有word.text，因此本次只添加use_case的fts。后续重构core model的时候再重新设计。
**todo**

prototype
    修改
        `INSERT INTO meaning_fts(meaning_fts, rowid, use_case) VALUES('delete', old_meaning.id, old_meaning.use_case);`
        `INSERT INTO meaning_fts(rowid, use_case) VALUES (meaning.id, meaning.use_case);`
    添加
        `INSERT INTO meaning_fts(rowid, use_case) VALUES (meaning.id, meaning.use_case);`
    重建
        `CREATE VIRTUAL TABLE IF NOT EXISTS meaning_fts USING fts5(use_case, content='meaning', content_rowid='id', tokenize = 'porter');`
        <!-- `DROP TABLE meaning_fts;` -->
        `INSERT INTO meaning_fts(meaning_fts) VALUES('delete-all');`
        `INSERT INTO meaning_fts(rowid, use_case) select meaning.id,meaning.use_case from meaning;`
    查询

        ```sql
            select word.text,meaning.meaning,meaning.use_case FROM meaning_fts 
                LEFT JOIN meaning ON meaning_fts.rowid=meaning.id
                LEFT JOIN word ON word.id=meaning.word_id
                WHERE meaning_fts = 'beaver' order by rank limit 10;
        ```
    
initialize、migrate的时候手写sql为meaning rebuild virtual table——Done
新写入或修改meaning的时候，都先delete再插入virtual table——Done
<!-- 修改meaning的时候，删除原来的virtual table记录，插入新的记录 -->
search的时候搜索`meaning.use_case`——Done
add的时候搜索`meaning.use_case`，然后展示所有match的meaning——Pending
    因为add的时候还要判断是否有该word，所以不能只搜索use_case

https://www.sqlite.org/fts5.html#external_content_tables


#### 7. 复习计划打散 P1——Done

下一个阶段的复习计划在某个范围内打散，防止分布不均匀。
打散时间范围为`randint(0, STAGE_DELTA_MAP[stage]//6)`

#### 8. review过程升级——Done

由现在的一个一个处理，改为如下过程：
1. 先统一review，并记录每个meaning的review结果，该阶段不创建新的ReviewPlan
2. 根据review结果统一生成ReviewPlan，同一个meaning如果有多个review结果，则依次：
    * if 存在`ReviewStatus.UNREMEMBERED`
        * 则以`ReviewStatus.UNREMEMBERED`为准来生成新计划
    * else
        * if 存在`ReviewStage`最大的且结果为`ReviewStatus.REVIEWED`的ReviewPlan
            * 则以该ReviewPlan来生成新计划
        * else
            * 以`ReviewStage`最大的且结果为`ReviewStatus.REMEMBERED`的ReviewPlan
3. commit

#### 9. predict算法更新 P2——Done

目的是能够计算出更长的时间

#### 10. review过程分阶段保存，应对单词较多的情况 P1

每次review，分成多组，每组5个单词。每组结束后就保存一次。

### 2022-5-4 v2.0.0
#### 实现一个单词多个含义的场景
由原来的`words->review_plans`模型，变为`words->meanings->review_plans`。
添加单词：
    1. 已存在的单词，则列出所有meanings，让user选择是否新建meanings
        如果不创建，则可以修改现有meaning
        如果创建，则新建meaning且新建review_plan
    2. 不存在的单词，则直接创建word、meaning、review_plan
复习单词：
    复习时，复习完本次review_plan的meaning之后，可以列出该word所有已存在且没有复习计划的meaning，让user选择是否复习其中一个。
        如果复习，则为该meaning建立review_plan
        如果不复习，什么都不做
        

