import matplotlib.pyplot as plt
from graphic import read_data, find_optimal_EMA,oper_MACD,MACD, EMA, read_all_data
def draw():
    closes, highs, lows, opens = read_all_data("../data/apple/AAPL_historical_data.csv")
    x = [i for i in range(len(closes))]
    # x = list(range(len(y)))
    zero = [0] * len(closes)
    plt.plot(x, zero)
    # plt.plot(x, opens, label="open")
    plt.plot(x, closes, label="close")
    # plt.plot(x, [sum(y) / len(y) for i in range(len(y))], label="avg")
    # plt.plot(x, creat_line_f(y), label="liner_avg")
    # plt.plot(x, SMA(y, m=12), label='SMA12')
    # plt.plot(x, SMA(y, m=26), label='SMA26')
    # plt.plot(x, EMA(y, t=0.5), label="EMA")
    # plt.plot(x, UMA(closes, t=0.5), label="UMA")
    # m = 12
    # up, sma, down = bolinger_bands(y, m=m)
    # plt.plot(x, up, label=f"upper bound{m}")
    # plt.plot(x, sma, label=f"sma{m}")
    # plt.plot(x, down, label=f"lower bound{m}")

    # m = 26
    # up, sma, down = bolinger_bands(closes, m=m)
    # plt.plot(x, up, label=f"upper bound{m}")
    # plt.plot(x, sma, label=f"sma{m}")
    # plt.plot(x, down, label=f"lower bound{m}")
    # uma = SMA(closes,14)
    # plt.plot(x, uma, label=f"uma(t = 0.5, m=14")
    ft, sc = find_optimal_EMA(closes)
    ft.draw(x)
    sc.draw(x)
    # sma = EMA(closes, t=sc[2])
    # plt.plot(x, sma, label=f"SMA m={sc[1]}")
    macd = MACD(sc, ft)
    macd.draw(x)

    MACD_oper = oper_MACD(macd, EMA, 48)
    MACD_oper.draw(x)

    for i in ft, sc, MACD_oper:
        print(f"{i} stonks {i.stonks} with chance {i.reliability}")
    if macd.line[-1] > 0:
        print(f"{macd} stonks")
    else:
        print(f"{macd} not stonks")


    print()




    plt.legend(loc="best")
    plt.show()
if __name__ == "__main__":
    draw()