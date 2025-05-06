#qui frasi per testare l'applicazione nel campo pratico e vedere quando mi da risultati e confronto
#risultati ottenuti con la query
import run 



'''
"I would like to go in Rome for 3 days, can you reccomend for me the best things to visit?",
            "Hello, can you say me the current situation about the security in France, is safe?", 
            "Tell me the last news about the warning weather alert in Valencia.",
            "Some concerts in Ljubljana for tomorrow.",
            "Events or concerts rock in Rome today",
            'I am going in Milan in the 1 June, there are concert by Jerry Cantrell?',
            "Can you write for me the best places where i can eat in Prague",
            "What are the typical food in Naples? and in Paris?",
            "I am going in Berlin, tell me the temperature for friday."
            "Search for me the ticket by train or bus to go from Rome tomorrow to Paris, to return sunday"
'''

#"I want visit Zagreb for 1 day, tell me the best things to visit.",

dt_query = [
            
            ]


output_path = "./testing/real_result.txt"
from pathlib import Path
output_path = Path(output_path)

fp = open(output_path,"a")

for query in dt_query:
    text,diz = run.main(query)
    print(str(diz))
    # salvo in un file query,text,diz
    fp.write(query)
    fp.write("\n")
    fp.write(text)
    fp.write("\n")
    fp.write(str(diz))
    fp.write("\n\n\n")

fp.close()
