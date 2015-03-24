all: wq_rc.py

wq_rc.py: wq.qrc
	pyrcc4 -o $? $+
