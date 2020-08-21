import random as r

# Probability distribution of each syllable
syllables = list('11111222222222222222222222333333333333333344456')

# Consonants that can start a word
c_s = "w,wr,r,t,tw,th,thr,y,p,ph,pr,d,dr,f,fr,fl,g,gl,gr,gh,h,j,k,kl,kr,c,ch,cl,cr,z,v,b,br,n,m,s,sl,sk,sm,sn,st,fr,l".split(',')

# Consonants in the middle of a word
c_m = "w,ws,wd,wr,wt,wth,wp,wk,wn,wm,wb,r,rt,rp,rm,rn,rc,rb,rl,rk,rd,rs,rth,rch,t,th,thr,tch,t,ts,y,ys,p,pl,pr,ps,s,sh,sch,st,sm,sn,dr,ddl,dd,f,ff,fr,fl,mp,mn,gs,gl,j,k,kl,kr,kw,l,ll,lm,ls,sl,sk,z,zz,ch,cr,ct,cl,ck,v,b,br,bs,bl,n,ns,m,ms,nth".split(',')

# Consonants that can end a word
c_e = "w,ws,wd,wt,wth,wk,r,rt,rp,rm,rn,rc,rb,rl,rk,rd,rs,rth,rch,t,th,tch,t,ts,y,p,ps,s,sh,sch,st,,ff,,mp,gs,k,ll,ls,sk,ch,ct,ck,v,b,bs,n,ns,m,ms,nth".split(',')

# Vowels
v = "a,e,i,o,u,ae,ao,ei,eu,ea,oo,ou,oi,oy,ay,ey,y".split(',')


# Rules for making the words
def make_word(syllables):
  out = ""
  combos = []

  if syllables == 1:
    vowel = 1
  else:
    vowel = r.randrange(2)

  for i in range(syllables):
    if vowel:
      vowel = 0
      out += r.choice(v)
    else:
      vowel = 1
      if i == 0:
        out += r.choice(c_s)
      elif i == syllables - 1:
        out += r.choice(c_e)
      else:
        out += r.choice(c_m)

  return out


# Create the text
capitol = True
dictionary = []
density = 500
for i in range(1000000):
  if r.randrange(1000) < density and dictionary:
    word = r.choice(dictionary)
  else:
    word = make_word(int(r.choice(syllables)))

  dictionary.append(word)


real_out = ''
for i in range(32269):
  out = r.choice(dictionary)

  if capitol:
    out = out.title()
  capitol = False

  if i == 0:
    capitol = True

  if i == 32268:
    out += '.'
  else :
    punc = r.randrange(1000)
    if punc < 50:
      out += '.'
      capitol = True
    elif punc < 200:
      out += ','

  real_out += out + ' '

with open('rand_text.txt', 'w') as f:
  f.write(real_out)
