from matplotlib import pyplot as plt


poeti = [
    (1943, "Muntenia", ["Contemporan", "poezie socială"]),
    (1806, "Basarabia", ["Romanticism"]),
    (1854, "Muntenia", ["Simbolism"]),
    (1858, "Moldova", ["Realism", "Naturalism"]),
    (1888, "Basarabia", ["Poezie religioasă", "Simbolism"]),
    (1838, "Muntenia", ["Romanticism"]),
    (1950, "Muntenia", ["Contemporan"]),
    (1837, "Muntenia", ["Romanticism"]),
    (1819, "Muntenia", ["Romanticism"]),
    (1939, "Moldova", ["Contemporan", "poezie socială"]),
    (1881, "Moldova", ["Simbolism", "Decadență"]),
    (1866, "Transilvania", ["Realism", "Poporanism"]),
    (1935, "Basarabia", ["Poezie patriotică", "Lirică"]),
    (1906, "Bucovina", []),  
    (1949, "Basarabia", ["Contemporan", "poezie patriotică"]),
    (1895, "Transilvania", ["Modernism", "Simbolism"]),
    (1954, "Muntenia", ["Contemporan"]),
    (1850, "Moldova", ["Romanticism"])
]

def plot_poets_by_birthyear(poets):
    years = [poet[0] for poet in poets]
    plt.figure(figsize=(10, 3))
    plt.hist(years, bins=range(1800, 1950, 1), color='skyblue', edgecolor='black')
    plt.xlabel("Year of Birth")
    plt.ylabel("Number of Poets")
    plt.title("Poets by Birth Year")
    plt.tight_layout()
    plt.show()

def plot_poets_by_region(poets):
    regions = [poet[1] for poet in poets]
    region_counts = {region: regions.count(region) for region in set(regions)}
    
    plt.figure(figsize=(10, 3))
    plt.bar(region_counts.keys(), region_counts.values(), color='skyblue')
    plt.xlabel("Region")
    plt.ylabel("Number of Poets")
    plt.title("Poets by Region")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_poets_by_literary_movement(poets):
    movements = [movement for poet in poets for movement in poet[2]]
    movement_counts = {movement: movements.count(movement) for movement in set(movements)}
    
    plt.figure(figsize=(10, 3))
    plt.bar(movement_counts.keys(), movement_counts.values(), color='skyblue')
    plt.xlabel("Literary Movement")
    plt.ylabel("Number of Poets")
    plt.title("Poets by Literary Movement")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # plot_poets_by_birthyear(poeti)
    # plot_poets_by_region(poeti)
    plot_poets_by_literary_movement(poeti)