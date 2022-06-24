# Misurare l'Impatto della Produzione Scientifica. 
## Risultati di un'Indagine Bibliometrica sul Teorema di Bell. 

AVVERTENZA: 
La qualità dei codici qui pubblicati non è particolarmente raffinata. Tali codici sono il risultato di un lungo lavoro
e di diverse manipolazioni. Moltoo spesso ho imparato il funzionamento di alcuni moduli importati mentre li stavo utilizzando 
e questo ha prodotto un risultato che non sempre è il più efficace, soprattutto per quanto riguarda la leggibilità e la pulizia.
Tuttavia il lavoro svolto permette di ottenere dei risultati verificabili e replicabili. Sarebbe interessante provare a riscrivere 
in un secondo momento tutti gli script qui collezionati, eliminando le parti superflue e rendendo più snello e pulito il lavoro. 


Breve spiegazione del lavoro svolto dai file .py:

BELL1.0.PY
È stato utilizzato per la maggior parte delle analisi di titpo quantitativo. La parte relativa agli script è divisa in due blocchi, 
ognuno dei quali prende come oggetto un differente file .csv (questo a causa del fatto che una parte dei dati è stata ottenuta attraverso 
WoS e una parte è stata raccolta manualmente via Google Scholar. Questo ha prodotto due tabelle contenti informazioni diverse e organizzate
in maniera lievemente differente). Lo script esegue:
- la raccolta del numero di citazioni totali dell'articolo di Bell(1964) divise per anno 
- la raccolta cumulativa del numero di citazioni totali dell'articolo di Bell(1964)

per cicli di dieci anni: 
- la raccolta degli n autori più frequenti (tra quelli che citano l'articolo preso in esame)
- la raccolta delle n fonti più frequenti
- la raccolta delle n parole più frequenti negli abstract
- la raccolta delle n parole più frequenti nei titoli 

- la stampa dei grafici che mostrano l'andamento delle citazioni sulle riviste che hanno collezionato più di un certo numero n di articoli 
che citavano (Bell1964)

relativamente alla parte riguardante i dati post '85: 
- l'analisi delle affiliazioni degli autori più frequenti (intesa per singoli dipartimenti e non per università). 

SBMTM.PY
È il modulo scritto da Gerlach per fare topic modeling con le correzioni suggerite da da Hanningam. Per maggiori informazioni a riguardo
il rimando è al lavoro di Gerlach:

https://advances.sciencemag.org/content/4/7/eaaq1360.full

https://github.com/martingerlach/hSBM_Topicmodel

TOPICMODELING.PY (e TOPICMODELING85_20.PY)
Sono i due script con i quali applico il modello di Gerlach ai dati citazionali raccolti. (I due file lavorano sui due .csv di cui sopra. 
Dopo aver stampato il grafo lo script produce una serie di file json che permettono di visualizzare e lavorare sulle informazioni contenute
nel grafo stesso. 

JSONANALYZER.PY
Lo script produce visualizzazioni grafiche dei dati contenuti all'interno dei file JSON per ogni livello richiesto. In particolar modo: 
le informazioni contenute nei file riguardanti i topics vengono visualizzate sottoforma di istogrammi, mentre il rapporto tra cluster di 
documenti e topics viene visualizzato attraverso la stampa di matrici (e matrici densità). 


L'insieme degli output prodotti attraverso i codici qui presentati è disponibile al seguente indirizzo: https://mega.nz/folder/d1JmxTiT#5-59GtTFdo2mb1VVLjEG7A
