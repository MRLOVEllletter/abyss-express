from engine.display import print_header, print_line, slow_print, wait_enter, get_choice, print_menu, print_event_menu, get_event_choice
import random

EVENTS_POOL = [
    {
        "title": "街角的老人",
        "desc": "一个老人坐在街角的台阶上，似乎在等人。他看到你，微微点了点头。",
        "choices": [
            ("上前搭话", "talk"),
            ("默默走开", "leave")
        ],
        "result_talk": "老人说：'钟塔的指针是反的。记住，反的不只是时间。'你不太明白他的意思，但把这句话记在了心里。\n获得线索：钟塔的秘密",
        "result_leave": "你从老人身边走过。他的目光一直跟着你，直到你消失在街角。"
    },
    {
        "title": "废弃的报刊亭",
        "desc": "报刊亭的玻璃碎了，里面的报纸被风吹得到处都是。一张发黄的报纸上写着：'钟塔建成百年，镇长宣布将举办庆典。'日期是三十年前。",
        "choices": [
            ("翻找有用的东西", "search"),
            ("看看其他报纸", "read")
        ],
        "result_search": "你在柜台下面找到了一本破旧的日记。日记的主人似乎曾经是这里的报摊主。\n获得道具：陈旧的日记本",
        "result_read": "其他报纸上都是普通的小镇新闻——谁家的猫丢了，谁家的孩子考了第一名。看起来很平静的小镇。太平静了。"
    },
    {
        "title": "神秘的地下室入口",
        "desc": "你发现一扇半掩在地面的铁门。门上挂着一把锈迹斑斑的锁，锁上刻着奇怪的符号。",
        "choices": [
            ("想办法打开锁", "open"),
            ("先记下位置，以后再来", "note")
        ],
        "result_open": "你费了好大劲才撬开锁。铁门后面是一条通向地下的阶梯，黑暗而潮湿。你隐约听到深处有滴水声。\n你决定改天准备好再下来探索。",
        "result_note": "你记住了这个位置。也许以后会有用。"
    }
]

SOUND_POLICE_ENCOUNTERS = [
    "走廊尽头传来整齐的脚步声。是声音警察！你屏住呼吸，贴紧墙壁。脚步声越来越近，然后在距离你几米的地方停了下来……",
    "一束手电筒的光扫过你藏身的角落。你赶紧蹲下。光柱在你头顶晃了晃，然后移开了。你松了一口气。",
    "你听到前方传来一声尖叫，然后是急促的脚步声和某种沉闷的撞击声。声音警察就在附近巡逻。"
]


def _time_of_day(day, phase):
    names = ["白天", "傍晚", "夜晚"]
    decibel_limits = ["60分贝（正常说话）", "30分贝（耳语级别）", "完全静默"]
    warnings = [
        "可以正常说话，但不要太吵。",
        "请降低音量。耳语是安全的。",
        "绝对安静。任何声音都会触发清理机制。"
    ]
    return {
        "name": names[phase],
        "limit": decibel_limits[phase],
        "warning": warnings[phase],
        "phase": phase
    }


def _show_status(day, phase, player, clock_parts, found_residents, alerted):
    td = _time_of_day(day, phase)
    print_line("─")
    print(f"  第 {day}/7 天 · {td['name']}  |  限制音量：{td['limit']}")
    print(f"  HP：{player.hp}/{player.max_hp}  |  白钞：{player.white_bills}")
    print(f"  钟塔零件：{clock_parts}/3  |  已找到居民：{found_residents}")
    if alerted:
        print(f"  ⚠️ 声音警察已经注意到你了！")
    print_line("─")


def _sound_check(player, alerted):
    td = _time_of_day(0, 0)
    roll = random.random()
    if alerted:
        if roll < 0.4:
            slow_print("\n你听到了远处传来的脚步声。声音警察正在靠近！")
            print_menu("", [
                ("1", "快速躲进旁边的建筑"),
                ("2", "屏住呼吸，保持不动"),
                ("3", "转身就跑")
            ])
            choice = get_choice()
            if choice == "1":
                slow_print("你闪身躲进一栋废弃的建筑里。脚步声从门外经过，没有发现你。")
                return False
            elif choice == "2":
                slow_print("你贴着墙壁一动不动。脚步声越来越近……然后停在了你面前。")
                if random.random() < 0.5:
                    slow_print("手电筒的光在你脸上晃了晃，然后移开了。好险！")
                    return False
                else:
                    slow_print("'找到你了。'一个冰冷的声音说。")
                    player.take_damage(20)
                    slow_print("你被声音警察打了一棍，失去了20点HP。")
                    return player.hp <= 0
            else:
                slow_print("你拼命地跑。脚步声在身后紧追不舍。")
                if random.random() < 0.3:
                    slow_print("你摔倒了！声音警察追上了你……")
                    player.take_damage(30)
                    slow_print("你被狠狠地教训了一顿，失去了30点HP。")
                    return player.hp <= 0
                else:
                    slow_print("你钻进一条小巷，七拐八绕后终于甩掉了追兵。")
                    return False
    return False


def _random_event():
    return random.choice(EVENTS_POOL)


def _night_choice(player, safe_house_today):
    slow_print("\n天色已经完全暗了下来。")
    slow_print("你必须在完全静默的状态下找到一个安全的地方过夜。")
    print_line()
    if safe_house_today:
        print(f"  你知道今天的安全屋在：{safe_house_today}")
        print_menu("", [
            ("1", "前往安全屋"),
            ("2", "冒险探索（可能会遇到声音警察）")
        ])
        choice = get_choice()
        if choice == "1":
            slow_print(f"你小心翼翼地来到{safe_house_today}，关好门窗。")
            slow_print("这里很安全。你终于可以喘口气了。")
            heal = 15
            player.heal(heal)
            slow_print(f"休息一晚，HP恢复 {heal} 点。")
            return False
        else:
            slow_print("你决定在夜色中探索……")
            if random.random() < 0.5:
                return _sound_check(player, True)
            else:
                slow_print("运气不错，你没有遇到声音警察。")
                slow_print("但你也没找到什么有用的东西。")
                return False
    else:
        slow_print("你不知道安全屋在哪里。今晚只能碰运气了。")
        print_menu("", [
            ("1", "找一栋看起来安全的建筑过夜"),
            ("2", "继续探索，找线索（高风险）")
        ])
        choice = get_choice()
        if choice == "1":
            safe = random.random() < 0.4
            if safe:
                slow_print("你找到了一栋废弃的民居。虽然破旧，但至少能遮风挡雨。")
                slow_print("你蜷缩在角落里，度过了不安的一夜。")
                heal = 10
                player.heal(heal)
                slow_print(f"HP恢复 {heal} 点。")
                return False
            else:
                slow_print("你刚躺下，就听到了门外的脚步声……")
                return _sound_check(player, True)
        else:
            return _sound_check(player, True)


def run_dungeon(player):
    print_header("副本载入", "分贝小镇 · Decibel Town")
    slow_print("\n列车缓缓停靠在一个迷雾笼罩的小站台旁。")
    slow_print("你走下列车，空气中弥漫着潮湿的雾气。")
    slow_print("前方是一个安静得不太正常的小镇。")
    slow_print("你的手机收到一条消息：")
    print_line()
    slow_print("  【副本任务】")
    slow_print("  任务一：在小镇生存7天 —— 遵守'分贝规则'")
    slow_print("  任务二：找到失踪的居民 —— 他们去了哪里？")
    slow_print("  任务三：修复钟塔 —— 让时间恢复正常")
    print_line()
    slow_print("在你踏入小镇之前，请记住：")
    slow_print("白天可以说话，傍晚只能耳语，夜晚——完全安静。")
    slow_print("违反规则的话……你会遇到'声音警察'。")
    wait_enter()

    clock_parts = 0
    found_residents = 0
    alerted = False
    safe_house_locations = [
        "旧教堂的地下室",
        "图书馆的阁楼",
        "废弃邮局的仓库",
        "钟塔旁边的守夜人小屋"
    ]
    safe_house_index = 0
    has_diary = False
    tower_unlocked = False
    days_explored = set()
    last_action = None

    for day in range(1, 8):
        for phase in range(3):
            if not player.is_alive():
                break

            if phase == 2:
                dead = _night_choice(player, safe_house_locations[safe_house_index % len(safe_house_locations)])
                safe_house_index += 1
                if dead:
                    break
                continue

            _show_status(day, phase, player, clock_parts, found_residents, alerted)

            if phase == 0:
                if day not in days_explored:
                    days_explored.add(day)
                    slow_print(f"\n清晨的阳光勉强穿过雾气照进小镇。新的一天开始了。")

            time_names = ["白天", "傍晚"]
            print(f"\n现在是{time_names[phase]}。{_time_of_day(day, phase)['warning']}")

            if day == 1 and phase == 0:
                slow_print("\n你站在小镇的入口处。雾气在脚边流动，像某种活物。")
                slow_print("前方的街道空无一人，只有一盏路灯在白天还亮着。")
                print_menu("去向选择", [
                    ("1", "沿主街向前走"),
                    ("2", "进入街边的杂货店"),
                    ("3", "走向那座高高的钟塔"),
                    ("4", "观察周围环境")
                ])
                choice = get_choice()
                if choice == "1":
                    slow_print("你沿着主街向前走。街道两旁是紧闭的店铺和民居。")
                    slow_print("你注意到所有门牌号都是反着挂的。")
                    if random.random() < 0.6:
                        event = _random_event()
                        _handle_event(event, player)
                elif choice == "2":
                    _general_store(player)
                elif choice == "3":
                    clock_parts = _clock_tower(player, clock_parts)
                else:
                    slow_print("你仔细观察周围。雾气中有一些模糊的影子在移动。")
                    slow_print("你不确定那些是人还是别的什么东西。")
            else:
                event = _random_event()
                _handle_event(event, player)

            if clock_parts >= 3 and not tower_unlocked:
                slow_print("\n你已经收集了三个钟塔零件！")
                slow_print("也许现在是时候去修复钟塔了。")
                tower_unlocked = True

            if tower_unlocked and clock_parts >= 3:
                print_menu("", [
                    ("1", "前往钟塔修复它"),
                    ("2", "继续探索")
                ])
                choice = get_choice()
                if choice == "1":
                    result = _fix_tower(player, day, phase)
                    if result == "win":
                        return _dungeon_end(player, clock_parts, found_residents, day, True)
                    elif result == "alert":
                        alerted = True

            if phase == 1 and random.random() < 0.3:
                alerted = True
                slow_print("\n⚠️ 你听到远处传来了哨声。声音警察似乎注意到了什么动静。")

        if not player.is_alive():
            break

    if player.is_alive():
        return _dungeon_end(player, clock_parts, found_residents, 7, False)
    else:
        return _dungeon_end(player, clock_parts, found_residents, 0, False)


def _handle_event(event, player):
    print_header(event["title"])
    slow_print(event["desc"])
    print_event_menu(event["choices"])
    choice = get_event_choice(event["choices"])
    if choice == "talk":
        slow_print(event["result_talk"])
    elif choice == "leave":
        slow_print(event["result_leave"])
    elif choice == "search":
        slow_print(event["result_search"])
    elif choice == "read":
        slow_print(event["result_read"])
    elif choice == "open":
        slow_print(event["result_open"])
    elif choice == "note":
        slow_print(event["result_note"])
    wait_enter()


def _general_store(player):
    print_header("杂货店")
    slow_print("你推开杂货店的玻璃门。门上的铃铛发出清脆的响声。")
    slow_print("你立刻僵住了——声音太大了！")
    slow_print("但什么都没发生。店里空无一人。")
    print_line()
    slow_print("货架上还有一些东西。看起来是小镇居民匆忙撤离时留下的。")
    print_menu("", [
        ("1", "搜索货架"),
        ("2", "检查柜台后面的房间"),
        ("0", "离开")
    ])
    choice = get_choice()
    if choice == "1":
        slow_print("你在货架上找到了几样东西：")
        found_item = random.choice(["一包饼干", "一瓶水", "一把手电筒", "一盒火柴"])
        slow_print(f"一包看起来没过期的{found_item}。")
        slow_print("你在柜台下面还发现了一个旧式助听器。")
        player.add_item({
            "id": "hearing_aid",
            "name": "旧式助听器",
            "level": "E",
            "effect": "可以增强听力，在夜晚更容易察觉声音警察",
            "price": 0,
            "note": "上一个主人的听力可能不太好——这玩意儿音量调到最大也只能听到蚊子扇翅膀的声音。"
        })
        slow_print("获得道具：旧式助听器")
    elif choice == "2":
        slow_print("柜台后面是一个小房间。墙上贴满了照片和剪报。")
        slow_print("照片上的人都在笑。看起来很正常。")
        slow_print("但所有照片里，钟塔的指针都是反的。")
        slow_print("你在抽屉里找到了一张纸条：'镇长说一切都会好的。镇长说谎了。'")
    wait_enter()


def _clock_tower(player, parts):
    print_header("钟塔")
    slow_print("你走近钟塔。塔很高，顶端的大钟指针确实是反着走的。")
    slow_print("钟塔的大门虚掩着。")
    print_menu("", [
        ("1", "推门进去"),
        ("2", "绕着钟塔走一圈"),
        ("0", "离开")
    ])
    choice = get_choice()
    if choice == "1":
        slow_print("你推开门，走了进去。塔内很暗，空气中弥漫着灰尘和机油的味道。")
        slow_print("在楼梯下面，你发现了一个生锈的齿轮——看起来是从某个机器上掉下来的。")
        slow_print("\n获得：钟塔零件（1/3）")
        wait_enter()
        return parts + 1
    elif choice == "2":
        slow_print("你绕着钟塔走了一圈。在塔基的背面，你发现墙上刻着一些文字：")
        slow_print("'当指针归位，声音回归。'")
        slow_print("'当钟声响起，沉默终结。'")
        slow_print("下面还有一行小字：'但别让警察听见。——老K'")
        wait_enter()
        return parts
    return parts


def _fix_tower(player, day, phase):
    print_header("修复钟塔")
    slow_print("你带着收集到的零件来到钟塔内部。")
    slow_print("登上旋转楼梯，你来到了钟塔的机械室。")
    slow_print("巨大的齿轮组在你的面前展开，其中几个齿轮已经脱落。")
    print_line()
    slow_print("你需要决定如何修复……")
    print_menu("", [
        ("1", "按照机械原理小心安装（安全但耗时）"),
        ("2", "用力把零件塞进去（快速但可能发出噪音）")
    ])
    choice = get_choice()
    if choice == "1":
        slow_print("你小心翼翼地将齿轮一一复位。")
        slow_print("钟塔的指针开始缓慢地倒转……然后恢复正常。")
        slow_print("一声洪亮的钟声响起——")
        slow_print("那是这个小镇三十年来第一次听到真正的声音。")
        slow_print("\n小镇的雾气开始消散。失踪的居民从各个角落出现。")
        slow_print("他们看起来都很困惑，但都还活着。")
        return "win"
    else:
        slow_print("你用蛮力把齿轮塞了进去。巨大的金属撞击声回荡在整个小镇！")
        slow_print("指针确实开始恢复正常了……但你听到了急促的脚步声。")
        slow_print("很多脚步声。正在向钟塔靠近。")
        slow_print("⚠️ 声音警察来了！")
        return "alert"


def _dungeon_end(player, clock_parts, found_residents, day, fixed_tower):
    print_header("副本结算", "分贝小镇")

    if not player.is_alive():
        slow_print("\n你在分贝小镇倒下了。")
        slow_print("意识模糊中，你感觉自己被拖进了某个黑暗的地方……")
        slow_print("\n评级：E级 — 死亡")
        score = 10
        reward = 0
    elif fixed_tower:
        slow_print("\n钟声响起，小镇恢复了正常。")
        slow_print("失踪的居民们从藏身之处走出来，困惑但安全。")
        slow_print("一个老人——你之前见过的那个——走过来拍了拍你的肩膀。")
        slow_print("'谢谢你。你是第一个修好钟塔的人。'")
        print_line()
        if clock_parts >= 3:
            slow_print("评级：S级 — 完美通关！")
            slow_print("你修复了钟塔，拯救了小镇，还发现了背后的秘密。")
            score = 300
            reward = 200
        else:
            slow_print("评级：A级 — 任务完成")
            slow_print("钟塔修好了，但还有一些谜题你没有解开。")
            score = 200
            reward = 150
    elif day >= 7:
        slow_print("\n七天的期限到了。")
        slow_print("你虽然没有完全解开小镇的秘密，但你活了下来。")
        slow_print("深渊列车在站台等你。你回头看了一眼这个安静的小镇。")
        print_line()
        if clock_parts >= 2:
            slow_print("评级：B级 — 部分探索")
            score = 100
            reward = 80
        else:
            slow_print("评级：C级 — 勉强生存")
            score = 60
            reward = 40
    else:
        slow_print(f"你在第{day}天就被小镇打败了……")
        slow_print("评级：D级 — 失败")
        score = 20
        reward = 10

    print_line()
    slow_print(f"  基础奖励：{reward} 白钞")
    slow_print(f"  额外积分：{score}")
    print_line()

    player.white_bills += reward
    player.dungeon_count += 1
    player.total_score += score

    evo_gain = score // 50
    if evo_gain > 0:
        player.evolution_rate = min(100, player.evolution_rate + evo_gain)
        slow_print(f"  进化率提升：+{evo_gain}%")

    if score >= 200:
        special_item = "evol_p0"
        from data.items import get_item
        item = get_item(special_item)
        if item:
            player.add_item(item)
            slow_print(f"  获得特殊奖励：{item['name']}")

    wait_enter()
    return "alive" if player.is_alive() else "dead"