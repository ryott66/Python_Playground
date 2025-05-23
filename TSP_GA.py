import numpy as np
import math

class TSP:

    def __init__(self, PROB_DIMEINTION):
        self.PROB_DIMEINTION = PROB_DIMEINTION
        self.rd = np.random
        self.rd.seed(1)

        self.map_info = self.TSP_mapGenerator()

    def TSP_mapGenerator(self):
        x_coord  = [self.rd.randint(0, 100) for _ in range(self.PROB_DIMEINTION)]
        y_coord  = [self.rd.randint(0, 100) for _ in range(self.PROB_DIMEINTION)]

        coord    = [[x_coord[i], y_coord[i]] for i in range(self.PROB_DIMEINTION)]
        pos_info = []
        for i in range(self.PROB_DIMEINTION):
            pos_info.append(coord[i])
        return pos_info

    def evaluate(self, x):
        if not len(x) == self.PROB_DIMEINTION:
            print("Error: Solution X is not a {}-d vector".format(self.PROB_DIMEINTION))
            return None

        _dst  = 0
        for i in range(len(x)-1):
            _prev = self.map_info[x[i]]
            _next = self.map_info[x[i+1]]

            _dst += math.sqrt(math.pow(_prev[0]-_next[0], 2) + math.pow(_prev[1]-_next[1], 2))

        return _dst



class RandomSearch:

    def __init__(self, N, MAX_EVALUATIONS, PROB_DIMEINTION):
        #RS settings
        self.N  = N

        #Problem settings
        self.MAX_EVALUATIONS = MAX_EVALUATIONS
        self.PROB_DIMEINTION = PROB_DIMEINTION

        #Private variables
        self.Xs = [None for _ in range(self.N)]
        self.Fs = [None for _ in range(self.N)]
        self.BestX = None
        self.BestFX = None
        self.BASICTOUR = [i for i in range(0,self.PROB_DIMEINTION)] #[0,1,2,...,50]

    def initialization(self):
        for i in range(self.N):
            self.Xs[i] = np.random.permutation(self.BASICTOUR)

    def evaluate(self, tsp):
        for i in range(self.N):
            self.Fs[i] = tsp.evaluate(self.Xs[i])

    def update(self):
        for i in range(self.N):
            if self.BestFX == None or self.Fs[i] < self.BestFX:
                self.BestX  = self.Xs[i]
                self.BestFX = self.Fs[i]

    def generation(self):
        self.initialization()

class GeneticAlgorithm:

    def __init__(self, N, CrossoverRate, MutationRate, TournamentSize, MAX_EVALUATIONS, PROB_DIMEINTION):
        # GA settings
        self.N  = N
        self.PC = CrossoverRate
        self.PM = MutationRate
        self.TS = TournamentSize

        #Problem settings
        self.MAX_EVALUATIONS = MAX_EVALUATIONS
        self.PROB_DIMEINTION = PROB_DIMEINTION

        #Private variables
        self.Xs        = [None for _ in range(self.N)]  #解集合
        self.Fs        = [None for _ in range(self.N)]  #解集合の適合度（コスト）
        self.BestX     = None
        self.BestFX    = None
        self.BASICTOUR = [i for i in range(0,self.PROB_DIMEINTION)] #[0,1,2,...,50]

    def initialization(self):#解集合の初期化　N個の経路をランダム作製
        for i in range(self.N):
            self.Xs[i] = np.random.permutation(self.BASICTOUR)

    def evaluate(self, tsp):  #全解集合XsのコストFsを計算
        for i in range(self.N):
            self.Fs[i] = tsp.evaluate(self.Xs[i])

    def update(self):   #全ての現在の解集合Xs[i]におけるコストFs[i]でBestを探して更新
        for i in range(self.N):
            if self.BestFX == None or self.Fs[i] < self.BestFX:
                self.BestX  = self.Xs[i]
                self.BestFX = self.Fs[i]

    # generate next population  (main cycle)
    def generation(self):    #解集合Xsを更新（遺伝的に）
        nextXs = []
        for _ in range((int)(self.N/2)):
            # parent selection
            parent1 = self.TournamentSelection()
            parent2 = self.TournamentSelection()

            #crossover
            offspring1, offspring2 = self.crossover(parent1, parent2)

            #mutation
            offspring1 = self.mutation(offspring1)
            offspring2 = self.mutation(offspring2)

            #add offspring to next population
            nextXs.append(offspring1)
            nextXs.append(offspring2)

        #update population
        self.Xs = nextXs

    # parent selection
    def TournamentSelection(self):
        tournamentlistidx= np.random.choice(self.N,self.TS,replace=False) #0~NからTS個をランダムで選択してリストを返す、重複なし
        Ftounamentlist=[self.Fs[tournamentlistidx[i]] for i in range(self.TS)]  #トーナメントリストの解の、適合度（コスト）を保存
        minFlist=np.min(Ftounamentlist)  #リストからトーナメントを勝つ最小値を探す
        for i in range(self.N):  #解集合の中からトーナメント勝者を探し、「解」を返す
            if minFlist==self.Fs[i]:
                return self.Xs[i]
    # crossover
    def crossover(self, parent1, parent2):
        # execute crossover with probability PC
        if np.random.rand() < self.PC:
            #determine the boundary for cross
            bou=np.random.randint(self.PROB_DIMEINTION-1)#0~48の整数

            #copy parent between "first"  and "bound"-th structures of parent
            offspring1=[parent1[i] for i in range(bou)] #[0] ~ ([1]~[48])
            offspring2=[parent2[i] for i in range(bou)]
            #copy another parent while escaping duplication of cities
            for a in parent2:
              if a not in offspring1:
                offspring1.append(a)
            for b in parent1:
              if b not in offspring2:
                offspring2.append(b)

            return offspring1, offspring2

        # return copies of parents if crossover does not act
        else:
            offspring1 = [parent1[i] for i in range(self.PROB_DIMEINTION)]
            offspring2 = [parent2[i] for i in range(self.PROB_DIMEINTION)]
            return offspring1, offspring2

    def mutation(self, offspring):
        # execute mutation with probability PM
        if np.random.rand() < self.PM:
            #select two points (alleles) to be swapped
            #0~49からランダムで2個選び要素数2のリスト
          sidx=np.random.choice(self.PROB_DIMEINTION,2,replace=False)
            #swap selected points
          offspring[sidx[0]],offspring[sidx[1]]=offspring[sidx[1]],offspring[sidx[0]]

          return offspring
        else:
            return offspring


def run(problem, optimizer, MAX_EVALUATIONS, filename):
    print("run {}".format(filename))

    evals = 0
    log   = []

    optimizer.initialization()
    optimizer.evaluate(problem)

    while evals < MAX_EVALUATIONS:
        optimizer.generation()
        optimizer.evaluate(problem)
        optimizer.update()
        evals += optimizer.N

        #logging
        print(evals, optimizer.BestFX)
        log.append([evals, optimizer.BestFX])
    np.savetxt('_out_{}.csv'.format(filename), log, delimiter=',')

if __name__ == "__main__":
    #Basic setting
    N, MAX_EVALUATIONS, PROB_DIMEINTION = 100, 50000, 50
    TSP = TSP(PROB_DIMEINTION)

    #run Random search
    RS = RandomSearch(N, MAX_EVALUATIONS, PROB_DIMEINTION)
    run(TSP, RS, MAX_EVALUATIONS, "RS")

    #run Genetic algorithm
    CrossoverRate, MutationRate, TournamentSize = 1.0, 0.1, 10
    GA = GeneticAlgorithm(N, CrossoverRate, MutationRate, TournamentSize, MAX_EVALUATIONS, PROB_DIMEINTION)
    run(TSP, GA, MAX_EVALUATIONS, "GA")
