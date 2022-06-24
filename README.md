# Misurare l'Impatto della Produzione Scientifica. 
## Risultati di un'Indagine Bibliometrica sul Teorema di Bell. 

La repository contiene i codici scritti per la realizzazione del lavoro di tesi magistrale. Quest'ultimo è stato articolato intorno a due domande di ricerca fondamentali: 
1) La storia del Teorema di Bell ci racconta davvero una storia di completo disinteresse nei confronti del lavoro del fisico irlandese come molta letteratura sul tema lascia intendere? 
2) E possibile ottenere una visualizzazione della comunità di ricerca che si è interessata al risultato raggiunto da Bell nel 1964?


### Analisi Storica 
Rispondere alla prima domanda ha richiesto un lavoro quantitativo che prendesse come _input_ due differenti file **.csv** e offrisse come _output_ una serie di visualizzazioni che permettessero di ottenere a colpo d'occhio le informazioni necessarie. Lo script prodotto a tale scopo `Bell1.0.py` deve adattarsi alla differente struttura dei due file in _input_ che contengono i dati ottenuti da due differenti banche dati: 
- Per quanto riguarda i dati riguardanti le pubblicazioni successive al 1985 si è attinto al bacino di _Web of Science_
- Per quanto riguarda i dati riguardanti le pubblicazioni precedenti al 1985 si è, invece, fatto riferimento al database di _Google Scholar_

![This is an image](Images/cit_per_year_tot.png)

Questo permette di osservare l'andamento citazionale totale che coinvolge _On the Einstein Podolski Rosen paradox_, come anche di osservare la crescita di citazioni anno per anno. 

![This is an image](Images/cit_per_year.png)

Si tenga presente che la raccolta di dati è stata effettuata a metà 2020. Per cui le citazioni relative a tale anno sono necessariamente incomplete. 



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
