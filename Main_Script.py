import os
#create a directory for all files to be added to
directory = "PipelineProject_Alec_Loftus"
parent_dir = os.path.abspath(os.getcwd())

path = parent_dir + "/" + directory
os.mkdir(path)
print("Directory '%s' created" % directory)
os.chdir(directory)
print('All outfiles will be written within the path ' + os.path.abspath(os.getcwd()))

dataset_type = input("Which dataset are you running?(full/test): ")

if dataset_type == "full":
    #all of the SRA files to be used
    list_of_links = ["https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR5660030/SRR5660030","https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR5660033/SRR5660033","https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR5660044/SRR5660044","https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR5660045/SRR5660045"]

    #do i need to do this step here or can i include the wget files
    #in my repository

    #generate list for all file names to be tracked
    filenames = []
    for link in list_of_links:
        filenames.append(link[-10:])
        command = 'wget ' + link
        os.system(command)
    #generate the paired end files
    for file in filenames:
        print('Now fastq dumping file ' + file)
        paired_command = "fastq-dump -I --split-files " + file
        os.system(paired_command)
    dataset_path = os.path.abspath(os.getcwd())
    #test fastq-dump for how many reads to take
    #or cut however many lines (multiple of 4 left)
elif dataset_type == "test":
    filenames = ['SRR5660030_test','SRR5660033_test','SRR5660044_test','SRR5660045_test']
    dataset_path = '../test_data/'

print(dataset_path)
#STEP 2#############################################################################################################################################################

import logging
logging.basicConfig(
    level = logging.INFO,
    format = '{asctime} {levelname:<8} {message}',
    style = '{',
    filename = 'PipelineProject.log',
    filemode = 'w')


reads_before = []
for file in filenames:
    file_length_command = 'wc -l < ' + dataset_path + file + '_1.fastq'
    reads_before.append(int(os.system(file_length_command)/4))
print(reads_before)


#pull reference genome from repository file and create HCMV index using bowtie2-build command
bowtie2_build_command = 'bowtie2-build ../HCMV_reference_genome.fasta HCMV'
os.system(bowtie2_build_command)

for file in filenames:
    bowtie2_command = 'bowtie2 --quiet -x HCMV -1 ' + dataset_path + file + '_1.fastq -2 ' + dataset_path + file + '_2.fastq -s ' + file + 'map.sam --al-conc-gz ' + file + '_mapped_%.fq.gz'
    os.system(bowtie2_command)


reads_after = []
for file in filenames:
    file_length_command = 'wc -l < ' + file +  '_mapped_1.fq.gz'
    reads_after.append(int(os.system(file_length_command)/4))


logging.info("Donor 1 (2dpi) had " + str(reads_before[0]) + " read pairs before Bowtie2 filtering and " + str(reads_after[0]) + " read pairs after.\n")

logging.info("Donor 1 (6dpi) had " + str(reads_before[1]) + " read pairs before Bowtie2 filtering and " + str(reads_after[1]) + " read pairs after.\n")

logging.info("Donor 3 (2dpi) had " + str(reads_before[2]) + " read pairs before Bowtie2 filtering and " + str(reads_after[2]) + " read pairs after.\n")

logging.info("Donor 3 (6dpi) had " + str(reads_before[3]) + " read pairs before Bowtie2 filtering and " + str(reads_after[3]) + " read pairs after.\n")



#STEP 3#############################################################################################################################################################

#spades to assemble all 4 transcriptomes together

#os.system(SPAdes_assembly_script.py)
spades_command = 'spades.py -k 77,99,127 -t 2 --only-assembler --pe-1 1 ' + filenames[0] + '_mapped_1.fq.gz --pe-2 1 ' + filenames[0] + '_mapped_2.fq.gz --pe-1 2 ' + filenames[1] + '_mapped_1.fq.gz --pe-2 2 ' + filenames[1] + '_mapped_2.fq.gz --pe-1 3 ' + filenames[2] + '_mapped_1.fq.gz --pe-2 3 ' + filenames[2] + '_mapped_2.fq.gz --pe-1 4 ' + filenames[3] + '_mapped_1.fq.gz --pe-2 4 ' + filenames[3] + '_mapped_2.fq.gz -o SPAdes_assembly/'
os.system(spades_command)

logging.info('spades.py -k 77,99,127 -t 2 --only-assembler --pe-1 1 ' + filenames[0] + '_mapped_1.fq.gz --pe-2 1 ' + filenames[0] + '_mapped_2.fq.gz --pe-1 2 ' + filenames[1] + '_mapped_1.fq.gz  --pe-2 2 ' + filenames[1] + '_mapped_2.fq.gz --pe-1 3 ' + filenames[2] + '_mapped_1.fq.gz --pe-2 3 ' + filenames[2] + '_mapped_2.fq.gz --pe-1 4 ' + filenames[3] + '_mapped_1.fq.gz --pe-2 4 ' + filenames[3] + '_mapped_2.fq.gz -o SPAdes_assembly/')

#STEP 4#############################################################################################################################################################

#os.system(total_number_of_contigs.py)


#STEP 5#############################################################################################################################################################

