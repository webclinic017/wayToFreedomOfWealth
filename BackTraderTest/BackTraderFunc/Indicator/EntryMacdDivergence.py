import backtrader as bt

'''
进场条件：
    1.MACD底背离
    2.价格在20日ema均线以上
'''
class MACDEMAEntryPoint(bt.Indicator):
    lines = ('top_divergences', 'bottom_divergences', 'entryPoint', )
    plotinfo = dict(subplot=True, plotlinelabels=True)

    params = dict(
        smaPeriod=20,
    )

    def __init__(self):
        self.strat = self._owner  # alias for clarity
        self.buyTrend = False
        self.div_top_List = []
        self.div_bottom_List = []

        self.sma = bt.talib.EMA(self.data, period=self.p.smaPeriod)

        for data in self.strat.datas:
            self.div_top_List.append(data.divergence_top)
            self.div_bottom_List.append(data.divergence_bottom)

    def next(self):
        self.l.entryPoint[0] = 0

        if self.buyTrend:
            # 这里进入之后，需要判断拐头和交叉，如果没有，要退出
            if self.data[0] > self.sma[0]:
                self.buyTrend = False
                self.l.entryPoint[0] = 1
            else:
                for div_top in self.div_top_List:
                    if div_top[0] > 0:
                        self.buyTrend = False
                        self.l.top_divergences[0] = 1
        else:
            for div_bottom in self.div_bottom_List:
                if div_bottom[0] > 0:
                    self.buyTrend = True
                    self.l.bottom_divergences[0] = 1