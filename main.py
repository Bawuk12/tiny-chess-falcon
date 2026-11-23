# Falcon v4 - tiny chess engine (alpha-beta, quiescence, TT)
import json as J,os,urllib.request as H
U=os.getenv("MAKEFUN_ENV_URL") or exit()
post=lambda p,b:J.load(H.urlopen(H.Request(U+p,J.dumps(b).encode())))
V=dict(P=100,N=320,B=330,R=500,Q=900,K=2e4)
N,E,S,W=-10,1,10,-1
B=(-9,11,9,-11);R=(N,E,S,W)
D={'P':(N,-20,-11,-9),'N':(-19,-8,12,21,19,8,-12,-21),'B':B,'R':R,'Q':R+B,'K':R+B}
pst={p:tuple(V[p]+c*(2+10*(p in'NB')-4*(p=='K'))+r*r*(p=='P') for i in range(120)for r in[9-i//10]for c in[min(i%10-1,8-i%10,r,7-r)]) for p in"PNBRQK"}
from collections import namedtuple
class P(namedtuple("P","b s wc bc ep")):
 def gen(o,c=0):
  for i,p in enumerate(o.b):
   if p not in"PNBRQK":continue
   for d in D[p]:
    j=i+d
    while 1:
     q=o.b[j]
     if q in" PNBRQK":break
     if p=='P':
      if(d in(N,N+N) and(q!='.'or c and j>28))or(d==N+N and(i<81 or o.b[i+N]!='.'))or(d in(N+W,N+E) and q=='.' and j!=o.ep):break
      if j<29:yield (i,j,"Q");break
     if q!='.' or not c or(p=='P' and j==o.ep):yield (i,j,"")
     if p in"PNK" or q in"pnbrqk":break
     if not c and i==91 and o.b[j+1]=='K' and o.wc[0]:yield (j+E,j+W,"")
     if not c and i==98 and o.b[j-1]=='K' and o.wc[1]:yield (j+W,j+E,"")
     j+=d
 def rot(o):
  return P(o.b[::-1].swapcase(),-o.s,o.bc,o.wc,o.ep and 119-o.ep)
 def val(o,m):
  i,j,pr=m;p,q=o.b[i],o.b[j];s=pst[p][j]-pst[p][i]
  if q in"pnbrqk":s+=pst[q.upper()][119-j]
  if p=='P':
   if j<29:s+=pst[pr][j]-pst['P'][j]
   if j==o.ep:s+=pst['P'][109-j]
  return s
 def mv(o,m):
  i,j,pr=m;u=lambda b,x,c:b[:x]+c+b[x+1:]
  p,b,wc,bc,ep=o.b[i],o.b,o.wc,o.bc,0
  s=o.s+o.val(m);b=u(b,j,b[i]);b=u(b,i,'.')
  wc=(wc[0] and i!=91,wc[1] and i!=98);bc=(bc[0] and j!=21,bc[1] and j!=28)
  if p=='K':
   wc=(False,False)
   if abs(j-i)==2:b=u(b,91 if j<i else 98,'.');b=u(b,(i+j)//2,'R')
  if p=='P':
   if j<29:b=u(b,j,pr)
   if j-i==2*N:ep=i+N
   if j==o.ep:b=u(b,j+S,'.')
  return P(b,s,wc,bc,ep).rot()
MT=2e4
class Sr:
 def __init__(s):s.t={};s.H={};s.n=0;s.mx=0
 def F(s,p,a,b,d,pl):
  s.n+=1
  if s.n>s.mx:raise StopIteration
  if p.s<=-10e3:return-MT+pl
  k=(p.b,p.wc,p.bc,p.ep);e=s.t.get(k);bm=e[3] if e else None
  if e and e[2]>=d and(e[1]>=b if e[0]==1 else e[1]<=a if e[0]==2 else 1):return e[1]
  if d<=0:
   x=p.s+30*(p.b.count('B')>1)-30*(p.b.count('b')>1)
   if x>=b:return b
   a=max(a,x)
   for w,m in sorted(((p.val(m),m) for m in p.gen(1)),reverse=True):
    if x+w+150<a:break
    w=-s.F(p.mv(m),-b,-a,0,pl+1)
    a=max(a,w)
    if a>=b:return b
   return a
  if d>2 and pl:
   q=P(p.b[::-1].swapcase(),-p.s,p.bc,p.wc,0)
   if -s.F(q,-b,-b+1,d-2,pl+1)>=b:return b
  oa=a;best=-MT;bestm=None
  for n,(w,m) in enumerate(sorted((((m==bm)*9999+p.val(m)+s.H.get(m,0),m) for m in p.gen()),reverse=True)):
   r=d-1-(n>3 and d>2 and p.b[m[1]]=='.')
   v=-s.F(p.mv(m),-b,-a,r,pl+1)
   if r<d-1 and v>a:v=-s.F(p.mv(m),-b,-a,d-1,pl+1)
   if v>best:best=v;bestm=m
   if best>=b:
    if p.b[m[1]]=='.':s.H[m]=s.H.get(m,0)+d*d
    s.t[k]=(1,best,d,bestm);return best
   a=max(a,best)
  s.t[k]=(0 if best>oa else 2,best,d,bestm)
  return best
 def root(s,p,budget):
  s.mx=budget;best=None
  for d in range(1,12):
   try:
    s.F(p,-MT,MT,d,0)
    e=s.t.get((p.b,p.wc,p.bc,p.ep))
    if e and e[3]:best=e[3]
   except StopIteration:break
  return best
def fenpos(f):
 p=f.split();b=list(" "*20+(" "+"."*8+" ")*8+" "*20);s=0;j=21;w=tuple(c in p[2]for c in"QKqk")
 for ch in p[0]:
  if ch=='/':j+=2
  elif ch.isdigit():j+=int(ch)
  else:b[j]=ch;s+=pst[ch][j] if ch in"PNBRQK" else -pst[ch.upper()][119-j];j+=1
 q=P(''.join(b),s,w[:2],w[2:],p[3]!='-' and 4-10*int(p[3][1])+ord(p[3][0]))
 return q.rot() if p[1]=='b' else q
def choose(f,l):
 b=Sr().root(fenpos(f),100000)
 if not b:return l[0]
 if" b "in f:b=(119-b[0],119-b[1],b[2])
 v="".join(chr(96+x%10)+str(10-x//10)for x in b[:2])+(b[2].lower() if b[2] else"")
 return v if v in l else l[0]
while(g:=post("/game",{}))["status"]!="done":
 while g["status"]=="your_move":g=post("/move",{"game":g["game"],"move":choose(g["fen"],g["legal_moves"])})
