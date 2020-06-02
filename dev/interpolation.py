class Interpolation:
    def cubic(y, x, xi):
        '''
        Алгоритм кубической интерполяции.
        '''
        ai = y[2]
        aj = y[1]
        ak = y[3]
        al = y[0]
        A = 5
        B = 20
        C = 5
        F1 = (ak + aj - 2 * ai) / 5
        F2 = (ai + al - 2 * aj) / 5
        alpha = -C/B
        beta1 = F1/B
        beta2 = F2/B
        ci = (F1 - A*beta1)/(B + A*alpha)
        cj = (F2 - A*beta2)/(B + A*alpha)
        di = (ci - cj) / 15
        bi = (ai - aj) / 5 + 5 * (2 * ci + cj) / 3
        return ai + bi * (x - xi) + ci * (x - xi) ** 2 + di * (x - xi) ** 3
    def bezier(self, *args):
        pass
        
