## TEAM 2 FUNCTIONAL ANNOTATION

#### MEMBERS:
Rohan Bhukar, Gabriel Cruz, Jinyoung Eum, Rohini Janivara, Caeden Meade, Aditya Natu, Sami Belhareth
  ___

#### INTRODUCTION

Functional annotation is defined as the process of collecting information about and describing a (genome feature’s) biological identity—its various aliases, molecular function, biological role(s), subcellular location, and its expression domains within the (organism). When we try to talk about Functional Annotation in context of real-world applications and with the Main goal of this present course genome-enabled outbreak investigation comes into discussion. While analysing the genome and figuring out the functions of the respective features of that genome, the analysis can help us, one in determining what essentially does the genome encode, and second wrt the Question of interest : who is related to whom (the Evolution part of the problem statement) to help decipher the outbreak source.

Through this current implementation, we will perform full functional annotation on the genes as well as proteins predicted by the Team-2 Group-2 Gene Prediction members, while focusing on features of interest such as Antimicrobial resistance genes, virulence factors etc. which have more weightage to Outbreak investigations of unknown species. 
  ___
#### TOOLS Required:
The following tools and required environments need to be available to run the pipeline.
-	conda
- git
-	Perl
-	make
- Python 2.7
- [USEARCH](https://www.drive5.com/usearch/download.html)
- [DeepARG](https://bench.cs.vt.edu/deeparg)
- [InterproScan](https://www.ebi.ac.uk/interpro/download/)
- [MicrobesOnline](http://www.microbesonline.org/)
- [SignalP 5.0](https://services.healthtech.dtu.dk/service.php?SignalP-5.0)
  
  
#### TOOLS USED:  
- Clustering: USEARCH
- Homology Based: DeepARG, MicrobesOnline, VFDB, InterproScan
- Ab-initio Based: SignalP 5.0, CRT, Phobius, PlasmidSeeker
  
  
#### 1. CLUSTERING Approach: USEARCH

Shared ancestry can lead to similarity between sequences which often leads to shared function. As a result, clustering sequences into groups based on function can reduce the redundancy in our functional annotation analysis. Clustering tools reduce the computational time of functional annotation tools and lowers storage cost. We have clustered both amino acid sequences as well as nucleotide sequences for inputs down the pipeline as per respective tools. 

USEARCH is a unique sequence analysis tool with thousands of users world-wide. USEARCH offers search and clustering algorithms that are often orders of magnitude faster than BLAST. It's a widely used method for sequence clustering of proteins and nucleotides that implements a greedy-incremental heuristic algorithm which sorts larger set of sequences by order centroids are represents of clusters identity is computed using kmers, global alignment.

RUN Command:
> <uSearch_path> -cluster_fast <input_fasta> -id <identity_threshold> -centroids <centroids_output_file> -uc <uclust_file>
  ___
#### 2. HOMOLOGY BASED TOOLS

DeepARG is a homology-based, deep learning tool that annotates antibiotic resistance genes in metagenomes. There are two types of pre-trained models: DeepARG-SS for short sequence reads from Next Generation Sequencing technologies, and DeepARG-LS for long, gene-like sequences. Users can a model if they wish. DeepARG uses UNIPROT database, which is a custom database incorporating CARD and ARDB.

RUN Command:
> deeparg predict --model <SS or LS> --type <nucleotide or protein> --input <intput_file> --out <output_file> -d <database_location>

#### Antimicrobial Resistance Genes: DeepARG



#### Protein coding regions : InterproScan

Interproscan is a homology based tool that performs functional annotation on input nucleotide or protein sequences by searching againsts Interpro databases. With the incorporation of large databases, Interproscan allows users to gain much more detailed annotations. From the Interpro databases, Interproscan classifies proteins into families and predicts domains and important sites. However, due to a use of large databases, long run time is expected.

Interproscan databases used:
* CDD
* COILS
* Gene3D
* HAMAP
* MobiDBLite
* PANTHER
* Pfam

RUN Command: 
> ./interproscan.sh -appl CDD,COILS,Gene3D,HAMAP,MobiDBLite,PANTHER,Pfam -i <input_file> -f gff3 -o <output_file>

#### Operons : MicrobesOnline
MicrobesOnline has been providing a community resource for comparative and functional genome analysis i.e. It provides operon predictions for every bacterial and archaeal genome. Within any particular genome it predicts weather a pair of adjacent genes is present in the same operon on not based on intergenic distance between them, the correlation of their expression patterns, and weather they belong to the same functional category.

RUN Command: 

> •	makeblastdb -in <ecoli_fasta_file> -dbtype prot -out <database_name> 
  __

> •	blastp -query <prot_cluster_file> -db <database_name> -evalue 0.01 -outfmt 6 -out <prot_cluster.hits.txt> -num_threads 4 -max_target_seqs 1 -max_hsps 1
  __

#### Virulence factors: VFDB
Virulence Factor Database which provides a well-organized and comprehensive resource for prediction of virulence factors within the bacterial pathogens. In VFDB, one can find information about the structural features of the virulence factors, functions and mechanisms used by the pathogens for invading host defense mechanisms and causing pathogenicity. 

RUN Command:

> •	makeblastdb -in VFDB_setB_nt.fas -dbtype 'nucl' -out <database_name>
  ___

> •	blastn -db <database_name> -query <nt_cluster_file> -out <output.cfinal.fna> -outfmt 6 -perc_identity 100 -max_hsps 1 -max_target_seqs 1 -num_threads 4
  ___

 
#### 3. AB-INITIO Approach


#### Signal peptides: SignalP 5.0
SignalP v5.0 is a deep-learning based signal peptide prediction software optimized for transfer learning. Signal peptides are an important feature to characterize as they inform us of the destination of the translated protein. SignalP can predict three types of signal peptides:Sec/SPI,Sec/SPII and Tat/SPI. Sec/SPI are signal peptides that go through the secratory pathway of the organism and end upoutside the membrane. Sec/SPII are signal peptides for lipoproteins that end up in the membrane. Tat/SPI are signal peptides much like Sec/SPI but go through the TAT pathway.

RUN Command:

> signalp -fasta <input_file> -org gram- -gff3 -format short
#### CRISPR regions: CRT

CRISPR stands for Clustered Regularly Interspaced Short Palindromic Repeats. CRISPRs are formed with repeat sequences and spaces between those sequences. CRISPR is very common in prokaryotes. Within spaces between repeat sequences, prokaryotes keep a genetic memory of viruses that have invaded it in the past. Thus, the system will later recognize and destroy the invaded viruses. With identifying CRISPRs, more personalized medicine is available. Mainly CRISPR have been using CRISPR to detect specific targets, such as DNA from cancer-causing viruses.

CRISPR Recognition Tool (CRT) is a tool that identifies CRISPR repeats and spaces in genomes or metagenomes. CRT uses an algorithm that searches for exact k-mer matches and has a simple sequential scan of a DNA sequence to detect repeats directly on the input data.

RUN Command:
> java -cp <CRT1.2-CLI.jar_path> crt <input_file> <output_file>

#### Plasmids: PlasmidSeeker
Plasmids are extra-chromosomal regions of DNA which may be passed between certain bacteria, conferring upon the recipients virulence factors, antibacterial resistence and more.

The presence of particular genes on particular plasmids, or homology with known reference plasmids may be used to annotate input genomes. To do so, PlasmidSeeker makes use of an input database, searching for homologous regions among the database's collection of reference plasmids. A reference genome which ideally is closely related to the input genome is supplied by PlasmidSeeker's users to facilitate the program's search. PlasmidSeeker analyses k-mer abundances to distinguish between chromosomal genome regions and plasmid regions.

Run Command:
> perl plasmidseeker.pl -i <input isolate FASTQ> -d <database directory path> -b <reference bacterium FASTA path> -o <output file name>

#### Transmembrane Domains: Phobius
Phobius uses a Hidden Markov Model to combine predictions signal peptide and transmembrane topology. These two classes of proteins have high similarity in the hydrophobic regions, making individual predictions error-prone. By combined modeling, Phobius increases the prediction accuracy, especially in proteins that have both kinds of domains.

Transmembrane proteins are anchored in the phospholipid bilayer of the cell membrane. They have multiple functions including transportation of molecules across the membrane, signal transduction, cell recognition, and enzymatic roles. They are important for pathogen detection and study since they are crucial biomarkers. They have two-thirds of all known druggable targets. Signal peptides are short amino acid sequences at the N-terminal of proteins, which can guide the proteins to their intended location outside the cell membrane.

Phobius takes in amino acid fasta files as input and provides an output of .out files that explains the number of amino acids in the transmembrane domain and whether or not the protein contains a signal peptide. The long output with graphics format also provides a posterior probability plot that shows the localization probabilities of different amino acids of the protein.

RUN Command:

> perl phobius.pl -short input.faa > output.out


#### CITATIONS

- Almagro Armenteros, J.J., Tsirigos, K.D., Sønderby, C.K. et al. SignalP 5.0 improves signal peptide predictions using deep neural networks. Nat Biotechnol 37, 420–423 (2019). https://doi.org/10.1038/s41587-019-0036-z

- Arango-Argoty, G., Garner, E., Pruden, A. et al. DeepARG: a deep learning approach for predicting antibiotic resistance genes from metagenomic data. Microbiome 6, 23 (2018). https://doi.org/10.1186/s40168-018-0401-z

- Bland C, Ramsey TL, Sabree F, Lowe M, Brown K, Kyrpides NC, Hugenholtz P. CRISPR recognition tool (CRT): a tool for automatic detection of clustered regularly interspaced palindromic repeats. BMC Bioinformatics. 2007 Jun 18;8:209. doi: 10.1186/1471-2105-8-209. PMID: 17577412; PMCID: PMC1924867.

- Chen, L., Yang, J., Yu, J., Yao, Z., Sun, L., Shen, Y., & Jin, Q. (2005, January 01). VFDB: A reference database for bacterial virulence factors. Retrieved March 23, 2021, from https://academic.oup.com/nar/article/33/suppl_1/D325/2505203

- Dehal, P., Joachimiak, M., Price, M., Bates, J., Baumohl, J., Chivian, D., . . . Arkin, A. (2010, January). MicrobesOnline: An integrated portal for comparative and functional genomics. Retrieved March 23, 2021, from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2808868/

- Käll L, Krogh A, Sonnhammer EL. Advantages of combined transmembrane topology and signal peptide prediction--the Phobius web server. Nucleic Acids Res. 2007;35(Web Server issue):W429-W432. doi:10.1093/nar/gkm2562. Käll L, Krogh A, Sonnhammer EL. A combined transmembrane topology and signal peptide prediction method. J Mol Biol. 2004 May 14;338(5):1027-36. doi: 10.1016/j.jmb.2004.03.016. PMID: 15111065.

- Li, Haifeng, et al. "Analysis of the Antigenic properties of membrane proteins of Mycobacterium tuberculosis." Scientific reports 9.1 (2019): 1-10. Cournia Z, Allen TW, Andricioaei I, et al. Membrane Protein Structure, Function, and Dynamics: a Perspective from Experiments and Theory. J Membr Biol. 2015;248(4):611-640. doi:10.1007/s00232-015-9802-0

- Robert C. Edgar, Search and clustering orders of magnitude faster than BLAST, Bioinformatics, Volume 26, Issue 19, 1 October 2010, Pages 2460–2461, https://doi.org/10.1093/bioinformatics/btq461

- Roosaare M, Puustusmaa M, Möls M, Vaher M, Remm M. PlasmidSeeker: identification of known plasmids from bacterial whole genome sequencing reads. PeerJ. 2018 Apr 2;6:e4588. doi: 10.7717/peerj.4588. PMID: 29629246; PMCID: PMC5885972.

- Quevillon E, Silventoinen V, Pillai S, Harte N, Mulder N, Apweiler R, Lopez R. InterProScan: protein domains identifier. Nucleic Acids Res. 2005 Jul 1;33(Web Server issue):W116-20. doi: 10.1093/nar/gki442. PMID: 15980438; PMCID: PMC1160203.
