# import matplotlib.pyplot as plt


class Graphic:
    def __init__(self, c, alg, *args, name=None, err=False, min_positive=False):
        self.line = alg(c, *args)
        self.min_positive = min_positive
        self.signal = False
        if err:
            self.err, self.stonks, self.reliability = self.count_err(c)
        else:
            self.err, self.stonks, self.reliability = 0, 0, 0
        self.args = args
        if name is None:
            self.name = f"{alg.__name__}{args}"
        else:
            self.name = name

    def count_err(self, c):
        assert len(c) == len(self.line)
        cnter = 0
        intersect_points = []
        for i in range(1, len(c)):
            if c[i - 1] > self.line[i - 1] and self.line[i] > c[i] or c[i - 1] < self.line[i - 1] and self.line[i] < c[
                i]:
                cnter += 1
                intersect_points.append(i)
        # print(cnter, end=", ")
        old_cnt = cnter
        for i in range(len(intersect_points)):
            flag = c[intersect_points[i]] > self.line[intersect_points[i]]
            start_value = c[intersect_points[i]]
            if i == len(intersect_points) - 1:
                end = len(c)
            else:
                end = intersect_points[i + 1]
            for j in range(intersect_points[i] + 1, end):
                is_it = c[j] > start_value
                if is_it == flag:
                    cnter -= 1
                    break
        if old_cnt == 0:
            rely = 0
        else:
            rely = (old_cnt - cnter) / old_cnt
        if len(intersect_points) == 0:
            stonks = None
        else:
            stonks = c[intersect_points[-1]] > self.line[intersect_points[-1]]
            if len(c) - 1 == intersect_points[-1]:
                self.signal = True

        return cnter, stonks, rely

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name == other.name and self.args == other.args

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.reliability < other.reliability

    def __le__(self, other):
        return self.reliability <= other.reliability

    def __gt__(self, other):
        return self.reliability > other.reliability

    def __ge__(self, other):
        return self.reliability >= other.reliability

    # def draw(self, x):
    #     plt.plot(x, self.line, label=self.__str__())

    def __getitem__(self, item):
        return self.line[item]

    def __len__(self):
        return len(self.line)

    def __iter__(self):
        return iter(self.line)


def diff(c, big, small):
    ans = []
    for i, j in zip(small, big):
        ans.append(i - j)
    return ans


def MACD(big, small):
    return Graphic([], diff, big.line, small.line, name=f"MACD({big}, {small})", min_positive=True)


class oper_MACD(Graphic):
    def __init__(self, macd, alg, *args):
        self.name = f"опережающий макд {alg.__name__}{args}({macd})"
        self.line = alg(macd, *args)
        self.err, self.stonks, self.reliability = self.count_err(macd)
        self.min_positive = True
        self.signal = False



def returning_value(a):
    def f(x):
        return [a] * len(x)


def return_it_self(c):
    return c[::]


def read_all_data(file):
    closes = []
    highs = []
    lows = []
    opens = []
    with open(file) as f:
        for i in f.readlines()[1:]:
            try:
                s = [float(j.strip('"')) for j in i.split(",")[1:5]]
            except:
                continue
            opens.append(s[0])
            highs.append(s[1])
            lows.append(s[2])
            closes.append(s[3])
    return closes, highs, lows, opens


def read_data(file):
    dates = []
    closes = []
    opens = []
    cnt = 0
    with open(file) as f:
        for i in f.readlines()[3:]:
            # print(i.split(","))
            closes.append(float(i.split(",")[1].strip('"')))
            # dates.append(i.split(",")[0].strip('"'))
            dates.append(cnt)
            cnt += 1

            opens.append(float(i.split(",")[1].strip('"')))
    ln = len(opens)
    return opens[:ln], dates[:ln], closes[:ln]


def gaus(m):
    for i in range(len(m)):
        mn = 10 ** 7
        ind = -1
        for i2 in range(i, len(m)):
            if abs(m[i2][i]) < mn and m[i2][i] != 0:
                ind = i2
        if ind != i:
            str_m = m[ind].copy()
            m[ind] = m[i].copy()
            m[i] = str_m
        x = m[i][i]
        for j in range(i, len(m[0])):
            if m[i][j] != 0:
                m[i][j] /= x
        for i1 in range(i + 1, len(m)):
            y = m[i1][i]
            for j1 in range(i, len(m[0])):
                m[i1][j1] -= m[i][j1] * y
        # Обратный ход
    for i in range(len(m) - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            m[j][-1] -= (m[i][-1] * m[j][i])
            m[j][i] = 0


def answer_from_gaus(m):
    return [m[j][-1] for j in range(len(m))]


def creat_line_f(y):
    n = len(y)
    p = sum([i for i in range(n)])
    q = sum([i * i for i in range(n)])
    c = sum(y)
    d = sum([y[i] * i for i in range(n)])
    m = [[n, p, c],
         [p, q, d]]
    gaus(m)
    b, a = answer_from_gaus(m)
    return [a * x + b for x in range(n)]


def SMA(y, m=5):
    sma = [y[i] for i in range(m)]
    for i in range(m, len(y)):
        sma.append(sum(y[i - m:i]) / m)
    return sma


def EMA(c, m=1):
    t = 2 / (m + 1)
    ema = [c[0]]
    for i in range(1, len(c)):
        ema.append((1 - t) * ema[-1] + t * c[i])
    return ema


def UMA(c, t=1, m=9):
    uma = [c[i] for i in range(m)]
    const = (1 - (1 - t) ** m)
    for i in range(m, len(c)):
        sm = 0
        for j in range(m):
            sm += c[i - j] * ((t * (1 - t) ** j) / const)
        uma.append(sm)
    return uma


def find_optimal_EMA(c, low_m=5, high_m=50):
    lst = []
    mx = None
    for t in range(low_m, (high_m - low_m) // 2):
        line = Graphic(c, EMA, t, err=True)
        # print(line, line.err)
        if mx is not None:
            mx = max(mx, line)
        else:
            mx = line
    lst.append(mx)
    mx = None
    for t in range(max((high_m - low_m) // 2 + 1, lst[0].args[0] + 10), high_m):
        line = Graphic(c, EMA, t, err=True)
        # print(line, line.err)
        if mx is not None:
            mx = max(mx, line)
        else:
            mx = line
    lst.append(mx)
    return lst


def bolinger_bands(c, m=5, l=2):
    sma = SMA(c, m=m)
    sigma = [c[i] for i in range(m)]
    for i in range(m, len(c)):
        sm = 0
        for k in range(i - m + 1, i):
            sm += ((c[k] - sma[k]) ** 2) * (1 / m)
        sigma.append(sm ** 0.5)
    u = [sma[i] + l * sigma[i] if i >= m else c[i] for i in range(len(c))]
    d = [sma[i] - l * sigma[i] if i >= m else c[i] for i in range(len(c))]
    return u, sma, d


class Zero(Graphic):
    def __init__(self, cnt):
        self.line = [0] * cnt
        self.min_positive = True
