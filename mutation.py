import csv
from difflib import SequenceMatcher
import matplotlib.pyplot as plt
import pandas as pd

# DNA dizilerini dosyadan veya kullanıcıdan alma işlevi
def get_dna_sequences():
    """
    Kullanıcıya DNA dizisini dosyadan mı yoksa manuel mi gireceğini sorar.
    Dosya seçilirse iki DNA dizisi dosyadan okunur, 
    aksi takdirde kullanıcıdan manuel olarak alınır.
    
    Returns:
        dna1 (str): Birinci DNA dizisi.
        dna2 (str): İkinci DNA dizisi.
    """
    choice = input("DNA dizisini dosyadan mı yüklemek istersiniz? (E/H): ").lower()
    if choice == 'e':
        file_path = input("Dosya yolunu girin: ")
        with open(file_path, 'r') as file:
            lines = file.readlines()
            dna1 = lines[0].strip().upper()  # Dosyadan okunan ilk DNA dizisi
            dna2 = lines[1].strip().upper()  # Dosyadan okunan ikinci DNA dizisi
    else:
        dna1 = input("Birinci DNA dizisini girin: ").upper()  # Kullanıcıdan alınan ilk DNA dizisi
        dna2 = input("İkinci DNA dizisini girin: ").upper()  # Kullanıcıdan alınan ikinci DNA dizisi
    return dna1, dna2

# DNA dizileri uzunluk karşılaştırması
def check_length(dna1, dna2):
    """
    İki DNA dizisinin uzunluklarını karşılaştırır ve eşit olup olmadığını bildirir.

    Args:
        dna1 (str): Birinci DNA dizisi.
        dna2 (str): İkinci DNA dizisi.

    Returns:
        bool: Dizilerin aynı uzunlukta olup olmadığını belirtir.
    """
    if len(dna1) == len(dna2):
        print("\nDiziler aynı uzunlukta, baz bazına karşılaştırma yapılacak.\n")
        return True
    else:
        print("\nDiziler farklı uzunlukta, hizalama yapılacak.\n")
        return False

# Aynı uzunluktaki diziler için mutasyonları bulma
def find_mutations(dna1, dna2):
    """
    İki aynı uzunluktaki DNA dizisini karşılaştırarak mutasyonları tespit eder.

    Args:
        dna1 (str): Birinci DNA dizisi.
        dna2 (str): İkinci DNA dizisi.

    Returns:
        mutations (list): Mutasyonların pozisyon ve değişikliklerini içeren liste.
    """
    mutations = []
    for i in range(len(dna1)):
        if dna1[i] != dna2[i]:
            # Mutasyonun pozisyonu, orijinal ve mutasyonlu bazları listeye ekler
            mutations.append((i + 1, dna1[i], dna2[i]))
    return mutations

# Farklı uzunluktaki diziler için hizalama ve mutasyon bulma
def align_dna(dna1, dna2):
    """
    İki farklı uzunluktaki DNA dizisini hizalayarak mutasyonları bulur.

    Args:
        dna1 (str): Birinci DNA dizisi.
        dna2 (str): İkinci DNA dizisi.

    Returns:
        mutations (list): Mutasyonların pozisyon ve değişikliklerini içeren liste.
    """
    matcher = SequenceMatcher(None, dna1, dna2)
    mutations = []
    for opcode in matcher.get_opcodes():
        tag, a0, a1, b0, b1 = opcode
        if tag == 'replace':
            mutations.append((a0 + 1, dna1[a0:a1], dna2[b0:b1]))  # Değiştirilen bazlar
        elif tag == 'delete':
            mutations.append((a0 + 1, dna1[a0:a1], '-'))  # Silinen bazlar
        elif tag == 'insert':
            mutations.append((a0 + 1, '-', dna2[b0:b1]))  # Eklenen bazlar
    return mutations

# Mutasyonları CSV dosyasına kaydetme işlevi
def save_to_csv(mutations):
    """
    Bulunan mutasyonları bir CSV dosyasına kaydeder.

    Args:
        mutations (list): Mutasyonların pozisyon ve değişikliklerini içeren liste.
    """
    with open("mutations.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Pozisyon", "Orijinal", "Mutasyonlu"])
        writer.writerows(mutations)
    print("\nMutasyonlar 'mutations.csv' dosyasına kaydedildi.")

# Mutasyon raporu oluşturma
def report_mutations(mutations):
    """
    Bulunan mutasyonları kullanıcıya raporlar ve CSV dosyasına kaydeder.

    Args:
        mutations (list): Mutasyonların pozisyon ve değişikliklerini içeren liste.
    """
    if not mutations:
        print("Hiçbir mutasyon tespit edilmedi.")
    else:
        print(f"Toplam {len(mutations)} mutasyon tespit edildi:")
        for mutation in mutations:
            print(f"Pozisyon {mutation[0]}: {mutation[1]} -> {mutation[2]}")
        
        save_to_csv(mutations)

# Mutasyonları grafik olarak görselleştirme
def plot_mutations(mutations):
    """
    Bulunan mutasyonları bir bar grafiği ile görselleştirir.

    Args:
        mutations (list): Mutasyonların pozisyon ve değişikliklerini içeren liste.
    """
    df = pd.DataFrame(mutations, columns=['Pozisyon', 'Orijinal', 'Mutasyonlu'])
    plt.bar(df['Pozisyon'], height=1)
    plt.title("Mutasyonların Pozisyonları")
    plt.xlabel("Pozisyon")
    plt.ylabel("Mutasyon Sayısı")
    plt.show()

# Ana çalışma fonksiyonu
def main():
    """
    Programın ana akışını yöneten işlev.
    Kullanıcıdan DNA dizilerini alır, mutasyonları bulur, raporlar ve isteğe bağlı olarak grafik gösterir.
    """
    dna1, dna2 = get_dna_sequences()
    if check_length(dna1, dna2):
        mutations = find_mutations(dna1, dna2)  # Aynı uzunluktaki diziler için mutasyon bulma
    else:
        mutations = align_dna(dna1, dna2)  # Farklı uzunluktaki diziler için hizalama ve mutasyon bulma
    
    report_mutations(mutations)
    
    # Kullanıcı grafik istiyorsa göster
    show_graph = input("Mutasyonları grafik olarak görmek ister misiniz? (E/H): ").lower()
    if show_graph == 'e':
        plot_mutations(mutations)

# Programın çalıştırılma noktası
if __name__ == "__main__":
    main()
