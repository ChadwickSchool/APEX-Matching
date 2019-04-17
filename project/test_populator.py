"""Python file to populate database with fake data"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Student, engine, Pref, Project

ENGINE = create_engine('mysql+pymysql://chadwick:godolphins@apex-matching.c0plu8oomro4.us-east-2.rds.amazonaws.com:3306/testdb')
Base.metadata.bind = ENGINE
DBSESSION = sessionmaker(bind=ENGINE)
session = DBSESSION()

A = Project(name='Lessons from a Student Athlete: Why the Grind Never Stops', session_number=1)
B = Project(name='Free Food!: What I learned about the LAUSDs free lunch program', session_number=2)
C = Project(name='Stories of Struggle, Victory, and Love: The Black Male Experience at Chadwick', session_number=3)
D = Project(name='Mirrors are your friend: Learning to love your body', session_number=4)
E = Project(name='AllRight: observing extreme political partisanship through FaceBook', session_number=1)
F = Project(name='A Safer E3nvironment: Chadwic3k and Mental Health', session_number=2)
G = Project(name='The Reality of the SAT/ACT', session_number=3)
H = Project(name='Emotional Abuse: A Closer Look at Pain Unseen', session_number=4)
I = Project(name='The Fifth Domain of Warfare', session_number=1)
J = Project(name='Nuclear Power: Friend or Foe?', session_number=2)
K = Project(name='Saving the Earth One Bite at a Time', session_number=3)
L = Project(name='O.E.,O.E., Never Much Love When We Go On O.E.', session_number=4)
M = Project(name='A Look into Americas Growing Health Epidemic', session_number=1)
N = Project(name='Mapping for Measles', session_number=2)
O = Project(name='A Dogs Purpose: Therapy Dogs', session_number=3)
P = Project(name='Ocean Friendly Restaurants in the South Bay', session_number=4)
Q = Project(name='Lessons from a Student Athlete: Why the Grind Never Stops', session_number=4)
R = Project(name='Triggered: What Most People Dont Know About Sports Injury', session_number=1)
S = Project(name='Spotlight: Using Childrens Theater to Enhance Multiple Intelligences', session_number=2)
T = Project(name='Bully the Bullies: The New Anti Cyberbullying Approach', session_number=3)
U = Project(name='Expanding Therapeutic Equestrian in Palos Verdes', session_number=4)
V = Project(name='Preventing Childhood Obesity in the South Bay', session_number=1)
W = Project(name='Healthy Habits To-Go: Ways to Efficiently Maintain a Balanced Lifestyle', session_number=2)
X = Project(name='Addressing the Systemic Risk of the Big Three: Depression, Anxiety, and Drug Abuse', session_number=3)
Y = Project(name='The Quality of Life in Spinal Muscular Atrophy Children', session_number=3)
Z = Project(name='Exposing the NCAA: The Rights of College Athletes', session_number=4)
AA = Project(name='AllRight: observing extreme political partisanship through FaceBook', session_number=1)
AB = Project(name='NEWSFLASH: Theater is more than just a form of entertainment', session_number=2)
AC = Project(name='Multiple Perspectives: Is my opinion really that controversial', session_number=3)
AD = Project(name='The Unshakeable Connection Between the Mind and Body', session_number=4)
AE = Project(name='Reading More Into Mental Illnesses and Homelessness: The Use of Libraries to Combat the Mentally Ill and Homeless of Long Beach', session_number=1)
AF = Project(name='Chadwick: Division 1 Sleep Deprivation', session_number=2)
AG = Project(name='The Anonymous Project', session_number=2)
AH = Project(name='Animal Advocacy: The Process of Meaningful Change', session_number=3)
AI = Project(name='A Look into the L.A. Foster Care System through Art', session_number=4)
AJ = Project(name='Eating Away at the Earth: The Meat Industrys Impact on the Environment and the Future of Meat', session_number=1)
AK = Project(name='Obesity: Quite a Large Problem if You Ask Me', session_number=2)
AL = Project(name='Stripping Away Negative Body Image: Medias Promotion of an Unattainable Ideal', session_number=3)
AM = Project(name='Blaming the Victims: The Mistreatment of Sexual Assault Cases at Educational Institutions', session_number=4)
AN = Project(name='The Spotlight Project', session_number=1)
AO = Project(name='If You Come To This Presentation, Ill Let You Nap', session_number=1)
AP = Project(name='Puzzled? Heres an Easy Way to Destress', session_number=2)
AQ = Project(name='Making Bank the Smart Way: What Chadwick Failed to Teach You', session_number=3)
AR = Project(name='Creating a Pen Pal Program to Help Orphans', session_number=4)
AS = Project(name='Houseless Not Homeless!', session_number=1)
AT = Project(name='Craving Companionship: Promoting Multigenerational Relationships to Combat Elderly Loneliness', session_number=2)
AU = Project(name='Programming Your Mind:  How To Edit Habits', session_number=3)
AV = Project(name='JAWS: Fixing Sharks Bad Reputations', session_number=4)
AW = Project(name='AllRight: observing extreme political partisanship through FaceBook', session_number=1)
AX = Project(name='Helping Hospitalized Children Cope with Stress', session_number=2)
AY = Project(name='Out of Tune: Revamping the Chadwick Instrumental Program', session_number=3)
AZ = Project(name='Solar Freakin Umbrellas: Implementing Solar Technology at Chadwick', session_number=4)
BA = Project(name='A Salute to Service Dogs', session_number=1)
BB = Project(name='Go the Frick to Sleep, You Fricking Fricks', session_number=2)
BC = Project(name='Not just a Brazilian Butt Workout: Another Type of Workout Vide', session_number=3)
BD = Project(name='Dancing in the rain during a drought: a water conservation guide for daily life', session_number=4)
BE = Project(name='From Assistants to Physicists: The Pursuit of Equality in STEM', session_number=1)
BF = Project(name='Guys And Dolls: A Look At Gendered Marketing Of Childrens Products', session_number=2)
BG = Project(name='Color Your Way Towards Happiness', session_number=3)
BH = Project(name='The California Coastline Takeover: Invasive Seaweed', session_number=4)
BI = Project(name='There Will Be Blood: Preventing Type 1 Diabetes Misdiagnosis', session_number=1)
BJ = Project(name='Stamping out Sexism in the Elementary School Classroom', session_number=2)
BK = Project(name='Capture Water Before it Goes', session_number=3)
BL = Project(name='Spotlight on the Students: Fostering Creativity in Chadwicks Stage Crew', session_number=4)
BM = Project(name='Why Should You be Grateful for Chadwick?', session_number=1)
BN = Project(name='Zoos: Born to be Wild', session_number=2)
BO = Project(name='How Many Bunnies Died for your Chapstick? Exposing Animal Testing in Cosmetics', session_number=3)
BP = Project(name='The ART of De-Stressing: Using Creativity to Promote Wellness', session_number=4)
BQ = Project(name='F#### of S####: What Can You Legally Say On Chadwicks Campus?', session_number=1)
BR = Project(name='Building Relationship with Children in Foster Care', session_number=2)
BS = Project(name='Protecting the Protected: Safeguarding Marine Protected Areas', session_number=3)
BT = Project(name='Infusing Objectivity and Individualism into Educating the Global Citizen', session_number=4)
BU = Project(name='Balancing the Numbers:  Supporting Female Engineers at Chadwick', session_number=1)
BV = Project(name='Are you a boy, girl, or other?: The importance of gender inclusion at school', session_number=2)
BW = Project(name='Empowering Girls in India Through Education', session_number=3)
BX = Project(name='Putting the Anti in Antibiotic Meat: The Pitfalls of Antibiotic Usage in Livestock Farming for Human Health and the Environment', session_number=4)
BY = Project(name='Protect Yourself Before You Wreck Yourself: The Dangers of Lifelong Sun Damage', session_number=1)
BZ = Project(name='Meditation: Methods to relieve stress and improve personal condition', session_number=2)
CA = Project(name='Fake News: the Cancer of Our Democracy', session_number=3)
CB = Project(name='What Happens To Homeless Pets In Our World', session_number=4)
CC = Project(name='Media and User Bias in the Digital Age: What You Can Do to Beat It', session_number=1)
CD = Project(name='Click on Sustainability: Reducing Your Carbon Footprint in Los Angeles', session_number=2)
CE = Project(name='Why Excessive Homework is Bad for High School Students', session_number=3)
CF = Project(name='Oh Brother!: The Conveniences and Costs of Mass Surveillance', session_number=4)
CG = Project(name='The Myth of Car Idling', session_number=1)
CH = Project(name='Need a hand? Providing a list of babysitters for families dealing with pediatric cancer', session_number=2)
CI = Project(name='"Youre So Pretty for a Black Girl": The Problem With White Beauty Ideals', session_number=3)
CJ = Project(name='Addressing Homelessness in My Community', session_number=4)
CK = Project(name='Mental Health: What do All Faculty Need to Know', session_number=1)
CL = Project(name='Healthy Habits To-Go: Ways to Efficiently Maintain a Balanced Lifestyle', session_number=2)
CM = Project(name='Addressing the Systemic Risk of the Big Three: Depression, Anxiety, and Drug Abuse', session_number=3)
CN = Project(name='The Quality of Life in Spinal Muscular Atrophy Children', session_number=4)
CO = Project(name='Kids These Days: Why Arent They Active?', session_number=1)
CP = Project(name='This Book Could Change Your Life: Combating Homophobia One Book at a Time', session_number=2)
CQ = Project(name='The Importance of Media Literacy in the Digital Age', session_number=3)
CR = Project(name='Apex under a Microscope: Employing Empathy to Ensure the Success of Chadwick Apex Projects', session_number=4)
CS = Project(name='Expanding the Admirals Role in the Chadwick Community', session_number=1)
none = Project(name='Not Matched', session_number=2)
session.add(A)
session.add(B)
session.add(C)
session.add(D)
session.add(E)
session.add(H)
session.add(I)
session.add(J)
session.add(K)
session.add(L)
session.add(M)
session.add(N)
session.add(O)
session.add(P)
session.add(Q)
session.add(R)
session.add(S)
session.add(T)
session.add(U)
session.add(V)
session.add(W)
session.add(X)
session.add(Y)
session.add(Z)
session.add(AA)
session.add(AB)
session.add(AC)
session.add(AD)
session.add(AE)
session.add(AF)
session.add(AG)
session.add(AH)
session.add(AI)
session.add(AJ)
session.add(AK)
session.add(AL)
session.add(AM)
session.add(AN)
session.add(AO)
session.add(AP)
session.add(AQ)
session.add(AR)
session.add(AS)
session.add(AT)
session.add(AU)
session.add(AV)
session.add(AW)
session.add(AX)
session.add(AY)
session.add(AZ)
session.add(BA)
session.add(BB)
session.add(BC)
session.add(BD)
session.add(BE)
session.add(BF)
session.add(BG)
session.add(BH)
session.add(BI)
session.add(BJ)
session.add(BK)
session.add(BL)
session.add(BM)
session.add(BN)
session.add(BO)
session.add(BP)
session.add(BQ)
session.add(BR)
session.add(BS)
session.add(BT)
session.add(BU)
session.add(BV)
session.add(BW)
session.add(BX)
session.add(BY)
session.add(BZ)
session.add(CA)
session.add(CB)
session.add(CC)
session.add(CD)
session.add(CE)
session.add(CF)
session.add(CG)
session.add(CH)
session.add(CI)
session.add(CJ)
session.add(CK)
session.add(CL)
session.add(CM)
session.add(CN)
session.add(CO)
session.add(CP)
session.add(CQ)
session.add(CR)
session.add(CS)
session.commit()

"""Create and add projects A-H to database"""
# project_A = Project(name='A', session_number=1)
# project_B = Project(name='B', session_number=1)
# project_C = Project(name='C', session_number=2)
# project_D = Project(name='D', session_number=2)
# project_E = Project(name='E', session_number=3)
# project_F = Project(name='F', session_number=3)
# project_G = Project(name='G', session_number=4)
# project_H = Project(name='H', session_number=4)
#
# SESSION.add(project_A)
# SESSION.add(project_B)
# SESSION.add(project_C)
# SESSION.add(project_D)
# SESSION.add(project_E)
# SESSION.add(project_F)
# SESSION.add(project_G)
# SESSION.add(project_H)
#
# SESSION.commit()
