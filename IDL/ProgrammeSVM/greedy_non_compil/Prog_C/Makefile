CXX? = g++
#CFLAGS = -Wall -g -Wconversion -O3 -fPIC
CFLAGS = -Wall -m64 -g -Wconversion -O3 -fPIC
# -m32 : compilation pour 32 bits
SHVER = 1

all: svm-train svm-predict_dist svm-predict_prob svm-scale

lib: svm.o
	$(CXX) -shared svm.o -o libsvm.so.$(SHVER)

svm-predict_dist: svm-predict_avec_dist.c svm.o
	$(CXX) $(CFLAGS) svm-predict_avec_dist.c svm.o -o svm-predict-bin_dist -lm
svm-predict_prob: svm-predict_sans_dist.c svm.o
	$(CXX) $(CFLAGS) svm-predict_sans_dist.c svm.o -o svm-predict-bin_prob -lm
svm-train: svm-train.c svm.o
	$(CXX) $(CFLAGS) svm-train.c svm.o -o svm-train-bin -lm
svm-scale: svm-scale.c
	$(CXX) $(CFLAGS) svm-scale.c -o svm-scale-bin
svm.o: svm.cpp svm.h
	$(CXX) $(CFLAGS) -c svm.cpp
clean:
	rm -f *~ svm.o svm-train-bin svm-predict-bin_dist svm-predict-bin_prob svm-scale-bin