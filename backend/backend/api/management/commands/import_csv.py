import csv
from django.core.management.base import BaseCommand
from api.models import CryptoSymbols

# Ganti dengan path file CSV Anda
csv_file_path = 'D:\Downloads\crypto-symbol\crypto-symbol.csv'

class Command(BaseCommand):
    help = "Import data crypto symbols dari csv ke database"

    def handle(self, *args, **kwargs):
    # Buka file CSV
        with open(csv_file_path, mode='r', encoding='utf-8') as infile:
            csvreader = csv.DictReader(infile)
            
            # Iterasi setiap baris dan masukkan ke dalam model
            for row in csvreader:
                # Ambil nama dari kolom 'name' di CSV
                symbol_name = row['name']
                
                # Masukkan data ke dalam database
                CryptoSymbols.objects.create(name=symbol_name)
        
        self.stdout.write(self.style.SUCCESS("Import data selesai."))
