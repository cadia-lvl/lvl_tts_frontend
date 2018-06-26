#Sparrowhawk set up

Sparrowhawk is the open version of Google's Kestrel text normalization engine. It has several prerequisites, the following is the set up process followed from https://github.com/danijel3/SparrowhawkTest

Recommends creating a virtual environment:

    virtualenv sparrowhawk

    cd sparrowhawk

##OpenFST
  
Get and install OpenFST - we will install all packages of relevant software in /usr/local:

    wget http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.6.3.tar.gz
    tar xvf openfst-1.6.3.tar.gz 
    cd openfst-1.6.3
 
    ./configure --prefix=/usr/local --enable-far --enable-linear-fsts --enable-pdt --enable-mpdt --enable-grm
    make
    make install

##Thrax

Get and install Thrax:

    cd ..
    wget http://openfst.org/twiki/pub/GRM/ThraxDownload/thrax-1.2.3.tar.gz
    tar xvf thrax-1.2.3.tar.gz 
    cd thrax-1.2.3
	
    ./configure --prefix=/usr/local
    make
    make install

##RE2
	
Get and install RE2:

    cd ..
    git clone https://github.com/google/re2
    cd re2/
    make

##Protobuf
	
Get and install Protobuf:

    cd ..
    git clone https://github.com/google/protobuf

If you don't have autoconf, automake and libtools installed, needed for Protobuf:

    curl -O -L http://ftpmirror.gnu.org/autoconf/autoconf-2.69.tar.gz
    tar -xzf autoconf-2.69.tar.gz 
    cd autoconf-2.69

    ./configure
    make
    make install

    cd ..
    curl -O -L http://ftpmirror.gnu.org/automake/automake-1.15.tar.gz
    tar -xzf automake-1.15.tar.gz 
    cd automake-1.15

    ./configure
    make
    make install
	
    cd ..
    curl -OL http://ftpmirror.gnu.org/libtool/libtool-2.4.6.tar.gz
    tar -xzf libtool-2.4.6.tar.gz 
    cd libtool-2.4.6
	
    ./configure
    make
    make install
 
Continue with installing Protobuf:
  
    cd ..
    cd protobuf/
    ./autogen.sh 
    ./configure --prefix=/usr/local
    make
    make check

Make check might show some errors, you should be able to continue anyway ...

    make install


##Sparrowhawk

And, finally, install Sparrowhawk:

    cd ..
    git clone https://github.com/google/sparrowhawk
    cd sparrowhawk/

The following is for Mac OSX, Linux users can probably just call ./configure directly:

    CPPFLAGS=-I/usr/local/include LDFLAGS=-L/usr/local/lib ./configure
    make
    make install

If all the above went well, everything should be set up by now.

#### Run Sparrowhawk

First, build the demo grammars:

    cd documentation/grammars/en_toy/classify/
    thraxmakedep tokenize_and_classify.grm 
    make
    cd ..
    cd verbalize
    thraxmakedep verbalize.grm 
    make
    cd ..
    cd verbalize_serialization/
    thraxmakedep verbalize.grm 
    make

And run a test from the /grammars folder:

    cd ../..
    $HOME/sparrowhawk/src/bin/normalizer_main --config=sparrowhawk_configuration.ascii_proto --multi_line_text < test.txt > out.txt
    cat test.txt 

"The train left at 3:30 from Penn Station on Jan. 3, 2010. Mr. Snookums
was on the train carrying $40.25 (£30.60) of Belgian chocolate in a 3kg box that
was 20cm wide."

    cat out.txt
	
"The train left at three thirty from Penn Station on January the third twenty ten sil
Mr. Snookums was on the train carrying forty dollars and twenty five cents sil thirty pounds and sixty pence sil of Belgian chocolate in a three kilograms box that was twenty centimeters wide sil"


