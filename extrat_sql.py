import mysql.connector as sql

Bdd = sql.connect(
  host="localhost",
  user="root",
  password="",
  database="resultatsnuitsommeil"
)

cur = Bdd.cursor()

requeteProc= "CALL nbrapnee "

#nbrapneeProc = "EXEC Bdd[nbrapnee]@id_nuit='1'"
#nrbhypopnee= cur.execute("exec resultatsnuitsommeil.nrbhypopnee('id_nuit')")
#nrbrera= cur.execute("exec resultatsnuitsommeil.nrbrera('id_nuit')")
#nrbtotalevenement= cur.execute("exec resultatsnuitsommeil.nrbtotalevenement('id_nuit')")

#myresult = cur.fetchall()

print(nbrapneeProc)