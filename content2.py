# -*- coding: utf-8 -*-
"""
Ново съдържание към СпасиДете.БГ / additional content for СпасиДете.БГ

Източник: „Съдържание_Spasidete.bg.docx“ (МВР) и публичните страници за контакт
на областните дирекции на МВР (mvr.bg/<област>/bg/contacts), проверени 01.10.2026 г.

Source: the Ministry of Interior content document and the published contact pages of
the regional directorates (mvr.bg/<region>/bg/contacts), checked on 1 October 2026.
"""

# ==========================================================================
#  Областни дирекции на МВР / regional directorates
#  (име_bg, име_en, slug, телефон, етикет на телефона, имейл, адрес)
# ==========================================================================

ODMVR = [
    ("Благоевград", "Blagoevgrad", "blagoevgrad", "073 867 676", "централа", "централа", "blagoevgrad@mvr.bg",
     "ул. „Владо Черноземски“ № 3, 2700 Благоевград"),
    ("Бургас", "Burgas", "burgas", "056 856 555", "гореща линия / ОДЧ", "hotline / duty unit", "",
     "ул. „Христо Ботев“ № 46, Бургас"),
    ("Варна", "Varna", "varna", "052 615 166", "дежурна част", "duty unit", "varna@mvr.bg",
     "ул. „Цар Калоян“ № 2, Варна"),
    ("Велико Търново", "Veliko Tarnovo", "veliko-tarnovo", "062 662 662", "централа", "централа", "veliko-tarnovo@mvr.bg",
     "ул. „Бачо Киро“ № 7, Велико Търново"),
    ("Видин", "Vidin", "vidin", "094 600 014", "централа", "централа", "vidin@mvr.bg",
     "ул. „Цар Симеон Велики“ № 87, 3700 Видин"),
    ("Враца", "Vratsa", "vratza", "092 692 318", "оперативна дежурна част", "duty unit", "odc.vratza@mvr.bg",
     "ул. „Поп Косто Буюклийски“ № 10, 3000 Враца"),
    ("Габрово", "Gabrovo", "gabrovo", "066 800 860", "централа, денонощно", "switchboard, 24/7", "gabrovo@mvr.bg",
     "ул. „Орловска“ № 50, 5300 Габрово"),
    ("Добрич", "Dobrich", "dobrich", "058 658 058", "централа", "централа", "dobrich@mvr.bg",
     "ул. „Максим Горки“ № 12, 9300 Добрич"),
    ("Кърджали", "Kardzhali", "kardjali", "0361 6 96 99", "централа", "централа", "kardjali@mvr.bg",
     "бул. „България“ № 39, 6600 Кърджали"),
    ("Кюстендил", "Kyustendil", "kustendil", "078 557 323", "дежурна част", "duty unit", "ODMVR_KN@mvr.bg",
     "ул. „Цар Освободител“ № 12, 2500 Кюстендил"),
    ("Ловеч", "Lovech", "lovech", "068 601 112", "централа", "централа", "lovech@mvr.bg",
     "ул. „Стефан Караджа“ № 2, 5500 Ловеч"),
    ("Монтана", "Montana", "montana", "096 396 396", "денонощна линия", "24/7 line", "montana@mvr.bg",
     "бул. „Александър Стамболийски“ № 2, 3400 Монтана"),
    ("Пазарджик", "Pazardzhik", "pazardjik", "034 434 400", "дежурен РУ Пазарджик", "duty officer", "pazardzhik@mvr.bg",
     "пл. „Съединение“ № 3, 4400 Пазарджик"),
    ("Перник", "Pernik", "pernik", "076 676 376", "оперативна дежурна част", "duty unit", "pernik@mvr.bg",
     "ул. „Самоков“ № 1, 2300 Перник"),
    ("Плевен", "Pleven", "pleven", "064 864 323", "дежурен ОДМВР", "duty officer", "pleven@mvr.bg",
     "ул. „Сан Стефано“ № 3, 5800 Плевен"),
    ("Пловдив", "Plovdiv", "plovdiv", "", "", "", "odmvr_plovdiv@mvr.bg",
     "ул. „Княз Богориди“ № 7, Пловдив"),
    ("Разград", "Razgrad", "razgrad", "084 684 200", "централа", "централа", "od_razgrad@mvr.bg",
     "ул. „Кирил и Методий“ № 8, 7200 Разград"),
    ("Русе", "Ruse", "ruse", "", "", "", "odmvrruse@mvr.bg",
     "бул. „Скобелев“ № 49, 7000 Русе"),
    ("Силистра", "Silistra", "silistra", "0868 86 286", "номератор", "switchboard", "silistra@mvr.bg",
     "бул. „Македония“ № 144, Силистра"),
    ("Сливен", "Sliven", "sliven", "044 644 644", "централа", "централа", "sliven@mvr.bg",
     "ул. „Ген. Скобелев“ № 5, 8800 Сливен"),
    ("Смолян", "Smolyan", "smolyan", "0301 35 323", "дежурен ОДМВР", "duty officer", "smolyan@mvr.bg",
     "бул. „България“ № 67, 4700 Смолян"),
    ("София-град (СДВР)", "Sofia city (SDVR)", "sdvr", "02 987 77 77", "дежурен център", "duty centre", "sdvr@mvr.bg",
     "ул. „Антим I“ № 5, 1303 София"),
    ("София-област", "Sofia region", "sofia", "02 873 99 45", "ОДЧ", "duty unit", "odmvr-sofia@mvr.bg",
     "бул. „Гео Милев“ № 71, 1574 София"),
    ("Стара Загора", "Stara Zagora", "stara-zagora", "042 602 805", "централа", "централа", "stara_zagora@mvr.bg",
     "ул. „Граф Игнатиев“ № 16, Стара Загора"),
    ("Търговище", "Targovishte", "targovishte", "0601 63 797", "дежурна част", "duty unit", "targovishte@mvr.bg",
     "ул. „Спиридон Грамадов“ № 36, 7700 Търговище"),
    ("Хасково", "Haskovo", "haskovo", "038 640 640", "централа", "централа", "haskovo@mvr.bg",
     "бул. „България“ № 85, 6300 Хасково"),
    ("Шумен", "Shumen", "shumen", "054 800 588", "дежурен ОДМВР", "duty officer", "shumen@mvr.bg",
     "ул. „Сан Стефано“ № 2, Шумен"),
    ("Ямбол", "Yambol", "yambol", "046 680 680", "централа", "централа", "yambol@mvr.bg",
     "ул. „Преслав“ № 40, Ямбол"),
]

# Резервен адрес, когато дирекцията не публикува обща електронна поща.
# Fallback address when a directorate publishes no general e-mail.
FALLBACK_EMAIL = "priemna@mvr.bg"

# ==========================================================================
#  Други канали за сигнал / other reporting channels
# ==========================================================================

OTHER_CHANNELS = [
    ("Районните полицейски управления по места",
     "Local district police departments",
     "Най-близкото РУ приема сигнал на място и по телефон. Телефоните са публикувани на страницата за контакт на съответната областна дирекция.",
     "The nearest district department takes reports in person and by phone. Numbers are published on each regional directorate’s contact page."),
    ("Прокуратура на Република България",
     "Prosecutor’s Office of the Republic of Bulgaria",
     "Сигнал може да се подаде в районната прокуратура по местоживеене или по местоизвършване на деянието.",
     "A report can be filed with the district prosecutor’s office where you live or where the act took place."),
    ("Отдели „Закрила на детето“ към Агенцията за социално подпомагане",
     "Child Protection Departments at the Social Assistance Agency",
     "Местната социална служба оценява риска за детето и осигурява подкрепа за него и за семейството му.",
     "The local social service assesses the risk to the child and arranges support for the child and the family."),
    ("Национална система 112",
     "112 — national emergency number",
     "При непосредствена опасност за живота или здравето на дете. Денонощно, безплатно, от всеки телефон.",
     "When a child’s life or health is in immediate danger. Round the clock, free, from any phone."),
]

# ==========================================================================
#  Материали: „Агресия и насилие“ / materials
# ==========================================================================

MATERIALS = [
    {
        "id": "m1-vidove",
        "num": "1",
        "title_bg": "Видовете насилие сред подрастващите в България",
        "title_en": "The forms of violence among adolescents in Bulgaria",
        "lead_bg": "В България подрастващите най-често преживяват и проявяват емоционално (психическо) насилие, следвано от физическа агресия и кибертормоз. Изследванията показват, че всяко второ дете (47%) в страната е преживяло някаква форма на насилие до 18-годишна възраст.",
        "lead_en": "In Bulgaria adolescents most often experience and display emotional (psychological) violence, followed by physical aggression and cyberbullying. Research shows that every second child (47%) in the country has experienced some form of violence before the age of 18.",
        "blocks": [
            {
                "h_bg": "1. Емоционално (психическо) насилие и тормоз",
                "h_en": "1. Emotional (psychological) violence and bullying",
                "body_bg": [
                    "Това е най-разпространената форма, която подрастващите проявяват помежду си или приемат от средата. Включва обиди, социално изключване, злепоставяне, разпространение на слухове и заплахи.",
                    "<strong>Статистика:</strong> според представителното национално изследване на УНИЦЕФ, емоционалното насилие засяга 45,9% от децата в България.",
                    "<strong>Къде:</strong> училището е основното място на проява — данните на PISA показват, че между 20% от момичетата и 24% от момчетата в България са подложени на системен училищен тормоз поне няколко пъти месечно.",
                ],
                "body_en": [
                    "This is the most widespread form, which adolescents display towards each other or absorb from their environment. It includes insults, social exclusion, discrediting, the spreading of rumours and threats.",
                    "<strong>Figures:</strong> according to the nationally representative UNICEF study, emotional violence affects 45.9% of children in Bulgaria.",
                    "<strong>Where:</strong> school is the main setting — PISA data show that between 20% of girls and 24% of boys in Bulgaria are subjected to systematic school bullying at least several times a month.",
                ],
            },
            {
                "h_bg": "2. Физическо насилие",
                "h_en": "2. Physical violence",
                "body_bg": [
                    "Проявява се чрез блъскане, удряне, сбивания и физическа саморазправа — често записвани с телефон и разпространявани в мрежите заради статус.",
                    "<strong>Статистика:</strong> заема второ място с 31,2% разпространение сред подрастващите.",
                    "<strong>Тенденция:</strong> мониторинговите доклади на Държавната агенция за закрила на детето отчитат устойчив ръст на сигналите за физическа агресия сред непълнолетните през последните години.",
                ],
                "body_en": [
                    "It shows up as pushing, hitting, fights and physical retaliation — often recorded on a phone and shared on social networks for status.",
                    "<strong>Figures:</strong> second most common, at 31.2% prevalence among adolescents.",
                    "<strong>Trend:</strong> the monitoring reports of the State Agency for Child Protection record a steady rise in reports of physical aggression among minors in recent years.",
                ],
            },
            {
                "h_bg": "3. Кибернасилие (онлайн тормоз)",
                "h_en": "3. Cyber violence (online bullying)",
                "body_bg": [
                    "Дигиталното пространство е основен проводник на тийнейджърската агресия. Изразява се в кибербулинг, обидни коментари, създаване на фалшиви профили за унижение на връстници и изнудване със снимки.",
                    "<strong>Статистика:</strong> според данните на УНИЦЕФ едно на всеки седем деца (около 14%) в България съобщава, че е било обект на онлайн тормоз, предимно в социалните мрежи.",
                ],
                "body_en": [
                    "The digital space is a principal conduit for teenage aggression. It takes the form of cyberbullying, abusive comments, fake profiles created to humiliate peers, and extortion with images.",
                    "<strong>Figures:</strong> according to UNICEF, one in seven children (about 14%) in Bulgaria reports having been subjected to online bullying, mostly on social networks.",
                ],
            },
            {
                "h_bg": "4. Насилие, основано на пола, и ранен сексуален тормоз",
                "h_en": "4. Gender-based violence and early sexual harassment",
                "body_bg": [
                    "В по-горната тийнейджърска възраст (15–19 години) започват да се проявяват модели на токсичен контрол в интимните връзки.",
                    "<strong>Статистика:</strong> данните на Националния статистически институт от изследването EU-GBV показват, че младите жени на възраст 18–29 години са изложени на най-висок риск от физическо и психическо насилие от интимен партньор, а корените на тези поведенчески модели се формират именно в юношеството. Сериозен процент от подрастващите съобщават и за преживян нежелан сексуален натиск или тормоз под различни форми.",
                ],
                "body_en": [
                    "In later adolescence (15–19) patterns of toxic control in intimate relationships begin to appear.",
                    "<strong>Figures:</strong> National Statistical Institute data from the EU-GBV survey show that young women aged 18–29 face the highest risk of physical and psychological violence from an intimate partner, and that the roots of these behavioural patterns are formed in adolescence. A significant share of adolescents also report unwanted sexual pressure or harassment in various forms.",
                ],
            },
        ],
        "sources_bg": [
            "<strong>УНИЦЕФ България</strong> — национално представително проучване „Изследване на насилието над деца в България“, проведено от Coram International и ЕСТАТ.",
            "<strong>Национален статистически институт</strong> — данни и методология от изследването за насилието, основано на пол (EU-GBV).",
            "<strong>Държавна агенция за закрила на детето</strong> — годишни мониторингови доклади за насилието над децата и регистър на сигналите.",
            "<strong>PISA (ОИСР)</strong> — данни за тормоза в училищна среда и сигурността на учениците в България.",
        ],
        "sources_en": [
            "<strong>UNICEF Bulgaria</strong> — the nationally representative study “Research on violence against children in Bulgaria”, carried out by Coram International and ESTAT.",
            "<strong>National Statistical Institute</strong> — data and methodology from the gender-based violence survey (EU-GBV).",
            "<strong>State Agency for Child Protection</strong> — annual monitoring reports on violence against children and the register of reports.",
            "<strong>PISA (OECD)</strong> — data on bullying in schools and pupil safety in Bulgaria.",
        ],
    },
    {
        "id": "m2-cenata",
        "num": "2",
        "title_bg": "Цената на непълноценната грижа",
        "title_en": "The price of inadequate care",
        "lead_bg": "Липса на привързаност, свръхконтрол, липса на качествено общуване с родителите, неглижиране, презадоволяване, отсъстващи родители, „интернет възпитание“ — всяко от тях оставя следа.",
        "lead_en": "A lack of attachment, over-control, the absence of real conversation with parents, neglect, over-indulgence, absent parents, “upbringing by internet” — each of these leaves a mark.",
        "blocks": [
            {
                "h_bg": "Агресия и насилие — къде е границата",
                "h_en": "Aggression and violence — where the line falls",
                "body_bg": [
                    "Под „агресия“ се разбира съвкупност от действия и постъпки, които нарушават физическата или психическата цялостност на друг човек или група от хора. Агресивното поведение се свързва с нанасяне на материални вреди, физическа болка, словесни обиди, възпрепятстване на желанията и противодействие на интересите на другите.",
                    "Резултатът от поведението е водещ при определянето на агресивността. Така <strong>насилието</strong> може да се определи като вид агресия, която се проявява под различни форми на причиняване на страдание, болка и тормоз спрямо други хора.",
                ],
                "body_en": [
                    "“Aggression” means the set of acts that violate the physical or psychological integrity of another person or group. Aggressive behaviour is associated with material damage, physical pain, verbal insults, the thwarting of others’ wishes and opposition to their interests.",
                    "It is the outcome of the behaviour that defines aggressiveness. <strong>Violence</strong> can therefore be defined as a kind of aggression that appears in various forms of inflicting suffering, pain and torment on other people.",
                ],
            },
            {
                "h_bg": "Основни форми на насилие",
                "h_en": "The basic forms of violence",
                "list_bg": [
                    "<strong>Физическо:</strong> всяко умишлено използване на физическа сила, което води до болка, нараняване, телесна повреда или смърт — удряне, блъскане, скубане, душене, лишаване от свобода на движение.",
                    "<strong>Психическо (емоционално):</strong> системно вербално или невербално въздействие, което уврежда самооценката и психическото здраве — обиди, унижения, заплахи, изолация, крайна ревност, манипулация, газлайтинг.",
                    "<strong>Сексуално:</strong> всяко сексуално действие, опит за такова или принуда към сексуални прояви без изрично и свободно дадено съгласие — нежелано докосване, сексуален тормоз, изнасилване, принуда към гледане или заснемане на порнографски материали.",
                    "<strong>Икономическо:</strong> поставяне на жертвата в пълна финансова зависимост и/или контрол над нейните ресурси — отнемане на лични доходи, забрана за работа или учене, отказ от средства за основни нужди като храна и лекарства.",
                ],
                "list_en": [
                    "<strong>Physical:</strong> any deliberate use of physical force that causes pain, injury, bodily harm or death — hitting, pushing, hair-pulling, strangling, restricting freedom of movement.",
                    "<strong>Psychological (emotional):</strong> systematic verbal or non-verbal pressure that damages self-esteem and mental health — insults, humiliation, threats, isolation, extreme jealousy, manipulation, gaslighting.",
                    "<strong>Sexual:</strong> any sexual act, attempted act or coercion into sexual behaviour without explicit and freely given consent — unwanted touching, sexual harassment, rape, coercion into watching or filming pornographic material.",
                    "<strong>Economic:</strong> placing the victim in complete financial dependence and/or controlling their resources — taking their income, forbidding work or study, refusing money for basic needs such as food and medicine.",
                ],
            },
            {
                "h_bg": "Форми според средата и контекста",
                "h_en": "Forms by setting and context",
                "list_bg": [
                    "<strong>Домашно насилие:</strong> всеки акт на физическо, сексуално, психическо или икономическо насилие в рамките на семейството, домакинството или между бивши и настоящи партньори.",
                    "<strong>Училищен тормоз (булинг):</strong> системна агресия — физическа, вербална или социална — между ученици в образователна среда.",
                    "<strong>Кибернасилие:</strong> използване на дигитални технологии и социални мрежи за злепоставяне, обиди, заплахи, разпространение на снимки, слухове или изнудване.",
                    "<strong>Насилие на работното място (мобинг):</strong> системен психологически тормоз от колеги или ръководители с цел дискредитиране или принуда служителят да напусне.",
                ],
                "list_en": [
                    "<strong>Domestic violence:</strong> any act of physical, sexual, psychological or economic violence within the family, the household or between former and current partners.",
                    "<strong>School bullying:</strong> systematic aggression — physical, verbal or social — between pupils in an educational setting.",
                    "<strong>Cyber violence:</strong> using digital technology and social networks to discredit, insult, threaten, spread images or rumours, or to extort.",
                    "<strong>Workplace violence (mobbing):</strong> systematic psychological harassment by colleagues or managers aimed at discrediting an employee or forcing them to leave.",
                ],
            },
            {
                "h_bg": "Специфични и структурни форми",
                "h_en": "Specific and structural forms",
                "list_bg": [
                    "<strong>Насилие чрез неглижиране:</strong> системно, хронично незадоволяване на основните нужди на зависимо лице — дете, възрастен или болен човек — лишаване от храна, медицински грижи, образование, сигурност и емоционална подкрепа.",
                    "<strong>Насилие, основано на пола:</strong> насилие, насочено срещу лице заради неговия пол или засягащо непропорционално лица от определен пол.",
                    "<strong>Институционално насилие:</strong> тормоз, лошо отношение или системно лишаване от права на хора, настанени в институции.",
                    "<strong>Трафик на хора:</strong> набиране, транспортиране и укриване на хора чрез принуда и измама с цел експлоатация — трудова, сексуална или за отнемане на органи.",
                ],
                "list_en": [
                    "<strong>Violence through neglect:</strong> the systematic, chronic failure to meet the basic needs of a dependent person — a child, an elderly or a sick person — depriving them of food, medical care, education, safety and emotional support.",
                    "<strong>Gender-based violence:</strong> violence directed at a person because of their gender, or which disproportionately affects people of a particular gender.",
                    "<strong>Institutional violence:</strong> harassment, mistreatment or the systematic denial of rights to people placed in institutions.",
                    "<strong>Human trafficking:</strong> recruiting, transporting and concealing people through coercion and deception for the purpose of exploitation — labour, sexual, or for the removal of organs.",
                ],
            },
        ],
        "closing_bg": "Агресията, проявявана от подрастващите, почти никога не е просто „лош характер“ — тя е видимият симптом на по-дълбок вътрешен или външен проблем. Психолозите я разглеждат като силен сигнал за помощ, като неспособност за справяне със средата или като знак за емоционален дефицит.",
        "closing_en": "Aggression displayed by adolescents is almost never simply “a bad character” — it is the visible symptom of a deeper internal or external problem. Psychologists view it as a strong call for help, an inability to cope with the environment, or a sign of emotional deficit.",
    },
    {
        "id": "m3-poslaniya",
        "num": "3",
        "title_bg": "Посланията, които младите хора отправят",
        "title_en": "The messages young people are sending",
        "lead_bg": "Зад едно и също поведение могат да стоят много различни причини. Ето трите, които психолозите срещат най-често.",
        "lead_en": "The same behaviour can have very different causes behind it. These are the three psychologists encounter most often.",
        "blocks": [
            {
                "h_bg": "1. Зов за внимание",
                "h_en": "1. A call for attention",
                "body_bg": [
                    "<strong>Неосъзнат вик за помощ.</strong> Често агресивното поведение е сигнал за затруднения в семейството. Някои тийнейджъри, когато се чувстват невидими или неразбрани, „избират“ — несъзнавано — скандала или физическата проява, защото това гарантира, че възрастните най-накрая ще ги забележат.",
                    "<strong>Огледален модел.</strong> Агресията може да е знак, че самото дете е жертва на тормоз — в училище или у дома. Детето копира модела на поведение, на който е подложено: от една страна подражава на насилника, който е „всесилен“, а от друга се освобождава от натрупаните емоции, защото не може да отвърне на своя насилник — особено ако той е родител.",
                ],
                "body_en": [
                    "<strong>An unrecognised cry for help.</strong> Aggressive behaviour is often a signal of difficulties at home. Some teenagers, when they feel invisible or misunderstood, unconsciously “choose” a row or a physical outburst, because that guarantees adults will finally notice them.",
                    "<strong>A mirrored pattern.</strong> Aggression can be a sign that the child is itself a victim of abuse — at school or at home. The child copies the behaviour it is subjected to: on one hand imitating the abuser, who appears all-powerful, on the other releasing accumulated emotion, because it cannot answer its own abuser — especially if that is a parent.",
                ],
            },
            {
                "h_bg": "2. Хормонална и емоционална буря",
                "h_en": "2. A hormonal and emotional storm",
                "body_bg": [
                    "<strong>Липса на емоционална регулация.</strong> Юношеството е период на интензивни физиологични промени. Агресията сигнализира, че нервната система на подрастващия е претоварена — той все още няма зрели механизми да изразява страха, тревожността или гнева си по здравословен начин, а вероятно няма и емоционално здрав възрастен за пример около себе си.",
                    "<strong>Маскирана депресия.</strong> При възрастните депресията често се проявява с тъга и изолиране. При подрастващите обаче скритата депресия и високите нива на тревожност много често се маскират като раздразнителност, враждебност и изблици на ярост.",
                ],
                "body_en": [
                    "<strong>No emotional regulation yet.</strong> Adolescence is a period of intense physiological change. Aggression signals that the young person’s nervous system is overloaded — they do not yet have mature mechanisms for expressing fear, anxiety or anger in a healthy way, and quite possibly have no emotionally healthy adult around them to model it.",
                    "<strong>Masked depression.</strong> In adults, depression often shows as sadness and withdrawal. In adolescents, hidden depression and high anxiety very often present as irritability, hostility and outbursts of rage.",
                ],
            },
            {
                "h_bg": "3. Социален натиск и търсене на идентичност",
                "h_en": "3. Social pressure and the search for identity",
                "body_bg": [
                    "<strong>Статус и лидерство.</strong> В тази възраст мнението на връстниците е по-важно от това на родителите. Агресията може да е опит за приемане, за доказване, за издигане в йерархията на групата или страх от социално изключване. Често такава група — формирана основно от „сърдити и гневни“ подрастващи — замества значими липси в семейната среда: липса на емоционална връзка с родител, занижен родителски капацитет, насилие в семейството, прекалено обгрижване, възпитание чрез контрол и подчиненост или свръхидеализация на способностите на детето.",
                    "<strong>Проверка на границите.</strong> Подрастващите умишлено провокират средата, за да тестват докъде се простира тяхната автономия и къде се чупят правилата на възрастните.",
                ],
                "body_en": [
                    "<strong>Status and leadership.</strong> At this age the opinion of peers matters more than that of parents. Aggression can be an attempt to be accepted, to prove oneself, to rise in the group’s hierarchy, or fear of being excluded. Often such a group — made up largely of angry adolescents — substitutes for significant gaps at home: no emotional bond with a parent, reduced parental capacity, violence in the family, excessive protection, an upbringing built on control and submission, or the over-idealisation of the child’s abilities.",
                    "<strong>Testing the boundaries.</strong> Adolescents deliberately provoke their environment to test how far their autonomy reaches and where the adults’ rules break.",
                ],
            },
        ],
        "warn_bg": "Повечето психолози отбелязват, че пълната липса на конфликти и прекалено „безупречното“ поведение също изискват внимание. Такова поведение може да е сигнал за силно потисната агресия, която рискува да се превърне в автоагресия, в тревожно или друг вид разстройство.",
        "warn_en": "Most psychologists note that a complete absence of conflict and unusually “flawless” behaviour also deserve attention. Such behaviour can signal strongly suppressed aggression, which risks turning inward into self-harm, anxiety or another disorder.",
    },
    {
        "id": "m4-ot-agresiya",
        "num": "4",
        "title_bg": "От агресия към насилие",
        "title_en": "From aggression to violence",
        "lead_bg": "При подрастващите насилието е крайна форма на агресия и ясен знак, че вътрешните или външните проблеми на детето вече са преминали критичния праг на поносимост.",
        "lead_en": "In adolescents, violence is the extreme form of aggression and a clear sign that the child’s internal or external problems have crossed the critical threshold of what it can bear.",
        "blocks": [
            {
                "h_bg": "1. Знак за травма или преживяно насилие",
                "h_en": "1. A sign of trauma or violence suffered",
                "body_bg": [
                    "<strong>Преживян тормоз.</strong> В огромен процент от случаите подрастващите, които упражняват насилие, самите те са били или в момента са жертви на един или на множество видове насилие у дома или в близката си среда. За някои жертви насилието е деструктивен начин да си върнат усещането за контрол и сила.",
                    "<strong>Травма от отхвърляне.</strong> Проявата на жестокост може да е реакция на тежко емоционално отхвърляне от родителите, на разпад на семейството или на болезнено изключване от групата на връстниците.",
                ],
                "body_en": [
                    "<strong>Abuse suffered.</strong> In a very large share of cases, adolescents who use violence have themselves been, or still are, victims of one or many kinds of violence at home or close to it. For some victims, violence is a destructive way of regaining a sense of control and strength.",
                    "<strong>The trauma of rejection.</strong> Cruelty can be a reaction to severe emotional rejection by parents, to a family breaking up, or to painful exclusion from the peer group.",
                ],
            },
            {
                "h_bg": "2. Знак за психологически и емоционални разстройства",
                "h_en": "2. A sign of psychological and emotional disorders",
                "body_bg": [
                    "<strong>Разстройство на поведението.</strong> Когато насилието е насочено към хора или животни и е придружено от разрушаване на имущество или кражби, това е знак за поведенческо разстройство, което изисква намесата на клиничен психолог или психиатър.",
                    "<strong>Липса на емпатия.</strong> Насилието показва сериозен дефицит в развитието на емпатия — детето не може да се постави на мястото на жертвата и да изпита състрадание. Състоянието има различни причини, но се нуждае от намесата на детски специалист.",
                    "<strong>Хронично висок стрес и тревожност.</strong> Когато тийнейджърът живее в постоянна среда на стрес, нервната му система е в режим „борба или бягство“. Насилието е знак за неконтролируем взрив на натрупано вътрешно напрежение.",
                ],
                "body_en": [
                    "<strong>Conduct disorder.</strong> When violence is directed at people or animals and is accompanied by the destruction of property or by theft, this is a sign of a behavioural disorder that calls for a clinical psychologist or psychiatrist.",
                    "<strong>An absence of empathy.</strong> Violence reveals a serious deficit in the development of empathy — the child cannot put itself in the victim’s place and feel compassion. The condition has various causes, but it needs a specialist in child care.",
                    "<strong>Chronically high stress and anxiety.</strong> When a teenager lives in a constant environment of stress, their nervous system is in “fight or flight”. Violence is a sign of an uncontrolled discharge of accumulated internal tension.",
                ],
            },
            {
                "h_bg": "3. Знак за социална и системна дисфункция",
                "h_en": "3. A sign of social and systemic dysfunction",
                "body_bg": [
                    "<strong>Влияние на токсична субкултура.</strong> Насилието често е знак за силен натиск от улични компании, банди или онлайн общности. За да бъде приет и да спечели статус на „лидер“, подрастващият прекрачва моралните граници.",
                    "<strong>Липса на здрави граници в семейството.</strong> Поведението е знак, че у дома липсват ясни правила, авторитет и последствия — или обратното: възпитанието е изградено върху краен диктат, който предизвиква мощен бунт.",
                ],
                "body_en": [
                    "<strong>The pull of a toxic subculture.</strong> Violence is often a sign of strong pressure from street groups, gangs or online communities. To be accepted and gain the status of a “leader”, the adolescent crosses moral lines.",
                    "<strong>No healthy boundaries at home.</strong> The behaviour signals that clear rules, authority and consequences are missing at home — or the opposite: an upbringing built on extreme dictate, which provokes a powerful revolt.",
                ],
            },
        ],
    },
    {
        "id": "m5-skriti-priznaci",
        "num": "5",
        "title_bg": "Скрити признаци и поведенчески прояви на агресия",
        "title_en": "Hidden signs and behavioural expressions of aggression",
        "lead_bg": "Агресивните импулси при подрастващите често са резултат от интензивни хормонални промени, емоционално пренапрежение и стремеж към себеутвърждаване. Проявите им обаче варират от явни физически действия до скрити, индиректни или психологически симптоми.",
        "lead_en": "Aggressive impulses in adolescents often follow from intense hormonal change, emotional overload and a drive for self-assertion. The way they show, however, ranges from open physical acts to hidden, indirect or psychological symptoms.",
        "blocks": [
            {
                "h_bg": "Поведенчески прояви",
                "h_en": "Behavioural signs",
                "list_bg": [
                    "<strong>Вербална агресия:</strong> чести викове, обиди, заплахи към членове на семейството, учители или връстници.",
                    "<strong>Физическа агресия:</strong> налитане на бой, блъскане, ритане или чупене на предмети с цел „изпускане на парата“.",
                    "<strong>Индиректна агресия и тормоз:</strong> разпространение на слухове, злонамерени инсинуации, ирония, подигравки и съзнателно социално изолиране на конкретни връстници.",
                    "<strong>Автоагресия (самонараняване):</strong> насочване на агресивния импулс навътре — рязане, горене на кожата, силно гризане на ноктите или чоплене на рани.",
                ],
                "list_en": [
                    "<strong>Verbal aggression:</strong> frequent shouting, insults and threats towards family members, teachers or peers.",
                    "<strong>Physical aggression:</strong> starting fights, pushing, kicking or breaking things to “let off steam”.",
                    "<strong>Indirect aggression and bullying:</strong> spreading rumours, malicious insinuation, sarcasm, mockery and the deliberate social isolation of particular peers.",
                    "<strong>Self-directed aggression:</strong> turning the aggressive impulse inward — cutting, burning the skin, severe nail-biting or picking at wounds.",
                ],
            },
            {
                "h_bg": "Психо-емоционални признаци",
                "h_en": "Psycho-emotional signs",
                "list_bg": [
                    "<strong>Внезапни изблици на гняв:</strong> прекомерна и яростна реакция на дребни или незначителни поводи — нарушен импулсен контрол.",
                    "<strong>Обвиняване на околните:</strong> липса на поемане на отговорност; тийнейджърът твърди, че другите са виновни за поведението му или че съзнателно го провокират.",
                    "<strong>Хронична раздразнителност и фрустрация:</strong> постоянно чувство на недоволство от себе си и от околния свят.",
                ],
                "list_en": [
                    "<strong>Sudden outbursts of anger:</strong> an excessive, furious reaction to small or trivial triggers — impaired impulse control.",
                    "<strong>Blaming everyone else:</strong> no acceptance of responsibility; the teenager insists others are to blame for their behaviour or are deliberately provoking them.",
                    "<strong>Chronic irritability and frustration:</strong> a constant sense of dissatisfaction with themselves and with the world around them.",
                ],
            },
            {
                "h_bg": "Физиологични и скрити симптоми",
                "h_en": "Physiological and hidden symptoms",
                "list_bg": [
                    "<strong>Проблеми със съня:</strong> трудно заспиване, неспокоен сън, кошмари или необичайна сънливост поради натрупано напрежение.",
                    "<strong>Нервни тикове:</strong> физически прояви на потиснат емоционален стрес и тревожност.",
                    "<strong>Безразсъдно поведение:</strong> склонност към високорискови дейности — злоупотреба с алкохол или вещества, опасно шофиране, кражби.",
                    "<strong>Рязка промяна във външния вид:</strong> крайни модификации или умишлено провокативен вид, които понякога сигнализират вътрешен бунт и саморазрушителни тенденции.",
                ],
                "list_en": [
                    "<strong>Sleep problems:</strong> difficulty falling asleep, restless sleep, nightmares or unusual sleepiness from accumulated tension.",
                    "<strong>Nervous tics:</strong> physical expressions of suppressed emotional stress and anxiety.",
                    "<strong>Reckless behaviour:</strong> a pull towards high-risk activity — alcohol or substance abuse, dangerous driving, theft.",
                    "<strong>An abrupt change in appearance:</strong> extreme modifications or a deliberately provocative look, which sometimes signal inner revolt and self-destructive tendencies.",
                ],
            },
        ],
    },
]

# ==========================================================================
#  Съвети към гражданите / advice for citizens
# ==========================================================================

CITIZENS_INTRO_BG = (
    "Всеки от нас е виждал група тийнейджъри да обграждат по-малко дете в мола или в парка, "
    "или да се блъскат агресивно в автобуса и на спирката. Често си казваме: „Това са детски игри“ "
    "или „Някой друг ще се намеси“. Понякога точно тези секунди са критични."
)
CITIZENS_INTRO_EN = (
    "Every one of us has seen a group of teenagers surround a smaller child in the mall or the park, "
    "or shove each other aggressively on the bus or at the stop. We often tell ourselves: “It’s just children playing” "
    "or “Someone else will step in.” Sometimes those very seconds are the critical ones."
)

CITIZENS_BG = [
    "<strong>Не снимай, а помогни.</strong> Вместо да извадиш телефона за Facebook, Instagram или TikTok, използвай го, за да набереш 112 или 116 111. Ако ситуацията не е физически опасна, просто застани близо до тормозеното дете — присъствието на възрастен често е достатъчно агресорите да се оттеглят.",
    "<strong>Разсей ситуацията.</strong> Намеси се с добронамерен тон. Приближи се и попитай силно: „Здравейте, нещо сериозно ли става тук? Имате ли нужда от полиция?“ Или се обърни към детето: „Здравей, ела с мен до касата за малко.“",
    "<strong>Ангажирай още хора.</strong> В градския транспорт — кажи на шофьора. В мола — на охраната. На улицата — извикай силно към другите минувачи, за да не си сам.",
    "<strong>Не се излагай на опасност.</strong> Ако ситуацията е физически опасна, не влизай в нея. Обади се на 112 и остани наблизо като свидетел.",
    "<strong>Опиши фактите, когато подаваш сигнал.</strong> Място, час, колко са участниците, как изглеждат, в каква посока са тръгнали. Всяка подробност помага.",
]
CITIZENS_EN = [
    "<strong>Don’t film — help.</strong> Instead of taking out your phone for Facebook, Instagram or TikTok, use it to dial 112 or 116 111. If the situation is not physically dangerous, simply stand close to the child being bullied — an adult’s presence is often enough for the aggressors to back off.",
    "<strong>Defuse the situation.</strong> Step in with a friendly tone. Come closer and ask clearly: “Hello, is something serious going on here? Do you need the police?” Or turn to the child: “Hi, come with me to the checkout for a moment.”",
    "<strong>Bring in other people.</strong> On public transport, tell the driver. In a mall, tell security. On the street, call out to other passers-by so that you are not alone.",
    "<strong>Do not put yourself in danger.</strong> If the situation is physically dangerous, do not enter it. Call 112 and stay nearby as a witness.",
    "<strong>Describe the facts when you report.</strong> Place, time, how many people are involved, what they look like, which way they went. Every detail helps.",
]

CITIZENS_CLOSING_BG = (
    "За едно уплашено дете ти можеш да си единственият спасителен пояс в този момент. "
    "С реакцията си помагаш не само на жертвата, но и на агресорите — така поведението им "
    "получава внимание и вероятността да го променят е голяма."
)
CITIZENS_CLOSING_EN = (
    "For a frightened child you may be the only lifeline at that moment. By reacting you help not "
    "only the victim but the aggressors too — their behaviour gets attention, and the chance that "
    "they change it is real."
)

# ==========================================================================
#  Кампании на МВР / Ministry of Interior campaigns
# ==========================================================================

CAMPAIGNS = [
    {
        "id": "dobriyat-primer",
        "title_bg": "Добрият пример",
        "title_en": "The Good Example",
        "lead_bg": "Детско полицейско управление — Велинград. Как изглежда превенцията, когато полицаят е познато лице, а не униформа отдалеч.",
        "lead_en": "The Children’s Police Department in Velingrad. What prevention looks like when the officer is a familiar face rather than a uniform seen from afar.",
        "youtube": "fyiXOyATDhk",
        "body_bg": [
            "Детските полицейски управления събират деца от началния и прогимназиалния курс в редовни занимания с униформени служители — за пътна безопасност, за това какво е престъпление, какво е тормоз и към кого да се обърнеш.",
            "Смисълът им не е да изглеждат добре на снимка. Децата, които познават полицая по име, се обръщат към него, когато нещо се обърка — и това е цялата разлика.",
        ],
        "body_en": [
            "Children’s Police Departments bring primary and lower-secondary pupils into regular sessions with uniformed officers — on road safety, on what counts as a crime, on what bullying is and whom to turn to.",
            "Their point is not to look good in a photograph. Children who know the officer by name turn to him when something goes wrong — and that is the whole difference.",
        ],
        "photo": "dpu-10-godini.jpg",
        "photo_alt_bg": "Торта за 10 години Детско полицейско управление",
        "photo_alt_en": "A cake marking ten years of the Children’s Police Department",
        "credit_bg": "Видео: „Доброволци от Детското полицейско управление във Велинград създадоха обучителен клип“, публикувано в канала znamee Pazardjik.",
        "credit_en": "Video: “Volunteers from the Children’s Police Department in Velingrad made a training clip”, published on the znamee Pazardjik channel.",
    },
    {
        "id": "nasilieto-e-bezsilie",
        "title_bg": "Насилието е безсилие",
        "title_en": "Violence is powerlessness",
        "lead_bg": "Съвместна програма на МВР и Министерството на образованието и науката. Насочена е към учениците от VIII и IX клас и се разширява към минимум 100 000 ученици в над 1000 училища.",
        "lead_en": "A joint programme of the Ministry of Interior and the Ministry of Education and Science. It targets pupils in grades VIII and IX and is expanding to at least 100,000 pupils in over 1,000 schools.",
        "youtube": "",
        "body_bg": [
            "Програмата учи младите хора да разпознават домашното насилие и оскърбителното поведение, да отреагират на травматични преживявания, да премахнат чувството за вина и да повишат самооценката си.",
            "Целта не е просто да бъдат информирани какво е токсична връзка, а да разпознават ранните сигнали, да изграждат самоуважение и граници и да знаят, че имат право на здрава, подкрепяща и безопасна връзка — независимо от модела, който са виждали у дома.",
        ],
        "body_en": [
            "The programme teaches young people to recognise domestic violence and abusive behaviour, to respond to traumatic experience, to let go of guilt and to build their self-esteem.",
            "The aim is not simply to inform them what a toxic relationship is, but to have them recognise the early signals, build self-respect and boundaries, and know they have a right to a healthy, supportive and safe relationship — whatever model they have seen at home.",
        ],
        "photo": "kampaniya-presconf.jpg",
        "photo_alt_bg": "Представяне на кампанията пред медиите",
        "photo_alt_en": "The campaign being presented to the media",
    },
    {
        "id": "nikoga-poveche",
        "title_bg": "Никога повече насилие у дома",
        "title_en": "Never again violence at home",
        "lead_bg": "Кампания на МВР и УНИЦЕФ срещу домашното насилие. От домашното насилие има изход — потърси помощ и закрила.",
        "lead_en": "A campaign of the Ministry of Interior and UNICEF against domestic violence. There is a way out of domestic violence — seek help and protection.",
        "youtube": "",
        "body_bg": [
            "Всеки акт на насилие причинява болка и за него няма оправдание. Кампанията насочва пострадалите и свидетелите към линиите за помощ и към институциите, които могат да се намесят.",
            "Домашното насилие рядко остава само между възрастните. Детето, което го вижда, го носи със себе си — в училище, сред връстниците и по-късно в собствените си връзки.",
        ],
        "body_en": [
            "Every act of violence causes pain and there is no excuse for it. The campaign points those affected and those who witness it towards the helplines and the institutions that can step in.",
            "Domestic violence rarely stays between the adults. A child who sees it carries it onward — into school, among peers, and later into their own relationships.",
        ],
        "photo": "kampaniya-nikoga-poveche.jpg",
        "photo_alt_bg": "Плакат на кампанията „Никога повече насилие у дома“",
        "photo_alt_en": "Poster of the “Never again violence at home” campaign",
    },
]

# Галерия на кампаниите / campaign gallery
CAMPAIGN_GALLERY = [
    ("dpu-risunka.jpg", "Детска рисунка за Детското полицейско управление", "A child’s drawing of the Children’s Police Department"),
    ("bezopasnost-velosipedi.jpg", "Обучение по безопасно движение с велосипеди и тротинетки", "A session on safe cycling and scooter riding"),
    ("dobriyat-primer-pozharna.jpg", "Младеж на занятие с екип на Пожарна безопасност", "A young man at a session with a fire-safety team"),
    ("sabitie-bezopasnost.jpg", "Открито занятие по безопасност с участието на полицията", "An open-air safety session with the police"),
]

# ==========================================================================
#  Информация за платформата / about the platform
# ==========================================================================

# Видео на платформата / the platform video
PLATFORM_VIDEO = {
    "youtube": "G5PGVCCfQy8",
    "title_bg": "Кампания на МВР „Спаси Дете“",
    "title_en": "The Ministry of Interior’s “Save a child” campaign",
    "credit_bg": "Видео: канал ГДБОП-МВР в YouTube.",
    "credit_en": "Video: the GDBOP-MVR channel on YouTube.",
    "poster": "hero",
    "poster_alt_bg": "Полицейска служителка и дете със знак на МВР",
    "poster_alt_en": "A policewoman and a child holding a Ministry of Interior sign",
}

PLATFORM_BG = [
    "„Спаси дете“ е информационна платформа, насочена към превенция и противодействие на престъпления, свързани с насилие и агресия от и към деца.",
    "Сайтът има за цел да предостави полезна и достъпна информация за деца, родители и учители за разпознаването на рискови ситуации, както и възможност за лесно и бързо подаване на сигнали за престъпления срещу или от деца, която да достигне бързо и адекватно до съответната областна дирекция на МВР и до компетентните институции на всички нива в страната.",
]
PLATFORM_EN = [
    "“Save a child” is an information platform for preventing and countering crimes involving violence and aggression by and against children.",
    "The site sets out to give children, parents and teachers useful and accessible information for recognising situations of risk, together with a straightforward and fast way of reporting crimes against or by children, so that the report reaches the relevant regional directorate of the Ministry of Interior and the competent institutions at every level in the country quickly and appropriately.",
]
