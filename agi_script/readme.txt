# run tracing:
# press enter to finish 
./bin/gapit trace -api perfetto -perfetto config.pbtx -device "Google Pixel 5"

# after tracing, generate text:
./bin/traceconv text trace.perfetto trace.txt

# run data analyais:
python3 analysis.py
