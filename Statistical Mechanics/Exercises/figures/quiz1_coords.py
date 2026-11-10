"""Coordinates for the Quiz 1 figures (lens fit and ternary conversion)."""
import numpy as np, json
out={}
# ---- Problem 2 lens: ideal solutions, T_A=1.5 (X=0), T_B=1.0 (X=1), s_f fitted
TA,TB,SF=1.5,1.0,2.3052346
W,H=6.0,5.0                       # plot box in cm; T from 0.85 to 1.6
T0,T1=0.85,1.6
def lens(T):
    kA=np.exp(SF*TA*(1/T-1/TA)); kB=np.exp(SF*TB*(1/T-1/TB))
    Xl=(1-kA)/(kB-kA); return Xl, kB*Xl
def xy(X,T): return (W*X, H*(T-T0)/(T1-T0))
Ts=np.linspace(TB+1e-4,TA-1e-4,60)
liq=[xy(*[lens(T)[0],T]) for T in Ts]; sol=[xy(*[lens(T)[1],T]) for T in Ts]
liq=[xy(1,TB)]+liq+[xy(0,TA)]; sol=[xy(1,TB)]+sol+[xy(0,TA)]
fmt=lambda pts:" ".join(f"({x:.3f},{y:.3f})" for x,y in pts)
out["lens_liq"]=fmt(liq); out["lens_sol"]=fmt(sol)
out["T2y"]=round(xy(0,1.299012)[1],3)
out["TAy"]=round(xy(0,TA)[1],3); out["TBy"]=round(xy(0,TB)[1],3)
# ---- Problem 5 ternary: barycentric from the quiz image pixels
Ab=np.array([40,490.]);An=np.array([572,497.]);Di=np.array([319,35.])
M=np.array([[Ab[0],An[0],Di[0]],[Ab[1],An[1],Di[1]],[1,1,1]])
def comp(p): return np.linalg.solve(M,[p[0],p[1],1])   # (Ab, An, Di) fractions
S=8.0; P_Ab=np.array([0,0.]); P_An=np.array([S,0.]); P_Di=np.array([S/2,S*np.sqrt(3)/2])
def tri(w): w=np.clip(w,0,None); w=w/w.sum(); return w[0]*P_Ab+w[1]*P_An+w[2]*P_Di
cot_px=[(60,458),(90,435),(120,415),(150,398),(195,372),(254,347),(282,333),(320,316),(350,300),(372,285),(400,262),(425,229)]
cot=[comp(p) for p in cot_px]
cot[0]=np.array([0.93,0,0.07]); cot[-1]=np.array([0,0.42,0.58])     # eutectics on the edges
out["cot"]=fmt([tri(w) for w in cot])
names={"A":(330,400),"l1":(305,377),"l2":(282,333),"l3":(254,347),"l4":(195,372),"s3":(373,423)}
for k,p in names.items():
    w=comp(p); out[k]=fmt([tri(w)]); out[k+"_comp"]=[round(100*v,1) for v in w]
out["E1"]=fmt([tri(cot[-1])]); out["E2"]=fmt([tri(cot[0])])
def base(an): return fmt([tri(np.array([1-an/100,an/100,0]))])
out["s2"]=base(69); out["pl55"]=base(55); out["pl64"]=base(64)
# liquid-plagioclase tie lines: An of plagioclase anchored on the figure
# (E2 -> An0, l4 -> An55, l3 -> An64, l2 -> An69, E1 -> An100), interpolated in arc length
P=np.array([tri(w) for w in cot]); s=np.r_[0,np.cumsum(np.hypot(*np.diff(P,axis=0).T))]
def at(frac):
    L=frac*s[-1]; i=np.searchsorted(s,L)-1; i=min(max(i,0),len(s)-2); t=(L-s[i])/(s[i+1]-s[i]); return P[i]+t*(P[i+1]-P[i])
def sof(p): return np.interp(0,[0],[0]) if False else None
anchors_pts=[tri(cot[0]),tri(comp((195,372))),tri(comp((254,347))),tri(comp((282,333))),tri(cot[-1])]
def arclen(pt):
    d=np.hypot(*(P-pt).T); i=int(np.argmin(d)); return s[i]
anchor_s=[arclen(p) for p in anchors_pts]; anchor_an=[0,55,64,69,100]
fan=[]
fl4,fl3,fl2=[arclen(p)/s[-1] for p in anchors_pts[1:4]]
print("fracs",round(fl4,3),round(fl3,3),round(fl2,3))
for frac,an in ((0.10,40),(fl4*0.55,50),(fl4,55),(fl3,64),(fl2,69),(0.72,80),(0.86,90)):
    p=at(frac); q=tri(np.array([1-an/100,an/100,0]))
    d=p-P_Di; t=-P_Di[1]/d[1]; proj=P_Di+t*d
    fan.append(dict(l=fmt([p]),pl=fmt([q]),proj=fmt([proj]),an=an))
out["fan"]=fan
# isotherm through l4 (schematic): Di-Ab edge at 30% Di, Ab-An edge at An 17
out["iso_DiAb"]=fmt([tri(np.array([0.70,0,0.30]))]); out["iso_AbAn"]=base(17)
out["iso_mid1"]=fmt([tri(np.array([0.66,0.06,0.28]))]); out["iso_mid2"]=fmt([tri(np.array([0.70,0.12,0.18]))])
json.dump(out,open("quiz1_coords.json","w"),indent=1)
for k in ("A_comp","l1_comp","l2_comp","l3_comp","l4_comp","s3_comp"): print(k,out[k])
print([ (f["an"]) for f in fan])
