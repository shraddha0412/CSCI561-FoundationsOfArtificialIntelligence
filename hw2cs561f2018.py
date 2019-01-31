class Player:
    def __init__(self, assigned, available, score):
        self.assigned = assigned
        self.available = available
        self.scores = score

    def is_gameover(self):
        if self == SPLA and (all(s >= SPLA_spaces for s in self.scores) or not self.get_available()):
                return True
        elif self == LAHSA and (all(s >= LAHSA_beds for s in self.scores) or not self.get_available()):
                return True
        else:
            return False

    def get_available(self):
        op = []
        for key, val in self.available.iteritems():
            if val == 0:
                op.append(key)
        return op

    def get_next_applicant(self, applicant):
        score_app = mainDictionary.get(applicant)[6]
        self.scores = [l + m for l, m in zip(self.scores, score_app)]
        if self == LAHSA:
            if all(s <= LAHSA_beds for s in self.scores):
                self.assigned.append(applicant)
                self.available[applicant] = 1
                if applicant in SPLA.available:
                    SPLA.available[applicant] = 1
            else:
                self.scores = [l - m for l, m in zip(self.scores, score_app)]
            return SPLA
        elif self == SPLA:
            if all(s <= SPLA_spaces for s in self.scores):
                self.assigned.append(applicant)
                self.available[applicant] = 1
                if applicant in LAHSA.available:
                    LAHSA.available[applicant] = 1
            else:
                self.scores = [l - m for l, m in zip(self.scores, score_app)]
            return LAHSA

    def backtrack(self, applicant):
        if applicant in self.assigned:
            self.assigned.remove(applicant)
            score_app = mainDictionary.get(applicant)[6]
            self.scores = [l - m for l, m in zip(self.scores, score_app)]
        if applicant in LAHSA_Available and applicant not in LAHSA.get_available():
            LAHSA.available[applicant] = 0
        if applicant in SPLA_Available and applicant not in SPLA.get_available():
            SPLA.available[applicant] = 0


def evaluate(end_player):
    LAHSAscores = list(LAHSA.scores)
    SPLAscores = list(SPLA.scores)
    if end_player == SPLA:
        for p, it in enumerate(LAHSA.get_available()):
            val = mainDictionary.get(it)[6]
            LAHSAscores = [z + x for z, x in zip(LAHSAscores, val)]
            if not all(s <= LAHSA_beds for s in LAHSAscores):
                LAHSAscores = [z - x for z, x in zip(LAHSAscores, val)]
                break
    else:
        for p, it in enumerate(SPLA.get_available()):
            val = mainDictionary.get(it)[6]
            SPLAscores = [z + x for z, x in zip(SPLAscores, val)]
            if not all(s <= SPLA_spaces for s in SPLAscores):
                SPLAscores = [z - x for z, x in zip(SPLAscores, val)]
                break
    return [sum(SPLAscores), sum(LAHSAscores)]


def play(player):
    if player.is_gameover():
        return evaluate(player)
    availables = player.get_available()
    max_score = [float('-inf'),float('-inf')]
    for applicant in availables:
        player2 = player.get_next_applicant(applicant)
        score = play(player2)
        if player == LAHSA:
            if score[1] > max_score[1]:
                max_score = score
            player.backtrack(applicant)
        else:
            if score[0] > max_score[0]:
                max_score = score
            player.backtrack(applicant)
    return max_score


def maximax(player):
    availables = player.get_available()
    if not availables:
        return "",""
    max_app = availables[0]
    max_score = float('-inf')
    for applicant in availables:
        player2 = player.get_next_applicant(applicant)
        score = play(player2)
        print(applicant, score)
        if score[0] == max_score and int(applicant) < int(max_app):
            max_app = applicant
        if score[0] > max_score:
            max_app = applicant
            max_score = score[0]
        player.backtrack(applicant)
    return max_app, max_score


input_f = open('input.txt', 'r')
LAHSA_beds = int(input_f.readline().strip('\n'))
LAHSA_bedCount = [0,0,0,0,0,0,0]
SPLA_spaces = int(input_f.readline().strip('\n'))
SPLA_spaceCount = [0,0,0,0,0,0,0]

LAHSA_Assignments = []
assigned_LAHSA_count = int(input_f.readline().strip('\n'))
for i in range(assigned_LAHSA_count):
    LAHSA_Assignments.append(input_f.readline().strip('\n'))

SPLA_Assignments = []
assigned_SPLA_count = int(input_f.readline().strip('\n'))
for i in range(assigned_SPLA_count):
    SPLA_Assignments.append(input_f.readline().strip('\n'))

mainDictionary = {}
count = int(input_f.readline().strip('\n'))
LAHSA_Available = {}
SPLA_Available = {}
for i in range(count):
    applicants = (input_f.readline().strip('\n'))
    mainDictionary[applicants[0:5]] = [applicants[5], applicants[6:9],applicants[9], applicants[10], applicants[11],
                                      applicants[12], [int(applicants[13]), int(applicants[14]), int(applicants[15]),
                                        int(applicants[16]), int(applicants[17]), int(applicants[18]), int(applicants[19])]]
    if applicants[10] == 'N' and applicants[11] == 'Y' and applicants[12] == 'Y' and applicants[0:5] not in SPLA_Assignments and applicants[0:5] not in LAHSA_Assignments:
        SPLA_Available[applicants[0:5]] = 0

    if applicants[5] == 'F' and int(applicants[6:9]) > 17 and applicants[9] == 'N' and applicants[0:5] not in LAHSA_Assignments and applicants[0:5] not in SPLA_Assignments:
        LAHSA_Available[applicants[0:5]] = 0

for k, item in enumerate(SPLA_Assignments):
    value = mainDictionary.get(item)[6]
    SPLA_spaceCount = [i + j for i, j in zip(SPLA_spaceCount, value)]

for k, item in enumerate(LAHSA_Assignments):
    value = mainDictionary.get(item)[6]
    LAHSA_bedCount = [i + j for i, j in zip(LAHSA_bedCount, value)]

LAHSA = Player(list(LAHSA_Assignments), LAHSA_Available, list(LAHSA_bedCount))
SPLA = Player(list(SPLA_Assignments), SPLA_Available, list(SPLA_spaceCount))
open("output.txt", "w").write(maximax(SPLA)[0])
print(maximax(SPLA))