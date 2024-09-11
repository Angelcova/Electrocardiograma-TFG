from random import uniform
import matplotlib.pyplot as plt

def electro():
    pr = round(uniform(0.16,0.2),3)
    qrs = round(uniform(0.06,0.12),3)
    qt = round(uniform(0.34,0.45),3)
    st = round(uniform(0.05,0.150),3)
    tiempoParcial = pr + qt
    tiempoTotal = round(uniform(tiempoParcial, 1.0),3)
    latido = [pr,qrs,qt,st]
    return latido, tiempoTotal

if __name__ == "__main__":
    latido,tiempoLatido = electro()
    for i in range(4):
        print(latido[i])
    print(tiempoLatido)
    p = latido[0]/2
    q = latido[0]
    r = (latido[1]/2) + latido[0]
    s = latido[1] +latido[0]
    st = s + 0.04
    t = ((latido[2] - latido[3])/2) + latido[1] +latido[0] + latido[3]

    x = [0,p,q,r,s,st,t,tiempoLatido]
    y =[0,0.15,-0.15,0.9,-0.3,0,0.3,0]

    plt.plot(x,y,marker='o')
    plt.show()




