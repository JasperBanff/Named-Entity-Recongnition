###############################################################################
# Docker file for testing COMP6714 16s2 Project
# 
# How to use:
#
#     1. Put this Dockerfile in the root of your project directory (where you 
#        put run.py)
#
#     2. Run the following command in this directory to build the testing 
#        environment and run the test. It's very slow for the first time
#        (Do not forget the trailing dot character!)
#
#          docker build -t 6714test .
# 
#     3. Run the following command to run the test, then you should see the 
#        test result
#
#          docker run --rm 6714test
#
#     4. If you have made any changes in your code, repeat Step 2 and Step 3
#        to test it again
#     
###################################################################################

# Basic
FROM ubuntu
MAINTAINER Yukai Miao <tjumyk@gmail.com>
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# Dependencies
RUN apt-get update && apt-get install -y wget bzip2 unzip libgomp1

# Setup Anaconda 3
RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/archive/Anaconda3-4.1.1-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh

# Update PATH
ENV PATH /opt/conda/bin:$PATH

# Install Spacy
RUN pip install spacy && \
    sputnik --name spacy --repository-url http://index.spacy.io install en==1.1.0

# Install Stanford CoreNLP
RUN wget --quiet http://nlp.stanford.edu/software/stanford-corenlp-full-2015-12-09.zip -O ~/corenlp.zip && \
    unzip -q ~/corenlp.zip -d /opt/corenlp && \
    rm ~/corenlp.zip

# Setup project skeleton files
RUN wget --quiet http://www.cse.unsw.edu.au/~cs6714/16s2/proj/6714-skeleton.tar -O- | tar xf - -C ~ && \
    mv ~/6714-skeleton ~/skeleton && \
    sed -i 's/\.\.\/stanford-corenlp-full/\/opt\/corenlp\/stanford-corenlp-full/' ~/skeleton/config.py

# Setup training data file
RUN mkdir ~/data && \
    wget --quiet http://www.cse.unsw.edu.au/~cs6714/16s2/proj/training.json -O ~/data/training.json

# Add students' code
ADD . /root/code

# Prepare test directory
RUN cp -r ~/code ~/test && \
    rm ~/test/Dockerfile && \
    cp ~/skeleton/config.py ~/test && \
    cp ~/skeleton/relation.py ~/test && \
    cp ~/skeleton/run.py ~/test && \
    cp ~/data/training.json ~/test

# Set working directory
WORKDIR /root/test

# Run the test
CMD [ "/bin/bash", "-c", "python run.py training.json"]

