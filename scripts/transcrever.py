#!/usr/bin/env python3
"""Transcreve o áudio de uma aula, de graça, nesta máquina (Whisper large-v3).

Uso: python3 -I scripts/transcrever.py <audio> <saida.txt> [--modelo large-v3] [--prompt "termos da aula"]

Converte o áudio para 16 kHz mono com o ffmpeg e transcreve em português com o
faster-whisper (instala sozinho se faltar). A saída tem uma linha por trecho,
com o tempo no começo ("[00:12:31] ..."), para a apostila citar o momento da fala.
O progresso sai no stderr. Lento: no processador desta máquina, conte com
algumas horas para uma aula de 2 h; rode em segundo plano.
"""
import argparse
import os
import subprocess
import sys
import time

p = argparse.ArgumentParser()
p.add_argument('audio')
p.add_argument('saida')
p.add_argument('--modelo', default='large-v3')
p.add_argument('--prompt', default='Aula de Medicina em português do Brasil.')
a = p.parse_args()

try:
    from faster_whisper import WhisperModel
except ImportError:
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--break-system-packages', '-q', 'faster-whisper'], check=True)
    from faster_whisper import WhisperModel
import numpy


def hms(s):
    s = int(s)
    return f'{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}'


# O ffmpeg decodifica (o leitor de áudio embutido do faster-whisper falha com
# algumas versões do PyAV): 16 kHz mono em float32, direto para a memória.
bruto = subprocess.run(['ffmpeg', '-v', 'error', '-i', a.audio, '-f', 'f32le', '-ac', '1', '-ar', '16000', '-'],
                       capture_output=True, check=True).stdout
audio = numpy.frombuffer(bruto, dtype=numpy.float32)
modelo = WhisperModel(a.modelo, device='cpu', compute_type='int8', cpu_threads=os.cpu_count() or 4)
trechos, info = modelo.transcribe(
    audio, language='pt', beam_size=5, vad_filter=True,
    initial_prompt=a.prompt, condition_on_previous_text=False,
)
inicio = time.time()
sys.stderr.write(f'duração do áudio: {hms(info.duration)}\n')
with open(a.saida + '.parcial', 'w', encoding='utf-8') as f:
    for t in trechos:
        f.write(f'[{hms(t.start)}] {t.text.strip()}\n')
        f.flush()
        gasto = time.time() - inicio
        sys.stderr.write(f'\r{hms(t.end)} de {hms(info.duration)} (gastos {hms(gasto)})')
os.replace(a.saida + '.parcial', a.saida)
sys.stderr.write(f'\npronto: {a.saida} em {hms(time.time() - inicio)}\n')
