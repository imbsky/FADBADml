include ../../config

INCLUDES += -I ../../lib fadbad.cma

CMO = \
	fode.cmo \
	interval.cmo \
	affineForm.cmo \
	sets.cmo \
	taylorModel.cmo \
	continuousIntegrator.cmo \
	exampleReachability.cmo

build: objects exampleReachability.byte

run: exampleReachability.byte exampleReachability.gp
	./exampleReachability.byte -tend 2.0 -dt 2e-2 -order 3 -threshold 3e-3 > data.dat
	gnuplot exampleReachability.gp
	xdg-open picture.svg

objects: $(CMO)

sets.cmo: interval.cmo affineForm.cmo

exampleReachability.byte: INCLUDES += interval.cmo affineForm.cmo sets.cmo taylorModel.cmo continuousIntegrator.cmo

clean:
	rm -rf *.cm[ixo] *.byte .depend
	rm -f data.dat picture.svg

cleanall: clean

-include .depend
.depend:
	ocamldep *.ml *.mli > .depend
