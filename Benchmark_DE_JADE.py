import math  as mt
import numpy as np
import scipy.stats as stats


class Function:

    """ constructor """
    # initialize method
    def __init__(self, PROB_NAME, PROB_DIMEINTION,):

        """ instance variable """
        self.PROB_DIMEINTION = PROB_DIMEINTION
        self.axis_range     = [0, 0]

        # choice of functions
        if PROB_NAME == "Rosenbrock":
            self.evaluate = self.Rosenbrock
            self.axis_range  = [-50, 50]
        elif PROB_NAME == "Ackley":
            self.evaluate = self.Ackley
            self.axis_range  = [-50, 50]
        elif PROB_NAME == "Rastrigin":
            self.evaluate = self.Rastrigin
            self.axis_range  = [-50, 50]

    """ instance method """
    # evaluation
    def doEvaluate(self, x):
        if not len(x) == self.PROB_DIMEINTION:
            print("Error: Solution X is not a {}-d vector".format(self.PROB_DIMEINTION))
            return None

        return self.evaluate(x)

    # Rosenbrock
    def Rosenbrock(self, x):
        ret = 0.
        for i in range(self.PROB_DIMEINTION - 1):
            ret += 100 * (x[i]**2 - x[i+1])**2 + (x[i] - 1)**2
        return ret

    # Ackley
    def Ackley(self, x):
        sum_1 = 0.
        sum_2 = 0.
        for i in range(self.PROB_DIMEINTION):
            sum_1 += x[i] * x[i]
            sum_2 += np.cos(2 * np.pi * x[i])
        ret = -20 * np.exp(-0.2 * np.sqrt(sum_1 / self.PROB_DIMEINTION)) - np.exp(sum_2 / self.PROB_DIMEINTION) + 20 + np.e
        return ret

    # Rastrigin
    def Rastrigin(self, x):
        ret = 0.
        for i in range(self.PROB_DIMEINTION):
            ret += x[i]**2 - 10 *mt.cos( 2 * mt.pi * x[i] ) + 10
        return ret



class RandomSearch:

    def __init__(self, N, Xmax, MAX_EVALUATIONS, PROB_DIMEINTION):
        #RS settings
        self.N    = N
        self.Xmax = Xmax

        #Problem settings
        self.MAX_EVALUATIONS = MAX_EVALUATIONS
        self.PROB_DIMEINTION = PROB_DIMEINTION

        #Private variables
        self.Xs = [None for _ in range(self.N)]
        self.Fs = [None for _ in range(self.N)]
        self.BestX = None
        self.BestFX = None

    def initialization(self):
        for i in range(self.N):
            self.Xs[i] = np.random.rand(self.PROB_DIMEINTION) *  (2* self.Xmax) - self.Xmax

    def evaluate(self, prob):
        for i in range(self.N):
            self.Fs[i] = prob.evaluate(self.Xs[i])

    def update(self):
        for i in range(self.N):
            if self.BestFX == None or self.Fs[i] < self.BestFX:
                self.BestX  = self.Xs[i]
                self.BestFX = self.Fs[i]

    def generation(self):
        self.initialization()

class DifferentialEvolution:
    def __init__(self, N, F, CR, Xmax, MAX_EVALUATIONS, PROB_DIMEINTION):
        # DE settings
        self.N    = N     # Number of individuals
        self.F    = F     # Scaling factor
        self.CR   = CR    # #Crossover rate
        self.Xmax = Xmax  # Defined range of position variables (search space)

        #Problem settings
        self.MAX_EVALUATIONS = MAX_EVALUATIONS
        self.PROB_DIMEINTION = PROB_DIMEINTION

        #Variables
        self.Xs        = [None for _ in range(self.N)] # Population
        self.Us        = [None for _ in range(self.N)] # Offspring　　子個体は親個体と同数　全個体に対して遷移を行う
        self.Fs        = [None for _ in range(self.N)] # Fitness (personal best's fitness)

        self.BestX     = None # Global best
        self.BestFX    = None # Best fitness (of global best)


    def initialization(self):
        for i in range(self.N):
            self.Xs[i] = np.random.rand(self.PROB_DIMEINTION) *  (2* self.Xmax) - self.Xmax    #各解が20個の配列であり、その中身は-50~50の乱数

    def evaluate(self, prob):  #子孫(U[s])をつくった後
        #For "initialization"
        if self.Us[0] == None:
            for i in range(self.N):
                self.Fs[i] = prob.evaluate(self.Xs[i])
        #For "generation"
        else:
            for i in range(self.N):
                _eval = prob.evaluate(self.Us[i])
               #print(self.Us[i])
               # print(_eval,self.Fs[i])
                if _eval <= self.Fs[i]: #update population only if offspring is better than the corresponding solution
                    self.Fs[i] = _eval
                    self.Xs[i] = self.Us[i]

    def update(self):   #解集合内の最適解とそのValueを更新
        #identify the best solution discovered so far
        for i in range(self.N):
            if self.BestFX == None or self.Fs[i] < self.BestFX:
                self.BestX  = self.Xs[i]
                self.BestFX = self.Fs[i]

    def generation(self):
        for i in range(self.N):
            #generate mutant solution with "rand/1" strategy
            v = self.mutation_rand1()  #解に加える20次元ベクトル配列
            #apply binominal crossover: generate offspring based on the mutant solution and the corresponding solution Xs[i]
            u = self.crossover_binominal(self.Xs[i], v)
            #update the offspring set
            self.Us[i] = u

    def mutation_rand1(self):
        #randomly pick up three ID's solutions in Population
        choice = np.random.randint(0,self.N, size =3)
        #identify the solutions selected randomly
        x1, x2, x3 = self.Xs[choice[0]], self.Xs[choice[1]], self.Xs[choice[2]]

        #prepare the output array (mutant solution)
        v = [0 for _ in range(self.PROB_DIMEINTION)]

        for i in range(self.PROB_DIMEINTION):
            v[i] = x1[i] + self.F * (x2[i] - x3[i])    #1つの解（20次元ベクトル）に対しての計算

        return v

    def crossover_binominal(self, x, v):
        # one element should be forcedly changed
        choice = np.random.randint(0, self.PROB_DIMEINTION)

        #prepare the output array (mutant solution)
        u = [x[i] for i in range(self.PROB_DIMEINTION)] #xは解1つが入ってる　uにコピー

        for i in range(self.PROB_DIMEINTION):
          if i == choice:  #choiceのときは絶対更新
            u[i] = v[i]
          else:     #それ以外はCRと比較して更新
            if np.random.rand() < self.CR:
              u[i] = v[i]
        return u
    
class JADE:
    def __init__(self, N, Xmax, MAX_EVALUATIONS, PROB_DIMEINTION):
        self.N = N
        self.Xmax = Xmax
        self.MAX_EVALUATIONS = MAX_EVALUATIONS
        self.PROB_DIMEINTION = PROB_DIMEINTION
        self.F = [0.5 for _ in range(self.N)]
        self.CR = [0.5 for _ in range(self.N)]
        self.myuF = 0.5
        self.myuCR = 0.5
        self.Xs = [None for _ in range(self.N)]
        self.Us = [None for _ in range(self.N)] # Offspring　　子個体は親個体と同数　全個体に対して遷移を行う
        self.Fs = [None for _ in range(self.N)]
        self.BestX = None
        self.BestFX = None


    def initialization(self):
        self.F = [0.5 for _ in range(self.N)]
        self.CR = [0.5 for _ in range(self.N)]
        self.myuF = 0.5
        self.myuCR = 0.5
        self.Us = [None for _ in range(self.N)] # Offspring　　子個体は親個体と同数　全個体に対して遷移を行う
        self.Fs = [None for _ in range(self.N)]
        self.BestX = None
        self.BestFX = None

        for i in range(self.N):
            self.Xs[i] = np.random.rand(self.PROB_DIMEINTION) * (2 * self.Xmax) - self.Xmax
        self.update()  # BestXを初期化


    def evaluate(self, prob):  #子孫(U[s])をつくった後
        #For "initialization"
        if self.Us[0] == None:
            for i in range(self.N):
                self.Fs[i] = prob.evaluate(self.Xs[i])
        #For "generation"
        else:
            Sn=0
            SF=0
            SF2=0
            SCR=0
            c=0.1
            for i in range(self.N):
                _eval = prob.evaluate(self.Us[i])
               #print(self.Us[i])
               # print(_eval,self.Fs[i])
                if _eval <= self.Fs[i]: #update population only if offspring is better than the corresponding solution
                    self.Fs[i] = _eval
                    self.Xs[i] = self.Us[i]
                    Sn+=1
                    SF+=self.F[i]
                    SF2+=self.F[i]*self.F[i]
                    SCR+=self.CR[i]

            if((SF !=0) and (Sn !=0)):
              self.myuF = (1-c)*self.myuF + c*(SF2/SF)
              self.myuCR = (1-c)*self.myuCR + c*(SCR/Sn)



    def update(self):   #解集合内の最適解とそのValueを更新
        #identify the best solution discovered so far
        for i in range(self.N):
            if self.BestFX == None or self.Fs[i] < self.BestFX:
                self.BestX  = self.Xs[i]
                self.BestFX = self.Fs[i]


    def generation(self):
        for i in range(self.N):#F[i]とCR[i]は解ごとにそのμF, μCRから計算する
            self.F[i] = stats.cauchy.rvs(loc=self.myuF, scale=0.1)
            if self.F[i] < 0:
                self.F[i] = 0
            elif self.F[i] > 1:
                self.F[i] = 1

            self.CR[i] = np.random.normal(self.myuCR, 0.1)
            if self.CR[i] < 0:
                self.CR[i] = 0
            elif self.CR[i] > 1:
                self.CR[i] = 1

            v = self.mutation(self.Xs[i],self.F[i])
            u = self.crossover(self.Xs[i], v, self.CR[i])
            self.Us[i] = u




    def mutation(self,x,F):
        #randomly pick up three ID's solutions in Population
        choice = np.random.randint(0,self.N, size =2)
        #identify the solutions selected randomly
        x2, x3 = self.Xs[choice[0]], self.Xs[choice[1]]

        #prepare the output array (mutant solution)
        v = [0 for _ in range(self.PROB_DIMEINTION)]

        #ADD rand1's operator to produce the mutant vector
        for i in range(self.PROB_DIMEINTION):
            v[i] = x[i] + F * (self.BestX[i]-x[i]) + F * (x2[i] - x3[i])    #1つの解（20次元ベクトル）に対しての計算

        return v


    def crossover(self, x, v, CR):
        # one element should be forcedly changed
        choice = np.random.randint(0, self.PROB_DIMEINTION)

        #prepare the output array (mutant solution)
        u = [x[i] for i in range(self.PROB_DIMEINTION)] #xは解1つが入ってる　uにコピー

        #Add binomial crossover to produce offspring
        for i in range(self.PROB_DIMEINTION):
          if i == choice:  #choiceのときは絶対更新
            u[i] = v[i]
          else:     #それ以外はCRと比較して更新
            if np.random.rand() < CR:
              u[i] = v[i]
        return u

def run(problem, optimizer, MAX_EVALUATIONS, filename):
    print("run {}".format(filename))

    evals = 0
    log   = []

    optimizer.initialization()
    optimizer.evaluate(problem)

    while evals < MAX_EVALUATIONS:
        optimizer.generation()#子個体の生成
        optimizer.evaluate(problem)#子と親を評価してXsが更新される
        optimizer.update()
        evals += optimizer.N
        if(optimizer=="JADE_Optimizer"):
          print(evals, optimizer.BestFX,"F:",optimizer.myuF,"CR:",optimizer.myuCR)
        else:
          print(evals, optimizer.BestFX)
        log.append([evals, optimizer.BestFX])

    np.savetxt('_out_{}.csv'.format(filename), log, delimiter=',')


if __name__ == "__main__":
    #Basic setting
    N, MAX_EVALUATIONS, PROB_DIMEINTION, Xmax = 50, 50000, 20, 50
    PROBLEM_LIST = ["Rosenbrock", "Ackley", "Rastrigin"]

    #Random search setting
    RS = RandomSearch(N, Xmax, MAX_EVALUATIONS, PROB_DIMEINTION)
    for i in range(len(PROBLEM_LIST)):
        fnc = Function(PROBLEM_LIST[i], PROB_DIMEINTION)
        run(fnc, RS, MAX_EVALUATIONS, "RS_{}".format(PROBLEM_LIST[i]))

    #DE setting
    F, CR = 0.5, 0.9
    DE = DifferentialEvolution(N, F, CR, Xmax, MAX_EVALUATIONS, PROB_DIMEINTION)
    for i in range(len(PROBLEM_LIST)):
        fnc = Function(PROBLEM_LIST[i], PROB_DIMEINTION)
        run(fnc, DE, MAX_EVALUATIONS, "DE_{}".format(PROBLEM_LIST[i]))

    # JADE setting
    JADE_Optimizer = JADE(N, Xmax, MAX_EVALUATIONS, PROB_DIMEINTION)
    for i in range(len(PROBLEM_LIST)):
        fnc = Function(PROBLEM_LIST[i], PROB_DIMEINTION)
        run(fnc, JADE_Optimizer, MAX_EVALUATIONS, "JADE_{}".format(PROBLEM_LIST[i]))